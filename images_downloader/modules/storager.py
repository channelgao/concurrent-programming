"""
coding:utf-8
@Software : PyCharm
@File : storager.py
@Time : 2023/4/7 10:49
@Author : Ryan Gao
@Email : 
@description : 
"""
from PIL import Image
from tqdm import tqdm

from images_downloader.modules.base import BaseModule
from images_downloader.modules import thread_pool_executor


class Storager(BaseModule):
    """
    存储模块
    """

    def __init__(self):
        super().__init__()

    def _process(self, item):
        # 保存图片
        content, path = item
        content = Image.fromarray(content.astype('uint8')).convert('RGB')
        content.save(path)

    def _process_singlethread(self, list_):
        # 单线程运行
        print('单线程图片保存中：')
        for item in tqdm(list_):
            self._process(item)

    def _process_multithread(self, list_):
        # 多线程运行
        task_list = []
        print('\n多线程图片保存中')
        for item in tqdm(list_):
            task_list.append(thread_pool_executor.submit(self._process, item))
        for task in task_list:
            task.result()

    def _process_multiprocess(self, list_):
        # 单进程运行
        pass

    def _process_coroutine(self, list_):
        # 协程运行
        pass