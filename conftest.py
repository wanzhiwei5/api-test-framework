"""
全局 pytest 配置 — 测试夹具（fixtures）定义
"""
import pytest
from core.client import APIClient


@pytest.fixture(scope="session")
def client() -> APIClient:
    """整个测试会话共用一个客户端实例"""
    return APIClient()


@pytest.fixture(autouse=True)
def print_separator():
    """每个测试自动打印分隔线，方便看日志"""
    print()
    yield