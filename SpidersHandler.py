#coding:utf-8
__author__ = 'Administrator'

from HomepageMonitor import HomepageMonitor
import time,pymysql

class SpidersHandler(object):
    def __init__(self,user_list,conn=None):
        if conn:
            self.conn = conn
        self.user_foo = user_list


    def run(self):
        self.allocate_task()

    def allocate_task(self):
        print('分配线程!')
        for user_id in self.user_foo:
            hpMonitor = HomepageMonitor(
                user_account_id = user_id,
                conn = self.conn
            )
            hpMonitor.start()
        print('线程分配完成!')
        while(1):
            time.sleep(10)



if __name__=='__main__':
    conn = pymysql.connect(
        host='localhost',   port=3306,
        user='root',        passwd='',
        db='selenium_weibo',   charset='utf8'
    )

    user_list = ['277772655','5360104594','5842071290']

    spiders = SpidersHandler(user_list,conn)

    spiders.run()