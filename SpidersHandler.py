#coding:utf-8
__author__ = 'Administrator'

from WeiboSpider import SeleniumWeiboCatch
import time

class SpidersHandler(object):
    def __init__(self,user_list,file):
        self.user_foo = []
        self.file = file
        cot = 0
        for user_id in user_list:
            info_dict = {}
            info_dict['id'] = user_id
            info_dict['buffer'] = None
            info_dict['spider'] = None
            info_dict['index'] = cot
            cot += 1
            self.user_foo.append(info_dict)

    def run(self):
        self.allocate_task()
        self.tear_down_all()

    def allocate_task(self):
        print('分配线程!')
        for user in self.user_foo:
            user['spider'] = SeleniumWeiboCatch(0,500,user)
            user['spider'].daemon = True
            user['spider'].start()
        time.sleep(10)
        print('线程分配完成!')
        while(1):
            time.sleep(10)

    def tear_down_all(self):
        for user in self.user_foo:
            user['spider'].tearDown()