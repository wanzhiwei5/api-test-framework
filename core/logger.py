"""
日志配置 — 测试执行过程全记录
"""
import logging
import sys
from core.config import config


def setup_logger(name: str = "api-test") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(config.log_level)

    # 控制台输出
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(config.log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = setup_logger()