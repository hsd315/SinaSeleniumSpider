#coding:utf-8
"""
@file:      weiboClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-8-19 20:30
@description:
            微博信息类，包括解析存储，传入对象为一个WB_feed_type类的div元素
"""

from selenium import webdriver
import time,pymysql
from func import access_homepage,time_str_convert_list,public_parse
from userClass import User


class Weibo:
    def __init__(self,weiboEle,conn=None):
        if conn:
            self.conn = conn
            self.cur = conn.cursor()
        self.weiboEle = weiboEle
        self.weibo_id = None
        self.via_weibo_id = None
        self.content = None
        self.user_id = None
        self.create_time = None
        self.source = None
        self.is_top = None
        self.via_cot = None
        self.like_cot = None
        self.comment_cot = None
        self.is_via = None
        self.submit_time = None
        self.parse()


    def show_in_cmd(self):
        print('**************微博信息**************')
        print('is_top :',self.is_top)
        print('like_cot :',self.like_cot)
        print('comment_cot :',self.comment_cot)
        print('via_cot :',self.via_cot)
        print('content :',self.content)
        print('weibo_id :',self.weibo_id)
        print(u'user_id :',self.user_id)
        print(u'submit_time :',self.submit_time)
        print(u'is_via :',self.is_via)
        print('source :',self.source)
        print('via_weibo_id :',self.via_weibo_id)
        print('**************微博信息**************')


    def parse(self):
        weiboEle = self.weiboEle
        if '&' in weiboEle.get_attribute('tbinfo'):
            self.is_via = 1
            self.via_weibo_id = weiboEle.get_attribute('omid')
            via_user_id = weiboEle.get_attribute('tbinfo').split('&')[-1].split('=')[-1]
            self.via_weibo_parse(
                via_weiboEle=weiboEle.find_element_by_class_name('WB_expand'),
                user_id=via_user_id,
                weibo_id=self.via_weibo_id
            )
        else:
            self.is_via = 0#即原创
        self.weibo_id = weiboEle.get_attribute('mid')
        handles = weiboEle.find_element_by_class_name('WB_feed_handle').find_elements_by_tag_name('em')
        self.via_cot = int(handles[3].text)
        self.comment_cot = int(handles[6].text)
        self.like_cot = int(handles[8].text)
        weibo_detail = weiboEle.find_element_by_class_name('WB_detail')
        wi = weibo_detail.find_elements_by_class_name('WB_info')
        self.user_id = wi[0].find_element_by_tag_name('a').get_attribute('usercard').split('&')[0].split('=')[-1]
        #存储注意先存user
        method_dict = public_parse(weiboEle=weiboEle)
        self.content = method_dict['content']
        self.submit_time = method_dict['submit_time']
        self.source = method_dict['source']
        try:
            wi[0].find_element_by_class_name('W_icon_feedpin')
            self.is_top = 1
        except:
            self.is_top = 0


    def via_weibo_parse(self,via_weiboEle,user_id,weibo_id):
        handles = via_weiboEle.find_elements_by_tag_name('em')
        via_cot = int(handles[-4].text)
        comment_cot = int(handles[-2].text)
        like_cot = int(handles[-1].text)
        method_dict = public_parse(weiboEle=via_weiboEle)
        is_top = 0
        is_via = 0
        via_weibo_id = None
        print('________内嵌原博信息________')
        print(is_top,like_cot,comment_cot,via_cot,method_dict['content'],weibo_id,user_id,method_dict['submit_time'],method_dict['source'],is_via,via_weibo_id)
        print('________内嵌原博信息________')
        self.save_to_db(
            *[False,is_top,like_cot,comment_cot,via_cot,method_dict['content'],weibo_id,user_id,method_dict['submit_time'],method_dict['source'],is_via,via_weibo_id]
        )


    def save_to_db(
        self,save_self=True,is_top=None,like_cot=None,comment_cot=None,
        via_cot=None,content=None,weibo_id=None,
        user_id=None,submit_time=None,
        source=None,is_via=None,via_weibo_id=None
    ):
        create_time = time.localtime()
        if save_self:
            user_id = self.user_id
        author_db_id = self.get_author_db_id(user_account_id=user_id)
        if not author_db_id:
            user = User(user_id,self.conn)
            user.show_in_cmd()
            user.save_to_db()
        else:
            print('作者已存')
        if save_self:
            method_tuple = (self.is_top,self.like_cot,self.comment_cot,self.via_cot,self.content,self.weibo_id,self.submit_time,self.source,self.is_via,self.via_weibo_id,create_time,author_db_id)
        else:
            method_tuple = (is_top,like_cot,comment_cot,via_cot,content,weibo_id,submit_time,source,is_via,via_weibo_id,create_time,author_db_id)
        try:
            self.cur.execute(
                'insert into weibo(is_top,like_cot,comment_cot,via_cot,content,weibo_id,submit_time,source,is_via,via_weibo_id,create_time,user)'
                'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                method_tuple
            )
            self.conn.commit()
            print ('Weibo save success!')
            return True
        except Exception as e:
            print ('Weibo save error:'+str(e))
        return False


    def get_author_db_id(self,user_account_id):
        self.cur.execute(
            'select id from user where account_id = ' + user_account_id
        )
        data = self.cur.fetchall()
        if data:
            return data[0][0]
        else:
            return False





if __name__=="__main__":
    conn = pymysql.connect(
        host='localhost',   port=3306,
        user='root',        passwd='',
        db='selenium_weibo',   charset='utf8'
    )
    browser = webdriver.Chrome()
    user_account_id = '1401880315'
    access_homepage(user_account_id,browser)
    weiboEles = browser.find_elements_by_class_name('WB_feed_type')
    for weiboEle in weiboEles:
        weibo = Weibo(weiboEle,conn)
        weibo.show_in_cmd()
        if weibo.save_to_db():
            pass#email
    browser.close()
    conn.close()

