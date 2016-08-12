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
    def __init__(self,user_account_id,conn=None):
        if conn:
            self.conn = conn
        self.driver = webdriver.Chrome()
        self.account_id = user_account_id
        self.username = ''
        self.sex = None
        self.area = None
        self.is_auth = None
        self.auth_info = None
        self.is_vip = None
        self.birthday = None
        self.abstract_info = None
        self.company = None
        self.school = None
        self.fans_cot = None
        self.weibo_cot = None
        self.follow_cot = None
        self.create_time = None
        self.homepageParse()
        self.tear_down()

    def show_in_cmd(self):
        print('**************用户信息**************')
        print('account_id :\t\t'+self.account_id)
        print('username :\t\t'+self.username)
        print('is_vip :\t\t'+str(self.is_vip))
        print('fans_cot :\t\t'+str(self.fans_cot))
        print('weibo_cot :\t\t'+str(self.weibo_cot))
        print('follow_cot :\t\t'+str(self.follow_cot))
        print('sex :\t\t\t'+str(self.sex))
        print('is_auth :\t'+str(self.is_auth))
        if self.area:
            print('area :\t\t\t'+self.area)
        if self.auth_info:
            print('auth_info :\t'+self.auth_info)
        if self.birthday:
            print('birthday :\t\t'+self.birthday)
        if self.abstract_info:
            print('abstract_info :\t\t'+self.abstract_info)
        if self.company:
            print('company :\t\t'+self.company)
        if self.school:
            print('school :\t\t'+self.school)
        print('**************用户信息**************')

    
    def homepageParse(self):
        access_homepage(self.account_id,self.driver)
        self.parse_basics()
        self.parse_details()


    def parse_details(self):
        details = self.driver.find_element_by_class_name('ul_detail').find_elements_by_tag_name('li')
        for detail in details:
            info = detail.text.split('\n')[1]
            #print (info)
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


    def parse_basics(self):
        self.username = self.driver.find_element_by_class_name('username').text
        tb = self.driver.find_element_by_class_name('tb_counter').find_elements_by_tag_name('strong')
        self.follow_cot = int(tb[0].text)
        self.fans_cot = int(tb[1].text)
        self.weibo_cot = int(tb[2].text)
        shadow = self.driver.find_element_by_class_name('shadow')
        try:
            shadow.find_element_by_class_name('icon_pf_male')
            self.sex = 1
        except:
            self.sex = 0
        try:
            shadow.find_element_by_class_name('icon_member4')
            self.is_vip = 1
        except:
            self.is_vip = 0
        try:
            shadow.find_element_by_class_name('icon_pf_approve')
            self.is_auth = 1
            self.auth_info = shadow.find_element_by_class_name('pf_intro').text
        except:
            try:
                shadow.find_element_by_class_name('icon_pf_approve_co')
                self.is_auth = 1
                self.auth_info = shadow.find_element_by_class_name('pf_intro').text
            except:
                self.is_auth = 0
                self.abstract_info = shadow.find_element_by_class_name('pf_intro').text


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


    def get_db_id(self,account_id=None):
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


    def tear_down(self):
        self.driver.close()



if __name__=="__main__":
    conn = pymysql.connect(
        host='localhost',   port=3306,
        user='root',        passwd='',
        db='selenium_weibo',   charset='utf8'
    )
    user_id_pool = ['1401880315','277772655','5360104594','5842071290']
    for user_id in user_id_pool:
        user = User(user_account_id=user_id,conn=conn)
        user.show_in_cmd()
        user.save_to_db()
    conn.close()
