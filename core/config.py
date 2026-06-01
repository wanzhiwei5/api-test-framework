"""
配置管理 — 支持多环境（dev/staging/prod）
"""
from pydantic_settings import BaseSettings

class TestConfig(BaseSettings):
    """从环境变量或 .env 文件读取配置"""

    # 被测系统地址
    base_url: str = "http://localhost:8000"

    # 超时设置（秒）
    timeout: int = 10

    # 测试报告目录
    report_dir: str = "reports"

    # 日志级别
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_prefix = "TEST_"


# 全局单例
config = TestConfig()