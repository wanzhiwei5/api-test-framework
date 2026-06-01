"""
HTTP 客户端封装 — 统一处理请求/响应/错误
"""
import requests
from core.config import config
from core.logger import logger


class APIClient:
    """API 测试客户端，封装所有 HTTP 方法"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.base_url
        self.session = requests.Session()
        self.session.timeout = config.timeout

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info(f"{method.upper()} {url}")

        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"← 状态码: {response.status_code}")
            if response.text:
                logger.debug(f"← 响应体: {response.text[:200]}")
            return response
        except requests.RequestException as e:
            logger.error(f"请求失败: {e}")
            raise

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, json: dict = None, **kwargs) -> requests.Response:
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: dict = None, **kwargs) -> requests.Response:
        return self._request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)