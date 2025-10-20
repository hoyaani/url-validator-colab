from setuptools import setup, find_packages

setup(
    name="url-validator-colab",
    version="2.0.0",
    description="URL 驗證器 - Google Colab 版本",
    author="Your Name",
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.28.0",
        "pandas>=1.3.0",
        "psutil>=5.9.0",
        "openpyxl>=3.8.0",
    ],
    packages=find_packages(),
)
