"""
视频文件上传系统
支持多格式、多文件上传，包含文件验证和安全检查
"""

import os
import hashlib
import mimetypes
from typing import Dict, List, Any, Optional
from pathlib import Path
import tempfile
import shutil

class FileUploader:
    """
    视频文件上传管理器
    支持安全的文件上传、验证和存储
    """
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        
        # 支持的文件格式
        self.supported_formats = {
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.mkv': 'video/x-matroska',
            '.wmv': 'video/x-ms-wmv',
            '.flv': 'video/x-flv',
            '.webm': 'video/webm',
            '.m4v': 'video/x-m4v'
        }
        
        # 文件大小限制 (500MB)
        self.max_file_size = 500 * 1024 * 1024
        
        # 安全检查配置
        self.forbidden_extensions = ['.exe', '.bat', '.cmd', '.scr', '.com']
        
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        验证上传的文件
        """
        validation_result = {
            "is_valid": False,
            "errors": [],
            "warnings": [],
            "file_info": {}
        }
        
        file_path = Path(file_path)
        
        # 检查文件是否存在
        if not file_path.exists():
            validation_result["errors"].append("文件不存在")
            return validation_result
        
        # 检查文件扩展名
        file_extension = file_path.suffix.lower()
        if file_extension not in self.supported_formats:
            validation_result["errors"].append(f"不支持的文件格式: {file_extension}")
        
        # 安全检查：防止恶意文件
        if file_extension in self.forbidden_extensions:
            validation_result["errors"].append("检测到潜在的安全风险文件")
            return validation_result
        
        # 检查文件大小
        file_size = file_path.stat().st_size
        if file_size > self.max_file_size:
            validation_result["errors"].append(f"文件大小超出限制 ({file_size / 1024 / 1024:.1f}MB > 500MB)")
        
        # 检查MIME类型
        mime_type, _ = mimetypes.guess_type(str(file_path))
        expected_mime = self.supported_formats.get(file_extension)
        
        if mime_type and expected_mime and not mime_type.startswith('video/'):
            validation_result["warnings"].append("文件MIME类型与扩展名不匹配")
        
        # 如果没有错误，标记为有效
        if not validation_result["errors"]:
            validation_result["is_valid"] = True
            validation_result["file_info"] = {
                "filename": file_path.name,
                "size": file_size,
                "extension": file_extension,
                "mime_type": mime_type or expected_mime,
                "size_mb": round(file_size / 1024 / 1024, 2)
            }
        
        return validation_result
    
    def calculate_file_hash(self, file_path: str) -> str:
        """
        计算文件的MD5哈希值，用于去重和完整性验证
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def generate_safe_filename(self, original_filename: str) -> str:
        """
        生成安全的文件名，避免路径遍历和特殊字符
        """
        # 移除路径分隔符和其他危险字符
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
        filename = "".join(c for c in original_filename if c in safe_chars)
        
        # 确保文件名不为空
        if not filename:
            filename = "unnamed_video"
        
        # 添加时间戳以避免冲突
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        name_parts = filename.rsplit('.', 1)
        if len(name_parts) == 2:
            return f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
        else:
            return f"{filename}_{timestamp}"
    
    def upload_file(self, source_path: str, custom_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        上传单个文件到指定目录
        """
        try:
            # 验证文件
            validation = self.validate_file(source_path)
            if not validation["is_valid"]:
                return {
                    "success": False,
                    "error": "文件验证失败",
                    "details": validation["errors"]
                }
            
            source_path = Path(source_path)
            
            # 生成安全的文件名
            if custom_filename:
                safe_filename = self.generate_safe_filename(custom_filename)
            else:
                safe_filename = self.generate_safe_filename(source_path.name)
            
            # 目标路径
            target_path = self.upload_dir / safe_filename
            
            # 如果文件已存在，添加序号
            counter = 1
            original_target = target_path
            while target_path.exists():
                name_parts = original_target.stem, original_target.suffix
                target_path = self.upload_dir / f"{name_parts[0]}_{counter}{name_parts[1]}"
                counter += 1
            
            # 复制文件
            shutil.copy2(source_path, target_path)
            
            # 计算文件哈希
            file_hash = self.calculate_file_hash(str(target_path))
            
            return {
                "success": True,
                "file_info": {
                    "original_name": source_path.name,
                    "uploaded_name": target_path.name,
                    "file_path": str(target_path),
                    "file_hash": file_hash,
                    **validation["file_info"]
                },
                "warnings": validation["warnings"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"上传失败: {str(e)}"
            }
    
    def upload_multiple_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        批量上传多个文件
        """
        results = {
            "successful_uploads": [],
            "failed_uploads": [],
            "total_files": len(file_paths),
            "success_count": 0,
            "failure_count": 0
        }
        
        for file_path in file_paths:
            upload_result = self.upload_file(file_path)
            
            if upload_result["success"]:
                results["successful_uploads"].append(upload_result)
                results["success_count"] += 1
            else:
                results["failed_uploads"].append({
                    "file_path": file_path,
                    "error": upload_result["error"]
                })
                results["failure_count"] += 1
        
        results["overall_success"] = results["failure_count"] == 0
        
        return results
    
    def get_uploaded_files(self) -> List[Dict[str, Any]]:
        """
        获取已上传的文件列表
        """
        uploaded_files = []
        
        for file_path in self.upload_dir.glob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                file_info = {
                    "filename": file_path.name,
                    "file_path": str(file_path),
                    "size": file_path.stat().st_size,
                    "size_mb": round(file_path.stat().st_size / 1024 / 1024, 2),
                    "created_time": file_path.stat().st_ctime,
                    "extension": file_path.suffix.lower()
                }
                uploaded_files.append(file_info)
        
        # 按创建时间排序
        uploaded_files.sort(key=lambda x: x["created_time"], reverse=True)
        
        return uploaded_files
    
    def delete_file(self, filename: str) -> Dict[str, Any]:
        """
        删除上传的文件
        """
        try:
            file_path = self.upload_dir / filename
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": "文件不存在"
                }
            
            file_path.unlink()
            
            return {
                "success": True,
                "message": f"文件 {filename} 已成功删除"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"删除文件失败: {str(e)}"
            }
    
    def cleanup_old_files(self, days_old: int = 7) -> Dict[str, Any]:
        """
        清理超过指定天数的旧文件
        """
        import time
        
        current_time = time.time()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)
        
        deleted_files = []
        error_files = []
        
        for file_path in self.upload_dir.glob("*"):
            if file_path.is_file():
                if file_path.stat().st_ctime < cutoff_time:
                    try:
                        file_path.unlink()
                        deleted_files.append(file_path.name)
                    except Exception as e:
                        error_files.append({
                            "filename": file_path.name,
                            "error": str(e)
                        })
        
        return {
            "deleted_count": len(deleted_files),
            "deleted_files": deleted_files,
            "error_count": len(error_files),
            "error_files": error_files
        }
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        获取存储空间信息
        """
        total_size = 0
        file_count = 0
        
        for file_path in self.upload_dir.glob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            "file_count": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "upload_directory": str(self.upload_dir),
            "max_file_size_mb": self.max_file_size / 1024 / 1024,
            "supported_formats": list(self.supported_formats.keys())
        } 