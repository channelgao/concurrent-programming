"""
coding:utf-8
@Software : PyCharm
@File : base.py
@Time : 2023/4/7 11:01
@Author : Ryan Gao
@Email : 
@description : 
"""
from images_downloader.const import CalcType


class BaseModule(object):
    """
    抽象模块
    """

    def __init__(self):
        # 初始化计算类型为单线程
        self.calc_type = CalcType.SingleThread

    def set_calc_type(self, type_):
        # 设置计算类型
        self.calc_type = type_

    def _process(self, url):
        # 业务代码
        raise NotImplementedError

    def _process_singlethread(self, list_):
        # 单线程运行
        raise NotImplementedError

    def _process_multithread(self, list_):
        # 多线程运行
        raise NotImplementedError

    def _process_multiprocess(self, list_):
        # 单进程运行
        raise NotImplementedError

    def _process_coroutine(self, list_):
        # 协程运行
        raise NotImplementedError

    def process(self, list_):
        # 运行入口
        if self.calc_type == CalcType.SingleThread:
            return self._process_singlethread(list_)
        elif self.calc_type == CalcType.MultiThread:
            return self._process_multithread(list_)
        elif self.calc_type == CalcType.MultiProcess:
            return self._process_multiprocess(list_)
        elif self.calc_type == CalcType.PyCoroutine:
            return self._process_coroutine(list_)
