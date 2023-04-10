"""
coding:utf-8
@Software : PyCharm
@File : scheduler.py
@Time : 2023/4/7 10:51
@Author : Ryan Gao
@Email : 
@description : 
"""
import os
import prettytable

from images_downloader.utils.timer import Timer
from images_downloader.modules.downloader import Downloader
from images_downloader.modules.hasher import Hasher
from images_downloader.modules.storager import Storager
from images_downloader.const import CalcType


class Scheduler(object):
    """
    调度模块
    """

    def __init__(self, image_url_path, save_path):
        self.image_url_path = image_url_path
        self.save_path = save_path

        self.timer = Timer()

        self.downloader = Downloader()
        self.hasher = Hasher()
        self.storager = Storager()

        if not os.path.exists(os.path.join('.', self.save_path)):
            os.makedirs(os.path.join('.', self.save_path))

    def _wrap_path(self, md5):
        # 生成保存路径
        filename = '{}.jpg'.format(md5)
        STORAGE_PATH = os.path.join('.', self.save_path)
        path = os.path.join(STORAGE_PATH, filename)
        return path

    def get_url_list(self, path):
        # 加载图片链接
        image_list = []
        list_file = os.path.join(path)
        with open(list_file, 'r') as f:
            image_list = [line.strip() for line in f]
        return image_list

    def set_calc_type(self, type_):
        # 设置计算类型
        if len(type_) < 3:
            type_ = [type_[0]] * 3
        self.downloader.set_calc_type(type_[0])
        self.hasher.set_calc_type(type_[1])
        self.storager.set_calc_type(type_[2])

    def process(self):
        # 调度逻辑
        save_path = []
        time_statistics = {}

        # 1、读取图片url
        image_url_list = self.get_url_list(self.image_url_path)
        # 2、调度下载模块
        self.timer.tick()
        image_list = self.downloader.process(image_url_list)
        time_statistics['network_time'] = self.timer.tock()
        # 3、调度哈希模块
        self.timer.tick()
        hash_list = self.hasher.process(image_list)
        time_statistics['cpu_time'] = self.timer.tock()
        # 4、调度存储模块
        for hash_name in hash_list:
            save_path.append(self._wrap_path(hash_name))
        self.timer.tick()
        self.storager.process(zip(image_list, save_path))
        time_statistics['disk_time'] = self.timer.tock()

        return time_statistics

    def statistics(self, log_list, calculate_items=None):
        # 统计模块
        list_size = len(log_list)
        calculate_items = ['network_time', 'cpu_time', 'disk_time']
        y_columns = ['类型', '单线程总耗时', '多线程总耗时', '多线程提升率', '多进程总耗时', '多进程提升率',
                     '协程总耗时', '协程提升率']

        y_columns = y_columns[:list_size*2]

        # 初始化，并设置y轴
        table = prettytable.PrettyTable(y_columns)

        # 初始化x轴
        x_row = {'network_time': ['network'], 'cpu_time': ['cpu'], 'disk_time': ['disk']}

        for index in range(list_size):
            x_row.get('network_time').append(log_list[index].get('network_time', None))
            x_row.get('cpu_time').append(log_list[index].get('cpu_time', None))
            x_row.get('disk_time').append(log_list[index].get('disk_time', None))

            if index >= 1:
                for item_index in range(len(calculate_items)):
                    time_ = log_list[0].get(calculate_items[item_index]) - log_list[index].get(
                        calculate_items[item_index])
                    lift_rate = '%.4f%%' % (time_ / log_list[0].get(calculate_items[item_index]) * 100)
                    x_row.get(calculate_items[item_index]).append(lift_rate)

        # x轴写入table
        table.add_row(x_row.get('network_time'))
        table.add_row(x_row.get('cpu_time'))
        table.add_row(x_row.get('disk_time'))
        print(table)


if __name__ == '__main__':
    log_list = []
    # 启动调度程序
    scheduler = Scheduler(image_url_path='image_list/baidu', save_path='images')
    # 单线程测试
    # 设置程序运行逻辑
    scheduler.set_calc_type([CalcType.SingleThread])
    # 调度开始
    log_list.append(scheduler.process())

    # 多线程测试
    # 设置程序运行逻辑
    scheduler.set_calc_type([CalcType.MultiThread] * 3)
    # 调度开始
    log_list.append(scheduler.process())

    # 多进程测试
    # 设置程序运行逻辑
    scheduler.set_calc_type([CalcType.MultiProcess] * 3)
    # 调度开始
    log_list.append(scheduler.process())

    # 统计并展示报表
    scheduler.statistics(log_list)
