#coding:utf-8
"""
@file:      userClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-8-9 16:30
@description:
            用户信息类，包括爬取解析存储
"""


from selenium import webdriver
from func import access_homepage
import time,pymysql


class User:
    def __init__(self,user_account_id,conn=None,ready_browser=None):
        if conn:
            self.conn = conn
        if ready_browser:
            self.driver = ready_browser
        else:
            self.driver = access_homepage(user_account_id)
        self.account_id = user_account_id
        self.company = None
        self.school = None
        self.area = None
        self.birthday = None
        self.abstract_info = None
        self.shadow = self.driver.find_element_by_class_name('shadow')
        self.tb = self.driver.find_element_by_class_name('tb_counter').find_elements_by_tag_name('strong')
        self.parse_details()


    @property
    def username(self):
        return self.shadow.find_element_by_class_name('username').text


    @property
    def sex(self):
        try:
            self.shadow.find_element_by_class_name('icon_pf_male')
            return 1
        except:
            return 0


    @property
    def is_auth(self):
        shadow = self.shadow
        try:
            shadow.find_element_by_class_name('icon_pf_approve')
        except:
            try:
                shadow.find_element_by_class_name('icon_pf_approve_co')
            except:
                return 0
        return 1


    @property
    def auth_info(self):
        if self.is_auth:
            return self.shadow.find_element_by_class_name('pf_intro').text
        else:
            return None


    @property
    def is_vip(self):
        try:
            self.shadow.find_element_by_class_name('icon_member4')
            return 1
        except:
            return 0


    @property
    def fans_cot(self):
        return int(self.tb[1].text)


    @property
    def weibo_cot(self):
        return int(self.tb[2].text)


    @property
    def follow_cot(self):
        return int(self.tb[0].text)


    @property
    def db_id(self,account_id=None):
        if account_id==None:
            account_id = self.account_id
        self.cur.execute(
            'select id from user where account_id = ' + account_id
        )
        data = self.cur.fetchall()
        if data:
            return data[0][0]
        else:
            return False


    def show_in_cmd(self):
        print('**************用户信息**************')
        print('account_id :',self.account_id)
        print('username :',self.username)
        print('is_vip :',self.is_vip)
        print('fans_cot :',self.fans_cot)
        print('weibo_cot :',self.weibo_cot)
        print('follow_cot :',self.follow_cot)
        print('sex :',self.sex)
        print('is_auth :',self.is_auth)
        print('area :',self.area)
        print('auth_info :',self.auth_info)
        print('birthday :',self.birthday)
        print('abstract_info :',self.abstract_info)
        print('company :',self.company)
        print('school :',self.school)
        print('**************用户信息**************')


    def parse_details(self):
        details = self.driver.find_element_by_class_name('ul_detail').find_elements_by_tag_name('li')
        for detail in details:
            try:
                info = detail.text.split('\n')[1]
            except:
                continue
            if detail.text.split('\n')[0]=='2':
                self.area = info
                continue
            if info.split(' ')[0]==u'公司':
                self.company = info.split(' ')[1]
                continue
            if info.split(' ')[0]==u'毕业于':
                self.school = info.split(' ')[1]
                continue
            if u'年' in info and u'月' in info and u'日' in info:
                self.birthday = info
                continue
            if u'简介' in info:
                self.abstract_info = info.split(u'：')[1]


    def save_to_db(self):
        cur = self.conn.cursor()
        try:
            cur.execute(
                'INSERT user(account_id,username,fans_cot,follow_cot,weibo_cot,area,birthday,sex,abstract_info,is_auth,is_vip,company,school,create_time) '
                'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (self.account_id,self.username,self.fans_cot,self.follow_cot,self.weibo_cot,self.area,self.birthday,self.sex,self.abstract_info,self.is_auth,self.is_vip,self.company,self.school,time.localtime())
            )
            self.conn.commit()
            print ('User: '+self.username+' save success!')
        except Exception as e:
            print ('User save error: '+str(e))


    def destory(self):
        self.driver.close()



if __name__=="__main__":
    conn = pymysql.connect(
        host='localhost',   port=3306,
        user='root',        passwd='',
        db='selenium_weibo',   charset='utf8'
    )
    user_id_pool = ['1650246564']
    for user_id in user_id_pool:
        user = User(user_account_id=user_id,conn=conn)
        user.show_in_cmd()
        user.save_to_db()
    conn.close()
