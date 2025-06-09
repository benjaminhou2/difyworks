"""
DifyWorks - 工作流自动化工具包

这是一个轻量级的 Python 自动化工具包，专为简化日常工作流程而设计。
"""

__version__ = "0.1.0"
__author__ = "DifyWorks Team"
__email__ = "admin@difyworks.com"

# 导入核心功能
from .main import DifyWorks, run_workflow

# 定义包的公共接口
__all__ = [
    "DifyWorks",
    "run_workflow",
    "__version__",
] 