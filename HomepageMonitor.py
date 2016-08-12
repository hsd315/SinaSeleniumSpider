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
from weiboClass import *
from func import access_homepage,send_mail
from selenium import webdriver


class HomepageMonitor:
    def __init__(self,user_account_id,conn=None):
        self.user_account_id = user_account_id
        self.driver = webdriver.Chrome()
        if conn:
            self.conn = conn


    def main_loop(self):
        browser = self.driver
        while(1):
            access_homepage(self.user_account_id,browser)
            for weiboEle in browser.find_elements_by_class_name('WB_feed_type'):
                weibo = Weibo(weiboEle,self.conn)
                weibo.show_in_cmd()
                #假如查到某条非置顶微博，数据库中已存，则下方不用检查，必然都已存，直接再刷新
                if weibo.get_db_id():
                    print('本条微博数据库中已存在')
                    if not weibo.is_top:
                        print('该微博非置顶，本页已无未存微博')
                        break
                    else:
                        print('该微博为置顶，向下方微博检测...\n\n')
                        continue
                print('检测到新微博，准备存入数据库...')
                if weibo.save_to_db():
                    self.new_weibo_action(content=weibo.content)
                print('\n\n')
            print('\n\n刷新访问...\n')


    def get_homepage_screenshot(self):
        new_browser = access_homepage(self.user_account_id)
        ele = new_browser.find_element_by_xpath('//*[@id="plc_main"]')
        ele.location_once_scrolled_into_view
        local_time = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
        save_name = 'Screenshots/'+local_time+'by'+self.user_account_id+'.png'
        try:
            self.driver.save_screenshot(save_name)
            print(self.user_account_id+': '+'图片保存成功，文件名为:'+save_name)
        except:
            print(self.user_account_id+': '+'图片保存失败')
        time.sleep(1)
        new_browser.close()
        return save_name


    def new_weibo_action(self,content):
        send_mail(
            subject = self.user_account_id+'发新微博了!',
            content = content + '\nplease check in http://weibo.com/u/'+ self.user_account_id + '?is_all=1',
            img_src = self.get_homepage_screenshot()
        )



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

    hpMontior.main_loop()

