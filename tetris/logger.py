"""日志系统模块"""
import logging
import os
import sys
from datetime import datetime


def setup_logger(name: str = "tetris") -> logging.Logger:
    """设置并返回日志记录器"""
    logger = logging.getLogger(name)

    # 避免重复配置
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 获取日志文件路径（程序运行目录）
    log_dir = os.path.dirname(os.path.abspath(sys.argv[0])) or "."
    if not log_dir:
        log_dir = "."
    log_file = os.path.join(log_dir, "tetris.log")

    # 文件处理器 - 记录DEBUG级别
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"无法创建日志文件: {e}")

    # 控制台处理器 - 记录INFO级别
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info(f"日志系统已初始化，日志文件: {log_file}")
    return logger


# 全局日志实例
logger = setup_logger()