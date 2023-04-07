"""
coding:utf-8
@Software : PyCharm
@File : const.py
@Time : 2023/4/7 11:03
@Author : Ryan Gao
@Email : 
@description : 
"""
from enum import Enum


class CalcType(Enum):
    """
    计算类型
    """
    SingleThread = 0
    MultiThread = 1
    MultiProcess = 2
    PyCoroutine = 3