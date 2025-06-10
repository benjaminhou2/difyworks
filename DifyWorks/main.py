#!/usr/bin/env python3
"""
DifyWorks 短视频质量分析系统
主程序入口文件

使用方法:
python main.py --video path/to/video.mp4
python main.py --batch path/to/video/folder
python main.py --demo  # 运行演示模式
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any

# 添加src目录到Python路径
sys.path.append(str(Path(__file__).parent / "src"))

from src.video_analyzer import VideoAnalyzer
from src.file_uploader import FileUploader
from src.workflow_engine import WorkflowEngine
from src.error_handler import error_handler

class DifyWorksMain:
    """
    DifyWorks主程序类
    """
    
    def __init__(self):
        self.video_analyzer = VideoAnalyzer()
        self.file_uploader = FileUploader()
        self.workflow_engine = WorkflowEngine()
        
        print("🎬 DifyWorks 短视频质量分析系统 v1.0")
        print("=" * 50)
    
    def analyze_single_video(self, video_path: str, analysis_depth: str = "standard") -> Dict[str, Any]:
        """
        分析单个视频文件
        """
        try:
            print(f"📹 开始分析视频: {Path(video_path).name}")
            
            # 验证文件
            validation = error_handler.validate_video_file(video_path)
            if not validation["is_valid"]:
                print(f"❌ 文件验证失败:")
                for error in validation["errors"]:
                    print(f"   - {error}")
                return {"status": "failed", "errors": validation["errors"]}
            
            # 执行工作流分析
            print("🔄 执行视频分析工作流...")
            result = self.workflow_engine.process_workflow(video_path)
            
            if result["status"] == "completed":
                # 显示分析结果
                self._display_results(result)
                
                # 导出报告
                report_file = self.workflow_engine.export_results(result)
                print(f"📄 分析报告已保存: {report_file}")
                
            else:
                print(f"❌ 分析失败: {result.get('error', '未知错误')}")
            
            return result
            
        except Exception as e:
            error_response = error_handler.handle_error(e, "single_video_analysis", {"video_path": video_path})
            print(f"❌ 分析过程中发生错误: {error_response['user_message']}")
            print("💡 建议解决方案:")
            for suggestion in error_response["suggestions"]:
                print(f"   - {suggestion}")
            return error_response
    
    def analyze_batch_videos(self, folder_path: str) -> Dict[str, Any]:
        """
        批量分析视频文件
        """
        try:
            folder_path = Path(folder_path)
            print(f"📁 开始批量分析文件夹: {folder_path}")
            
            # 查找视频文件
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            video_files = []
            
            for ext in video_extensions:
                video_files.extend(folder_path.glob(f"*{ext}"))
                video_files.extend(folder_path.glob(f"*{ext.upper()}"))
            
            if not video_files:
                print("❌ 未找到支持的视频文件")
                return {"status": "failed", "error": "未找到视频文件"}
            
            print(f"📊 找到 {len(video_files)} 个视频文件")
            
            # 批量处理
            video_paths = [str(f) for f in video_files]
            result = self.workflow_engine.process_workflow(video_paths)
            
            if result["status"] == "completed":
                # 显示批次分析结果
                self._display_batch_results(result)
                
                # 导出报告
                report_file = self.workflow_engine.export_results(result)
                print(f"📄 批次分析报告已保存: {report_file}")
                
            else:
                print(f"❌ 批量分析失败: {result.get('error', '未知错误')}")
            
            return result
            
        except Exception as e:
            error_response = error_handler.handle_error(e, "batch_video_analysis", {"folder_path": str(folder_path)})
            print(f"❌ 批量分析过程中发生错误: {error_response['user_message']}")
            return error_response
    
    def _display_results(self, result: Dict[str, Any]):
        """
        显示单个视频的分析结果
        """
        evaluation = result.get("comprehensive_evaluation", {})
        
        print("\n📊 分析结果摘要:")
        print("-" * 30)
        
        overall_eval = evaluation.get("overall_evaluation", {})
        print(f"综合评分: {overall_eval.get('score', 0)}/10 ({overall_eval.get('grade', 'N/A')}级)")
        print(f"质量等级: {overall_eval.get('level', '未知')}")
        
        # 各维度得分
        dimension_performance = evaluation.get("dimension_performance", {})
        if dimension_performance:
            print("\n📈 各维度评分:")
            for dimension, score in dimension_performance.items():
                if dimension != "overall":
                    print(f"  {dimension}: {score}/10")
        
        # 优势点
        strengths = evaluation.get("strengths", [])
        if strengths:
            print("\n✅ 优势亮点:")
            for strength in strengths[:3]:  # 显示前3个优势
                print(f"  • {strength}")
        
        # 改进建议
        improvements = evaluation.get("improvement_areas", [])
        if improvements:
            print("\n🔧 改进建议:")
            for improvement in improvements[:3]:  # 显示前3个建议
                print(f"  • {improvement}")
    
    def _display_batch_results(self, result: Dict[str, Any]):
        """
        显示批次分析结果
        """
        aggregated = result.get("aggregated_results", {})
        evaluation = result.get("comprehensive_evaluation", {})
        
        print("\n📊 批次分析结果:")
        print("-" * 30)
        
        print(f"总视频数: {aggregated.get('total_videos', 0)}")
        print(f"成功分析: {aggregated.get('successful_analyses', 0)}")
        print(f"分析失败: {aggregated.get('failed_analyses', 0)}")
        
        # 平均分数
        avg_scores = aggregated.get("average_scores", {})
        if avg_scores:
            print(f"\n📈 平均评分: {avg_scores.get('overall', 0)}/10")
            
            print("各维度平均分:")
            for dimension, score in avg_scores.items():
                if dimension != "overall":
                    print(f"  {dimension}: {score}/10")
        
        # 质量分布
        batch_stats = evaluation.get("batch_statistics", {})
        grade_dist = batch_stats.get("grade_distribution", {})
        if grade_dist:
            print("\n📊 质量等级分布:")
            for grade, count in grade_dist.items():
                print(f"  {grade}级: {count}个视频")
    
    def run_demo(self):
        """
        运行演示模式
        """
        print("🎭 演示模式")
        print("=" * 30)
        
        print("1. 系统健康检查...")
        health = error_handler.monitor_system_health()
        print(f"   系统状态: {health['overall_status']}")
        
        print("\n2. 视频分析能力演示...")
        print("   支持的视频格式: MP4, AVI, MOV, MKV, WMV, FLV, WebM")
        print("   分析维度:")
        print("   • 故事连贯性 - 评估情节逻辑和叙事结构")
        print("   • 画面统一性 - 分析视觉风格一致性")  
        print("   • 文案吸引力 - 评估语言表达和感染力")
        print("   • 画质清晰度 - 检查技术质量和清晰度")
        print("   • 技术制作 - 评估后期制作工艺水平")
        
        print("\n3. 智能分析路径:")
        print("   • 短视频 (≤30秒): 重点关注吸引力和冲击力")
        print("   • 中等时长 (30秒-5分钟): 平衡故事性和视觉效果")
        print("   • 长视频 (>5分钟): 深度分析结构和技术质量")
        
        print("\n4. 报告输出:")
        print("   • 综合评分等级 (S/A/B/C/D)")
        print("   • 详细的改进建议")
        print("   • 专业的分析报告")
        
        print(f"\n📝 使用示例:")
        print(f"   python main.py --video sample_video.mp4")
        print(f"   python main.py --batch ./videos/")
    
    def show_system_info(self):
        """
        显示系统信息
        """
        print("ℹ️  系统信息")
        print("=" * 30)
        
        health = error_handler.monitor_system_health()
        print(f"系统状态: {health['overall_status']}")
        
        for component, status in health.get('components', {}).items():
            print(f"{component}: {status['status']}")
        
        # 显示错误统计
        stats = error_handler.error_stats
        print(f"\n错误统计:")
        print(f"  总错误数: {stats['total_errors']}")
        print(f"  最近错误: {len(stats['recent_errors'])}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="DifyWorks 短视频质量分析系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s --video sample.mp4                    # 分析单个视频
  %(prog)s --batch ./videos                      # 批量分析文件夹中的视频
  %(prog)s --demo                                # 运行演示模式
  %(prog)s --info                                # 显示系统信息
        """
    )
    
    parser.add_argument("--video", "-v", 
                       help="分析单个视频文件的路径")
    parser.add_argument("--batch", "-b",
                       help="批量分析指定文件夹中的所有视频")
    parser.add_argument("--depth", "-d", 
                       choices=["quick", "standard", "detailed"],
                       default="standard",
                       help="分析深度 (默认: standard)")
    parser.add_argument("--demo", 
                       action="store_true",
                       help="运行演示模式")
    parser.add_argument("--info", 
                       action="store_true", 
                       help="显示系统信息")
    
    args = parser.parse_args()
    
    # 如果没有任何参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # 创建主程序实例
    app = DifyWorksMain()
    
    try:
        if args.demo:
            app.run_demo()
        elif args.info:
            app.show_system_info()
        elif args.video:
            if not os.path.exists(args.video):
                print(f"❌ 视频文件不存在: {args.video}")
                return
            app.analyze_single_video(args.video, args.depth)
        elif args.batch:
            if not os.path.exists(args.batch):
                print(f"❌ 文件夹不存在: {args.batch}")
                return
            app.analyze_batch_videos(args.batch)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断操作")
    except Exception as e:
        error_response = error_handler.handle_error(e, "main_program")
        print(f"\n❌ 程序运行错误: {error_response['user_message']}")

if __name__ == "__main__":
    main() 