"""
coding:utf-8
@Software : PyCharm
@File : downloader.py
@Time : 2023/4/7 10:49
@Author : Ryan Gao
@Email : 
@description : 
"""
import requests
import numpy as np
from PIL import ImageFile
from tqdm import tqdm

from images_downloader.modules.base import BaseModule
from images_downloader.modules import thread_pool_executor, process_pool_executor


class Downloader(BaseModule):
    """
    下载模块
    """

    def __init__(self):
        super().__init__()

    def _process(self, url):
        # 下载图片
        response = requests.get(url)
        content = response.content
        # 图片转numpy数组
        parser = ImageFile.Parser()
        parser.feed(content)
        img = parser.close()
        img = np.array(img)
        return img

    def _process_singlethread(self, list_):
        # 单线程运行
        response_list = []
        print('单线程图片下载中：')
        for url in tqdm(list_):
            img = self._process(url)
            response_list.append(img)
        return response_list

    def _process_multithread(self, list_):
        # 多线程运行
        response_list = []
        task_list = []
        print('\n多线程图片下载中：')
        for url in list_:
            # 多线程加载任务
            task = thread_pool_executor.submit(self._process, url)
            task_list.append(task)
        for task in tqdm(task_list):
            # 获取函数返回值
            img = task.result()
            response_list.append(img)
        return response_list

    def _process_multiprocess(self, list_):
        # 单进程运行
        response_list = []
        task_list = []
        print('\n多进程图片下载中：')
        for url in list_:
            # 多进程加载任务
            task = process_pool_executor.submit(self._process, url)
            task_list.append(task)
        for task in tqdm(task_list):
            # 获取函数返回值
            img = task.result()
            response_list.append(img)
        return response_list

    def _process_coroutine(self, list_):
        # 协程运行
        pass


if __name__ == "__main__":
    downloader = Downloader()
    downloader.process(["https://t7.baidu.com/it/u=4198287529,2774471735&fm=193&f=GIF"])