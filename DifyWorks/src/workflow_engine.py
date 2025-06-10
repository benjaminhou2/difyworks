"""
Dify工作流引擎
实现智能条件分支逻辑、结果聚合和综合评估系统
"""

from typing import Dict, List, Any, Optional, Union
import json
from datetime import datetime
from pathlib import Path
from .video_analyzer import VideoAnalyzer
from .file_uploader import FileUploader

class WorkflowEngine:
    """
    视频分析工作流引擎
    基于视频特征实现智能分析路径选择和结果聚合
    """
    
    def __init__(self):
        self.video_analyzer = VideoAnalyzer()
        self.file_uploader = FileUploader()
        self.analysis_history = []
        
        # 工作流配置
        self.workflow_config = {
            "parallel_analysis": True,
            "enable_caching": True,
            "max_concurrent_tasks": 5,
            "timeout_seconds": 300
        }
        
        # 分析阈值配置
        self.thresholds = {
            "duration_short": 30,      # 30秒以下为短视频
            "duration_medium": 300,    # 5分钟以下为中等时长
            "resolution_hd": 720,      # 720p以上为高清
            "file_size_large": 100     # 100MB以上为大文件
        }
    
    def determine_analysis_path(self, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于视频特征确定分析路径
        实现智能条件分支逻辑
        """
        duration = video_info.get("duration", 0)
        resolution = video_info.get("resolution", {})
        file_size_mb = video_info.get("file_size", 0) / (1024 * 1024)
        
        height = resolution.get("height", 0)
        
        analysis_path = {
            "path_type": "standard",
            "priority_dimensions": [],
            "analysis_depth": "normal",
            "estimated_time": 60,
            "special_considerations": []
        }
        
        # 根据时长确定路径
        if duration <= self.thresholds["duration_short"]:
            analysis_path["path_type"] = "short_form"
            analysis_path["priority_dimensions"] = ["script_appeal", "visual_consistency"]
            analysis_path["estimated_time"] = 30
            analysis_path["special_considerations"].append("短视频：重点关注吸引力和视觉冲击")
            
        elif duration <= self.thresholds["duration_medium"]:
            analysis_path["path_type"] = "medium_form"
            analysis_path["priority_dimensions"] = ["story_coherence", "script_appeal", "visual_consistency"]
            analysis_path["estimated_time"] = 45
            analysis_path["special_considerations"].append("中等时长：平衡故事性和视觉效果")
            
        else:
            analysis_path["path_type"] = "long_form"
            analysis_path["priority_dimensions"] = ["story_coherence", "technical_production"]
            analysis_path["analysis_depth"] = "detailed"
            analysis_path["estimated_time"] = 90
            analysis_path["special_considerations"].append("长视频：深度分析故事结构和技术质量")
        
        # 根据分辨率调整分析重点
        if height >= self.thresholds["resolution_hd"]:
            analysis_path["priority_dimensions"].append("image_quality")
            analysis_path["special_considerations"].append("高清视频：加强画质分析")
        else:
            analysis_path["special_considerations"].append("标清视频：重点关注内容质量")
        
        # 根据文件大小调整策略
        if file_size_mb >= self.thresholds["file_size_large"]:
            analysis_path["special_considerations"].append("大文件：可能包含丰富的技术细节")
            analysis_path["priority_dimensions"].append("technical_production")
        
        return analysis_path
    
    def execute_conditional_analysis(self, video_path: str, analysis_path: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于分析路径执行条件分析
        """
        try:
            # 获取视频基础信息
            video_info = self.video_analyzer.extract_video_info(video_path)
            
            if not video_info["is_valid"]:
                return {"error": "视频文件无效", "status": "failed"}
            
            # 提取关键帧
            frames = self.video_analyzer.extract_key_frames(video_path)
            
            if not frames:
                return {"error": "无法提取视频帧", "status": "failed"}
            
            # 根据分析路径执行相应的分析
            analyses = {}
            priority_dimensions = analysis_path.get("priority_dimensions", [])
            
            # 执行优先级分析
            if "story_coherence" in priority_dimensions:
                analyses["story_coherence"] = self.video_analyzer.analyze_story_coherence(frames, video_info)
            
            if "visual_consistency" in priority_dimensions:
                analyses["visual_consistency"] = self.video_analyzer.analyze_visual_consistency(frames, video_info)
            
            if "script_appeal" in priority_dimensions:
                analyses["script_appeal"] = self.video_analyzer.analyze_script_appeal(frames, video_info)
            
            if "image_quality" in priority_dimensions:
                analyses["image_quality"] = self.video_analyzer.analyze_image_quality(frames, video_info)
            
            if "technical_production" in priority_dimensions:
                analyses["technical_production"] = self.video_analyzer.analyze_technical_production(frames, video_info)
            
            # 如果是详细分析，执行所有维度
            if analysis_path.get("analysis_depth") == "detailed":
                all_analyses = {
                    "story_coherence": self.video_analyzer.analyze_story_coherence(frames, video_info),
                    "visual_consistency": self.video_analyzer.analyze_visual_consistency(frames, video_info),
                    "script_appeal": self.video_analyzer.analyze_script_appeal(frames, video_info),
                    "image_quality": self.video_analyzer.analyze_image_quality(frames, video_info),
                    "technical_production": self.video_analyzer.analyze_technical_production(frames, video_info)
                }
                analyses.update(all_analyses)
            
            return {
                "video_info": video_info,
                "analysis_path": analysis_path,
                "analyses": analyses,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": f"条件分析执行失败: {str(e)}",
                "status": "failed"
            }
    
    def aggregate_results(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        聚合多个分析结果
        """
        if not analysis_results:
            return {"error": "没有可聚合的分析结果"}
        
        aggregated = {
            "total_videos": len(analysis_results),
            "successful_analyses": 0,
            "failed_analyses": 0,
            "average_scores": {},
            "batch_summary": {},
            "individual_results": []
        }
        
        successful_results = []
        
        for result in analysis_results:
            if result.get("status") == "success":
                aggregated["successful_analyses"] += 1
                successful_results.append(result)
                
                # 保存个别结果摘要
                if "comprehensive_report" in result:
                    individual_summary = {
                        "filename": result.get("video_info", {}).get("filename", "未知"),
                        "overall_score": result["comprehensive_report"].get("overall_score", 0),
                        "grade": result["comprehensive_report"].get("grade", "N/A"),
                        "quality_level": result["comprehensive_report"].get("quality_level", "未知")
                    }
                    aggregated["individual_results"].append(individual_summary)
            else:
                aggregated["failed_analyses"] += 1
        
        # 计算平均分数
        if successful_results:
            dimension_scores = {}
            overall_scores = []
            
            for result in successful_results:
                if "comprehensive_report" in result:
                    report = result["comprehensive_report"]
                    overall_scores.append(report.get("overall_score", 0))
                    
                    dimension_scores_data = report.get("dimension_scores", {})
                    for dimension, score in dimension_scores_data.items():
                        if dimension not in dimension_scores:
                            dimension_scores[dimension] = []
                        dimension_scores[dimension].append(score)
            
            # 计算各维度平均分
            for dimension, scores in dimension_scores.items():
                aggregated["average_scores"][dimension] = round(sum(scores) / len(scores), 2)
            
            # 计算总体平均分
            if overall_scores:
                aggregated["average_scores"]["overall"] = round(sum(overall_scores) / len(overall_scores), 2)
        
        # 生成批次摘要
        aggregated["batch_summary"] = self.generate_batch_summary(successful_results)
        
        return aggregated
    
    def generate_batch_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成批次分析摘要
        """
        if not results:
            return {"message": "没有成功的分析结果"}
        
        # 统计各等级视频数量
        grade_counts = {}
        quality_levels = {}
        
        total_duration = 0
        total_file_size = 0
        
        for result in results:
            video_info = result.get("video_info", {})
            comprehensive_report = result.get("comprehensive_report", {})
            
            # 统计等级
            grade = comprehensive_report.get("grade", "N/A")
            quality_level = comprehensive_report.get("quality_level", "未知")
            
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
            quality_levels[quality_level] = quality_levels.get(quality_level, 0) + 1
            
            # 累计时长和文件大小
            total_duration += video_info.get("duration", 0)
            total_file_size += video_info.get("file_size", 0)
        
        # 生成建议
        recommendations = []
        
        high_quality_count = grade_counts.get("A", 0) + grade_counts.get("S", 0)
        total_count = len(results)
        
        if high_quality_count / total_count > 0.8:
            recommendations.append("批次整体质量优秀，建议保持当前制作水准")
        elif high_quality_count / total_count > 0.5:
            recommendations.append("批次质量良好，建议优化低分视频")
        else:
            recommendations.append("批次质量需要提升，建议重新审视制作流程")
        
        return {
            "total_videos": total_count,
            "grade_distribution": grade_counts,
            "quality_distribution": quality_levels,
            "total_duration_minutes": round(total_duration / 60, 2),
            "total_file_size_mb": round(total_file_size / (1024 * 1024), 2),
            "high_quality_ratio": round(high_quality_count / total_count, 2),
            "recommendations": recommendations
        }
    
    def generate_comprehensive_evaluation(self, aggregated_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于聚合结果生成综合评估
        """
        if aggregated_results.get("successful_analyses", 0) == 0:
            return {"error": "没有可评估的成功分析结果"}
        
        average_scores = aggregated_results.get("average_scores", {})
        batch_summary = aggregated_results.get("batch_summary", {})
        
        overall_avg = average_scores.get("overall", 0)
        
        # 生成评估等级
        if overall_avg >= 9:
            evaluation_grade = "卓越"
            evaluation_level = "S"
        elif overall_avg >= 8:
            evaluation_grade = "优秀"
            evaluation_level = "A"
        elif overall_avg >= 7:
            evaluation_grade = "良好"
            evaluation_level = "B"
        elif overall_avg >= 6:
            evaluation_grade = "一般"
            evaluation_level = "C"
        else:
            evaluation_grade = "需改进"
            evaluation_level = "D"
        
        # 识别强项和弱项
        strengths = []
        weaknesses = []
        
        for dimension, score in average_scores.items():
            if dimension != "overall":
                if score >= 8.5:
                    strengths.append(f"{dimension}: {score}分 (优秀)")
                elif score < 7:
                    weaknesses.append(f"{dimension}: {score}分 (需改进)")
        
        # 生成具体建议
        recommendations = []
        
        if weaknesses:
            recommendations.append(f"重点改进：{', '.join([w.split(':')[0] for w in weaknesses])}")
        
        if strengths:
            recommendations.append(f"保持优势：{', '.join([s.split(':')[0] for s in strengths])}")
        
        # 添加批次级别建议
        recommendations.extend(batch_summary.get("recommendations", []))
        
        return {
            "evaluation_timestamp": datetime.now().isoformat(),
            "overall_evaluation": {
                "score": overall_avg,
                "grade": evaluation_level,
                "level": evaluation_grade
            },
            "dimension_performance": average_scores,
            "batch_statistics": batch_summary,
            "strengths": strengths,
            "improvement_areas": weaknesses,
            "strategic_recommendations": recommendations,
            "quality_distribution": batch_summary.get("quality_distribution", {}),
            "summary": f"批次分析完成，共{aggregated_results['total_videos']}个视频，"
                      f"成功分析{aggregated_results['successful_analyses']}个，"
                      f"整体评分{overall_avg}分（{evaluation_grade}）"
        }
    
    def process_workflow(self, video_paths: Union[str, List[str]]) -> Dict[str, Any]:
        """
        执行完整的工作流程
        支持单个或批量视频处理
        """
        start_time = datetime.now()
        
        # 确保输入是列表格式
        if isinstance(video_paths, str):
            video_paths = [video_paths]
        
        workflow_results = {
            "workflow_id": f"workflow_{start_time.strftime('%Y%m%d_%H%M%S')}",
            "start_time": start_time.isoformat(),
            "total_videos": len(video_paths),
            "processing_results": [],
            "aggregated_results": {},
            "comprehensive_evaluation": {},
            "status": "processing"
        }
        
        try:
            # 处理每个视频
            analysis_results = []
            
            for video_path in video_paths:
                try:
                    # 1. 提取视频信息
                    video_info = self.video_analyzer.extract_video_info(video_path)
                    
                    # 2. 确定分析路径
                    analysis_path = self.determine_analysis_path(video_info)
                    
                    # 3. 执行条件分析
                    analysis_result = self.execute_conditional_analysis(video_path, analysis_path)
                    
                    # 4. 生成综合报告
                    if analysis_result.get("status") == "success":
                        comprehensive_report = self.video_analyzer.generate_comprehensive_report(
                            analysis_result["analyses"]
                        )
                        analysis_result["comprehensive_report"] = comprehensive_report
                    
                    analysis_results.append(analysis_result)
                    workflow_results["processing_results"].append({
                        "video_path": video_path,
                        "status": analysis_result.get("status", "failed"),
                        "analysis_path": analysis_result.get("analysis_path", {}),
                        "summary": analysis_result.get("comprehensive_report", {}).get("overall_score", 0)
                    })
                    
                except Exception as e:
                    error_result = {
                        "video_path": video_path,
                        "status": "failed",
                        "error": str(e)
                    }
                    analysis_results.append(error_result)
                    workflow_results["processing_results"].append(error_result)
            
            # 5. 聚合结果
            workflow_results["aggregated_results"] = self.aggregate_results(analysis_results)
            
            # 6. 生成综合评估
            workflow_results["comprehensive_evaluation"] = self.generate_comprehensive_evaluation(
                workflow_results["aggregated_results"]
            )
            
            # 7. 保存到历史记录
            self.analysis_history.append(workflow_results)
            
            workflow_results["status"] = "completed"
            workflow_results["end_time"] = datetime.now().isoformat()
            workflow_results["processing_time_seconds"] = (
                datetime.now() - start_time
            ).total_seconds()
            
            return workflow_results
            
        except Exception as e:
            workflow_results["status"] = "failed"
            workflow_results["error"] = str(e)
            workflow_results["end_time"] = datetime.now().isoformat()
            
            return workflow_results
    
    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """
        获取工作流历史记录
        """
        return self.analysis_history
    
    def export_results(self, workflow_results: Dict[str, Any], export_format: str = "json") -> str:
        """
        导出分析结果
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format.lower() == "json":
            filename = f"video_analysis_report_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(workflow_results, f, ensure_ascii=False, indent=2)
            return filename
        
        # 可以扩展其他格式的导出
        else:
            raise ValueError(f"不支持的导出格式: {export_format}") 