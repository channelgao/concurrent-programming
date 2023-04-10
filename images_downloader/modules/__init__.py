"""
coding:utf-8
@Software : PyCharm
@File : __init__.py.py
@Time : 2023/4/7 10:58
@Author : Ryan Gao
@Email : 
@description : 
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from images_downloader.config import settings

thread_pool_executor = ThreadPoolExecutor(max_workers=settings.THREAD_MULTI_NUMS)
process_pool_executor = ProcessPoolExecutor(max_workers=settings.PROCESS_MULTI_NUMS)
