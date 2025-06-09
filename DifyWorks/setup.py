"""
DifyWorks 项目安装配置文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件作为长描述
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements.txt文件
def read_requirements():
    """读取requirements.txt文件中的依赖"""
    requirements = []
    try:
        with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 忽略注释和空行
                if line and not line.startswith('#'):
                    requirements.append(line)
    except FileNotFoundError:
        pass
    return requirements

setup(
    # 项目基本信息
    name="difyworks",
    version="0.1.0",
    author="DifyWorks Team",
    author_email="admin@difyworks.com",
    description="一个基于 Python 的工作流自动化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/DifyWorks",
    
    # 包配置
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Python版本要求
    python_requires=">=3.8",
    
    # 依赖包
    install_requires=read_requirements(),
    
    # 额外依赖
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    
    # 入口点配置
    entry_points={
        "console_scripts": [
            "difyworks=main:main",
        ],
    },
    
    # 分类器
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    
    # 关键词
    keywords="automation, workflow, python, tools",
    
    # 项目URLs
    project_urls={
        "Bug Reports": "https://github.com/yourusername/DifyWorks/issues",
        "Source": "https://github.com/yourusername/DifyWorks",
        "Documentation": "https://github.com/yourusername/DifyWorks/docs",
    },
) 