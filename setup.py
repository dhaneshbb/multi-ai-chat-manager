#!/usr/bin/env python3
"""
Setup script for Multi-AI Chat Manager
For development installation and packaging
"""

from setuptools import setup, find_packages
import os
import sys

# Ensure we're on Windows
if sys.platform != 'win32':
    print("Warning: Multi-AI Chat Manager is designed for Windows only.")

# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# Read long description from README
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'readme.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Multi-AI Chat Manager - Send prompts to multiple AI platforms simultaneously"

setup(
    name="multi-ai-chat-manager",
    version="2.0.0",
    author="Multi-AI Chat Manager Developer",
    author_email="",
    description="Send prompts to multiple AI chat platforms simultaneously",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/dhaneshbb/multi-ai-chat-manager",
    project_urls={
        "Bug Reports": "https://github.com/dhaneshbb/multi-ai-chat-manager/issues",
        "Source": "https://github.com/dhaneshbb/multi-ai-chat-manager",
        "Documentation": "https://github.com/dhaneshbb/multi-ai-chat-manager#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Groupware",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Win32 (MS Windows)",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "build": [
            "pyinstaller>=6.0",
            "pillow>=8.0",  # For icons if needed
        ],
    },
    entry_points={
        "console_scripts": [
            "multi-ai-chat-manager=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "config.yml",
            "requirements.txt",
            "README.md",
            "LICENSE",
            "Chrome Extension/*.js",
            "Chrome Extension/*.json",
            "Build Tools/*.py",
            "assets/*.png",
            "assets/*.gif",
            "assets/*.svg",
        ],
    },
    exclude_package_data={
        "": [
            "build/*",
            "dist/*",
            "__pycache__/*",
            "*.pyc",
            "*.pyo",
            "logs/*",
            "input_history.txt",
        ],
    },
    keywords=[
        "ai", "chat", "automation", "productivity", "chatgpt", "claude", 
        "gemini", "perplexity", "grok", "deepseek", "window-management",
        "multi-platform", "prompt-engineering"
    ],
    platforms=["Windows"],
    zip_safe=False,
    
    # Custom metadata
    meta={
        "supported_ai_platforms": [
            "ChatGPT", "Claude", "Google Gemini", 
            "Perplexity", "Grok", "DeepSeek"
        ],
        "requires_chrome_extension": True,
        "windows_only": True,
    }
)
