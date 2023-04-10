"""
coding:utf-8
@Software : PyCharm
@File : hasher.py
@Time : 2023/4/7 10:49
@Author : Ryan Gao
@Email : 
@description : 
"""
import hashlib
from scipy import signal
from PIL import Image
from tqdm import tqdm

from images_downloader.modules.base import BaseModule
from images_downloader.modules import thread_pool_executor, process_pool_executor


class Hasher(BaseModule):
    """
    哈希模块
    """

    def __init__(self):
        super().__init__()

    def _process(self, item):
        # 计算图片md5
        # 卷积
        cov = [[[0.1], [0.05], [0.1]]]
        img = signal.convolve(item, cov)
        img = Image.fromarray(img.astype('uint8')).convert('RGB')
        # 哈希
        md5 = hashlib.md5(str(img).encode('utf-8')).hexdigest()
        return md5

    def _process_singlethread(self, list_):
        # 单线程运行
        md5_list = []
        print('单线程图片处理中：')
        for img in tqdm(list_):
            md5 = self._process(img)
            md5_list.append(md5)
        return md5_list

    def _process_multithread(self, list_):
        # 多线程运行
        md5_list = []
        task_list = []
        print('\n多线程图片处理中：')
        for img in list_:
            # 多线程加载任务
            task = thread_pool_executor.submit(self._process, img)
            task_list.append(task)
        for task in tqdm(task_list):
            md5 = task.result()
            md5_list.append(md5)
        return md5_list

    def _process_multiprocess(self, list_):
        # 单进程运行
        md5_list = []
        task_list = []
        print('\n多进程图片处理中：')
        for img in list_:
            # 多进程加载任务
            task = process_pool_executor.submit(self._process, img)
            task_list.append(task)
        for task in tqdm(task_list):
            md5 = task.result()
            md5_list.append(md5)
        return md5_list

    def _process_coroutine(self, list_):
        # 协程运行
        pass
