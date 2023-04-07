"""
coding:utf-8
@Software : PyCharm
@File : timer.py
@Time : 2023/4/7 11:51
@Author : Ryan Gao
@Email : 
@description : 
"""
import time


class Timer(object):
    """
    计时器
    """

    def __init__(self):
        self.val = time.time()

    def tick(self):
        self.val = time.time()

    def tock(self):
        return round(time.time() - self.val, 6)