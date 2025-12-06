"""Setup configuration for EasyQA AI Testing Framework."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easyqa-ai-framework",
    version="2.0.0",
    author="Anil Babu",
    description="AI-Powered Test Automation Framework with Multi-Language Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anil-babu/EasyQA-Framework",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.9",
    install_requires=[
        "playwright>=1.41.0",
        "selenium>=4.16.0",
        "pytest>=7.4.3",
        "tensorflow>=2.15.0",
        "opencv-python>=4.9.0",
        "scikit-learn>=1.3.2",
    ],
    extras_require={
        "dev": [
            "black>=23.12.1",
            "pylint>=3.0.3",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "easyqa=easyqa.cli:main",
        ],
    },
)
