#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志配置
设置统一的日志格式
"""

import logging
import sys


def setup_logger(
    name: str = "ai_skills_monitor", level: int = logging.INFO
) -> logging.Logger:
    """
    设置日志

    Args:
        name: 日志器名称
        level: 日志级别

    Returns:
        配置好的日志器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # 格式化
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
