#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,pymysql

class Weibo(object):
    def __init__(self,weiboEle):
        self.weiboEle = weiboEle#均为WB_detail类的div
        self.weibo_id = None
        self.content = None
        self.user_id = None
        self.create_time = None
        self.source = None
        self.is_top = None
        self.like_cot = None
        self.comment_cot = None
        self.is_via = None

    def show_in_cmd(self):
        print('**************微博信息**************')
        print('is_top :\t\t'+str(self.is_top))
        print('like_cot :\t\t'+str(self.like_cot))
        print('comment_cot :\t\t'+str(self.comment_cot))
        print('content :\t\t'+self.content)
        print('weibo_id :\t\t'+self.weibo_id)
        print('user_id :\t\t'+self.user_id)
        print('create_time :\t\t'+self.create_time)
        print('is_via :\t\t'+self.is_via)
        if self.source:
            print('source :\t\t'+self.source)
        print('**************微博信息**************')


    def weiboEleParse(self):
        weiboEle = self.weiboEle
        wi = weiboEle.find_elements_by_class_name['WB_info']
        if len(wi)==2:
            self.is_via = 1
        elif len(wi)==1:
            self.is_via = 0#即原创
        else:
            print(wi,len(wi))
        self.user_id = wi[0].find_element_by_tag_name('a').get_attribute('usercard').split('&')[0].split('=')[-1]



    def save_to_db(self):
        create_time = time.localtime()


if __name__=="__main__":
    pass