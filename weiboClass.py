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
from func import access_homepage,public_parse,handle_try_int
from userClass import User


class Weibo:
    def __init__(self,weiboEle,conn=None):
        if conn:
            self.conn = conn
        self.weiboEle = weiboEle
        self.content = None
        self.source = None
        self.via_cot = None
        self.like_cot = None
        self.comment_cot = None
        self.submit_time = None
        self.create_time = None


    @property
    def weibo_id(self):
        return self.weiboEle.get_attribute('mid')


    @property
    def is_top(self):
        try:
            self.weiboEle.find_element_by_class_name('W_icon_feedpin')
            return 1
        except:
            return 0


    @property
    def is_via(self):
        return '&' in self.weiboEle.get_attribute('tbinfo')


    @property
    def via_weibo_id(self):
        if self.is_via:
            return self.weiboEle.get_attribute('omid')
        else:
            return None

    @property
    def author_account_id(self):
        wb_info = self.weiboEle.find_element_by_class_name('WB_detail').find_elements_by_class_name('WB_info')
        return wb_info[0].find_element_by_tag_name('a').get_attribute('usercard').split('&')[0].split('=')[-1]


    def show_in_cmd(self):
        print('**************WEIBO Info**************')
        print('is_top :',self.is_top)
        print('like_cot :',self.like_cot)
        print('comment_cot :',self.comment_cot)
        print('via_cot :',self.via_cot)
        print('content :',self.content)
        print('weibo_id :',self.weibo_id)
        print(u'author_account_id :',self.author_account_id)
        print(u'submit_time :',self.submit_time)
        print(u'is_via :',self.is_via)
        print('source :',self.source)
        print('via_weibo_id :',self.via_weibo_id)
        print('**************WEIBO Info**************')


    def parse(self):
        weiboEle = self.weiboEle
        if self.is_via:
            via_user_id = weiboEle.get_attribute('tbinfo').split('&')[-1].split('=')[-1]
            self.via_weibo_parse(
                via_weiboEle=weiboEle.find_element_by_class_name('WB_expand'),
                user_id=via_user_id,
                weibo_id=self.via_weibo_id
            )
        handles = weiboEle.find_element_by_class_name('WB_feed_handle').find_elements_by_tag_name('em')
        self.via_cot = handle_try_int(handles[3].text)
        self.comment_cot = handle_try_int(handles[6].text)
        self.like_cot = handle_try_int(handles[8].text)
        method_dict = public_parse(weiboEle=weiboEle)
        self.content = method_dict['content']
        self.submit_time = method_dict['submit_time']
        self.source = method_dict['source']



    def via_weibo_parse(self,via_weiboEle,user_id,weibo_id):
        handles = via_weiboEle.find_elements_by_tag_name('em')
        via_cot = handle_try_int(handles[-4].text)
        comment_cot = handle_try_int(handles[-2].text)
        like_cot = handle_try_int(handles[-1].text)
        method_dict = public_parse(weiboEle=via_weiboEle)
        is_top = 0
        is_via = 0
        via_weibo_id = None
        print('________Expand Weibo INFO________')
        print(is_top,like_cot,comment_cot,via_cot,method_dict['content'],weibo_id,user_id,method_dict['submit_time'],method_dict['source'],is_via,via_weibo_id)
        print('________Expand Weibo INFO________')
        self.save_to_db(
            *[False,is_top,like_cot,comment_cot,via_cot,method_dict['content'],weibo_id,user_id,method_dict['submit_time'],method_dict['source'],is_via,via_weibo_id]
        )


    def save_to_db(
        self,save_self=True,is_top=None,like_cot=None,comment_cot=None,
        via_cot=None,content=None,weibo_id=None,
        user_id=None,submit_time=None,
        source=None,is_via=None,via_weibo_id=None
    ):
        if save_self:
            user_id = self.author_account_id
            weibo_id = self.weibo_id
        if self.get_db_id(weibo_id):
            print('Weibo save error: Has been saved previously')
            return False
        author_db_id = self.get_author_db_id(user_account_id=user_id)
        if not author_db_id:
            user = User(
                user_account_id = user_id,
                conn = self.conn,
                #ready_browser = self.driver
            )
            user.show_in_cmd()
            user.save_to_db()
            #author_db_id = self.get_author_db_id(user_account_id=user_id)
            author_db_id = user.db_id
            user.destory()
        else:
            print('Author has been saved previously')
        if save_self:
            method_tuple = (self.is_top,self.like_cot,self.comment_cot,self.via_cot,self.content,self.weibo_id,self.submit_time,self.source,self.is_via,self.via_weibo_id,time.localtime(),author_db_id)
        else:
            method_tuple = (is_top,like_cot,comment_cot,via_cot,content,weibo_id,submit_time,source,is_via,via_weibo_id,time.localtime(),author_db_id)
        try:
            self.conn.cursor().execute(
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


    def get_author_db_id(self,user_account_id=None):
        cur = self.conn.cursor()
        if user_account_id==None:
            user_account_id = self.user_id
        cur.execute(
            'select id from user where account_id = ' + user_account_id
        )
        data = cur.fetchall()
        if data:
            return data[0][0]
        else:
            return False


    def get_db_id(self,weibo_id=None):
        cur = self.conn.cursor()
        if weibo_id==None:
            weibo_id = self.weibo_id
        cur.execute(
            'select id from weibo where weibo_id = ' + weibo_id
        )
        data = cur.fetchall()
        if data:
            return data[0][0]
        else:
            return False



if __name__=="__main__":
    print('run main ok')
    conn = pymysql.connect(
        host='localhost',   port=3306,
        user='root',        passwd='',
        db='selenium_weibo',   charset='utf8'
    )
    browser = webdriver.Chrome()
    user_account_id = '5360104594'
    access_homepage(user_account_id,browser)
    weiboEles = browser.find_elements_by_class_name('WB_feed_type')
    for weiboEle in weiboEles:
        weibo = Weibo(weiboEle,conn)
        weibo.show_in_cmd()
        if weibo.save_to_db():
            pass#email or other func
        print('\n\n')
    browser.close()
    conn.close()

