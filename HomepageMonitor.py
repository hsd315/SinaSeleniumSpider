#coding:utf-8
"""
@file:      monitor_ones_homepage.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-8-12 12:30
@description:
            监测用户主页，新微博发邮件提示
"""
from weiboClass import Weibo
from func import access_homepage,send_mail
from selenium import webdriver
from threading import Thread
import random,pymysql,time


class HomepageMonitor(Thread):
    def __init__(self,user_account_id,conn=None):
        Thread.__init__(self)
        print(user_account_id+': 已分配得到线程')
        self.user_account_id = user_account_id
        self.driver = webdriver.Chrome()
        if conn:
            self.conn = conn


    def run(self):
        while(1):
            try:
                access_homepage(self.user_account_id,self.driver)
                weiboEle_list = self.driver.find_elements_by_class_name('WB_feed_type')
                new_weiboEle_list = self.get_new_weiboEle_list(weiboEle_list)
                if new_weiboEle_list:
                    print(self.user_account_id+':'+str(len(new_weiboEle_list))+'条新微博存在！')
                    for weiboEle in new_weiboEle_list:
                        weibo = Weibo(weiboEle,self.conn)
                        weibo.parse()
                        weibo.show_in_cmd()
                        if weibo.save_to_db():
                            self.new_weibo_action(content=weibo.content)
                        print('\n\n')
                else:
                    print(self.user_account_id+': '+'本页无未存微博')
            except:
                pass
            time.sleep(random.randint(2,4))


    def get_homepage_screenshot(self):
        new_browser = access_homepage(self.user_account_id,get_shot=True)
        ele = new_browser.find_element_by_xpath('//*[@id="plc_main"]')
        ele.location_once_scrolled_into_view
        time.sleep(1)
        local_time = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
        save_name = 'Screenshots/'+local_time+'by'+self.user_account_id+'.png'
        try:
            self.driver.save_screenshot(save_name)
            print(self.user_account_id+': '+'图片保存成功，文件名为:'+save_name)
        except:
            print(self.user_account_id+': '+'图片保存失败')
        new_browser.close()
        return save_name


    def new_weibo_action(self,content):
        send_mail(
            subject = self.user_account_id+'发新微博了!',
            content = content + '\nplease check in http://weibo.com/u/'+ self.user_account_id + '?is_all=1',
            img_src = self.get_homepage_screenshot()
        )


    def get_new_weiboEle_list(self,weiboEle_list):
        new_weiboEle_list = []
        for weiboEle in weiboEle_list:
            if not Weibo(weiboEle,self.conn).get_db_id():
                new_weiboEle_list.append(weiboEle)
        return new_weiboEle_list


if __name__=='__main__':
    conn = pymysql.connect(
        host='localhost',   port=3306,
        user='root',        passwd='',
        db='selenium_weibo',   charset='utf8'
    )

    hpMontior = HomepageMonitor(
        user_account_id = '571331191',
        conn = conn
    )

    hpMontior.run()

