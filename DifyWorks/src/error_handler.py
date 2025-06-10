"""
错误处理和异常管理模块
提供完善的错误处理、日志记录和系统稳定性保障
"""

import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import json

class ErrorHandler:
    """
    统一的错误处理和异常管理器
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 配置日志记录
        self._setup_logging()
        
        # 错误统计
        self.error_stats = {
            "total_errors": 0,
            "by_type": {},
            "by_module": {},
            "recent_errors": []
        }
        
        # 重试配置
        self.retry_config = {
            "max_retries": 3,
            "base_delay": 1.0,
            "max_delay": 60.0,
            "backoff_factor": 2.0
        }
    
    def _setup_logging(self):
        """配置日志系统"""
        log_file = self.log_dir / f"video_analysis_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 创建logger
        self.logger = logging.getLogger("VideoAnalysisSystem")
        self.logger.setLevel(logging.INFO)
        
        # 清除现有handlers
        self.logger.handlers.clear()
        
        # 文件handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def handle_error(self, 
                    error: Exception, 
                    context: str, 
                    details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        统一错误处理方法
        """
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "details": details or {},
            "traceback": traceback.format_exc()
        }
        
        # 记录日志
        self.logger.error(f"Error in {context}: {error}", extra={"error_info": error_info})
        
        # 更新统计
        self._update_error_stats(error_info)
        
        # 生成用户友好的错误响应
        user_response = self._generate_user_response(error_info)
        
        return {
            "status": "error",
            "error_id": f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_message": user_response["message"],
            "suggestions": user_response["suggestions"],
            "technical_details": error_info,
            "retry_possible": user_response["retry_possible"]
        }
    
    def _update_error_stats(self, error_info: Dict[str, Any]):
        """更新错误统计信息"""
        self.error_stats["total_errors"] += 1
        
        error_type = error_info["error_type"]
        context = error_info["context"]
        
        # 按类型统计
        if error_type not in self.error_stats["by_type"]:
            self.error_stats["by_type"][error_type] = 0
        self.error_stats["by_type"][error_type] += 1
        
        # 按模块统计
        if context not in self.error_stats["by_module"]:
            self.error_stats["by_module"][context] = 0
        self.error_stats["by_module"][context] += 1
        
        # 保存最近的错误
        self.error_stats["recent_errors"].append({
            "timestamp": error_info["timestamp"],
            "type": error_type,
            "context": context,
            "message": error_info["error_message"]
        })
        
        # 只保留最近50条错误
        if len(self.error_stats["recent_errors"]) > 50:
            self.error_stats["recent_errors"] = self.error_stats["recent_errors"][-50:]
    
    def _generate_user_response(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """生成用户友好的错误响应"""
        error_type = error_info["error_type"]
        context = error_info["context"]
        
        # 根据错误类型和上下文生成响应
        responses = {
            "FileNotFoundError": {
                "message": "找不到指定的视频文件，请检查文件路径是否正确。",
                "suggestions": [
                    "确认视频文件存在且未被移动或删除",
                    "检查文件路径是否正确",
                    "重新上传视频文件"
                ],
                "retry_possible": True
            },
            "PermissionError": {
                "message": "文件访问权限不足，无法读取视频文件。",
                "suggestions": [
                    "检查文件访问权限",
                    "尝试以管理员身份运行",
                    "将文件移动到有访问权限的目录"
                ],
                "retry_possible": True
            },
            "ValueError": {
                "message": "视频文件格式或内容存在问题。",
                "suggestions": [
                    "检查视频文件是否损坏",
                    "确认文件格式是否支持(MP4, AVI, MOV, MKV等)",
                    "尝试使用其他视频文件"
                ],
                "retry_possible": False
            },
            "ConnectionError": {
                "message": "网络连接失败，无法访问AI分析服务。",
                "suggestions": [
                    "检查网络连接是否正常",
                    "稍后重试",
                    "联系技术支持"
                ],
                "retry_possible": True
            },
            "TimeoutError": {
                "message": "分析处理超时，可能是文件过大或网络较慢。",
                "suggestions": [
                    "检查视频文件大小是否超过限制",
                    "确保网络连接稳定",
                    "尝试分析较小的视频文件"
                ],
                "retry_possible": True
            }
        }
        
        # 默认响应
        default_response = {
            "message": "分析过程中遇到未知错误，请联系技术支持。",
            "suggestions": [
                "重新尝试分析",
                "检查输入参数是否正确",
                "联系技术支持团队"
            ],
            "retry_possible": True
        }
        
        return responses.get(error_type, default_response)
    
    def retry_with_backoff(self, func, *args, **kwargs):
        """
        带退避策略的重试机制
        """
        last_exception = None
        
        for attempt in range(self.retry_config["max_retries"] + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.retry_config["max_retries"]:
                    delay = min(
                        self.retry_config["base_delay"] * (self.retry_config["backoff_factor"] ** attempt),
                        self.retry_config["max_delay"]
                    )
                    
                    self.logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.1f}s: {e}")
                    
                    import time
                    time.sleep(delay)
                else:
                    self.logger.error(f"All {self.retry_config['max_retries']} retry attempts failed")
        
        # 如果所有重试都失败，抛出最后一个异常
        raise last_exception
    
    def validate_video_file(self, file_path: str) -> Dict[str, Any]:
        """
        验证视频文件的有效性
        """
        try:
            file_path = Path(file_path)
            
            validation_result = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            # 检查文件是否存在
            if not file_path.exists():
                validation_result["is_valid"] = False
                validation_result["errors"].append("文件不存在")
                return validation_result
            
            # 检查文件大小
            file_size = file_path.stat().st_size
            max_size = 500 * 1024 * 1024  # 500MB
            
            if file_size > max_size:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"文件大小超过限制 ({file_size / 1024 / 1024:.1f}MB > 500MB)")
            
            # 检查文件扩展名
            supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            if file_path.suffix.lower() not in supported_formats:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"不支持的文件格式: {file_path.suffix}")
            
            # 尝试打开文件进行基础检查
            try:
                import cv2
                cap = cv2.VideoCapture(str(file_path))
                if not cap.isOpened():
                    validation_result["is_valid"] = False
                    validation_result["errors"].append("视频文件损坏或格式不支持")
                else:
                    # 检查是否有视频帧
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    if frame_count == 0:
                        validation_result["is_valid"] = False
                        validation_result["errors"].append("视频文件为空或无有效帧")
                cap.release()
            except Exception as e:
                validation_result["warnings"].append(f"无法验证视频内容: {str(e)}")
            
            return validation_result
            
        except Exception as e:
            return {
                "is_valid": False,
                "errors": [f"文件验证失败: {str(e)}"],
                "warnings": []
            }
    
    def monitor_system_health(self) -> Dict[str, Any]:
        """
        监控系统健康状态
        """
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "components": {}
        }
        
        try:
            # 检查磁盘空间
            import shutil
            disk_usage = shutil.disk_usage(".")
            free_space_gb = disk_usage.free / (1024**3)
            
            health_status["components"]["disk_space"] = {
                "status": "healthy" if free_space_gb > 1.0 else "warning",
                "free_space_gb": round(free_space_gb, 2),
                "message": f"可用空间: {free_space_gb:.1f}GB"
            }
            
            # 检查日志文件大小
            log_files = list(self.log_dir.glob("*.log"))
            total_log_size = sum(f.stat().st_size for f in log_files)
            log_size_mb = total_log_size / (1024**2)
            
            health_status["components"]["log_files"] = {
                "status": "healthy" if log_size_mb < 100 else "warning",
                "size_mb": round(log_size_mb, 2),
                "file_count": len(log_files)
            }
            
            # 检查错误率
            recent_errors = len([e for e in self.error_stats["recent_errors"] 
                                if (datetime.now() - datetime.fromisoformat(e["timestamp"])).seconds < 3600])
            
            health_status["components"]["error_rate"] = {
                "status": "healthy" if recent_errors < 10 else "warning",
                "recent_errors_count": recent_errors,
                "total_errors": self.error_stats["total_errors"]
            }
            
            # 确定整体状态
            component_statuses = [comp["status"] for comp in health_status["components"].values()]
            if "error" in component_statuses:
                health_status["overall_status"] = "error"
            elif "warning" in component_statuses:
                health_status["overall_status"] = "warning"
            
        except Exception as e:
            health_status["overall_status"] = "error"
            health_status["error"] = str(e)
        
        return health_status
    
    def export_error_report(self) -> str:
        """
        导出错误报告
        """
        report_file = self.log_dir / f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "statistics": self.error_stats,
            "system_health": self.monitor_system_health(),
            "configuration": self.retry_config
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return str(report_file)
    
    def clear_old_logs(self, days_to_keep: int = 7):
        """
        清理旧的日志文件
        """
        cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        deleted_files = []
        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    deleted_files.append(log_file.name)
                    self.logger.info(f"Deleted old log file: {log_file.name}")
                except Exception as e:
                    self.logger.error(f"Failed to delete log file {log_file.name}: {e}")
        
        return deleted_files

# 全局错误处理器实例
error_handler = ErrorHandler() 