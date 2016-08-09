#coding:utf-8
__author__ = 'Administrator'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from mytools.emailClass import Email
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
import time,random

class SeleniumWeiboCatch(Thread):
    def __init__(self,X=0,width=500,user=None):
        Thread.__init__(self)
        if user:
            delta = user['index']*width
            height = 500
        else:
            #没写user时是单纯为捕获图片
            delta = 0
            width = 800
            height = 800
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(height=height,width=width)
        self.driver.set_window_position(y=0,x=X+delta)
        self.user = user

    def run(self):
        print(self.user['id']+': '+'已分配得到线程')
        self.load_info_first()
        while(1):
            info = []
            while(1):
                info = self.catch_info()
                if info:
                   break
            if info[0][:2]=='置顶':
                latest_tweet = info[1]
            else:
                latest_tweet = info[0]
            if latest_tweet!=self.user['buffer']:
                self.new_weibo_action(latest_tweet)
            else:
                try:
                    print (self.user['id']+': '+'Same!BACK and NEW both is: '+latest_tweet)
                except:
                    print (self.user['id']+': '+'Same!BACK and NEW both is:_____ Sorry,Encoding Error!____')
            time.sleep(random.randint(2,4))

    def load_info_first(self):
        print(self.user['id']+': '+'正在初始化信息')
        while(1):
            if self.user['buffer']:
                break
            else:
                print(self.user['id']+': '+'正在尝试加载该用户信息')
                try:
                    info = self.catch_info()
                    if info[0][:2]=='置顶':
                        self.user['buffer'] = info[1]
                    else:
                        self.user['buffer'] = info[0]
                except:
                    print(self.user['id']+': '+'重新初始化')
                    time.sleep(random.randint(1,4))
        print(self.user['id']+': '+'首次初始化完成')


    def new_weibo_action(self,latest_tweet):
        print(self.user['id']+': '+'查到新微博!')
        print (self.user['id']+': '+'BACK:'+self.user['buffer'])
        print (self.user['id']+': '+'NEW:'+latest_tweet)
        self.user['buffer'] = latest_tweet
        spider2 = SeleniumWeiboCatch(user=self.user)
        save_name = spider2.get_homepage_screenshot()
        spider2.tearDown()
        subject = self.user['id']+'发新微博了!'
        content = latest_tweet
        content += '\nplease check in http://weibo.com/u/'+ self.user['id'] + '?is_all=1'
        self.send_mail(subject,content,save_name)


    def login(self,username,password):
        browser = self.driver
        browser.get("http://weibo.com/login.php")
        time.sleep(1)
        browser.maximize_window()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[1]/div/a[2]').click()
        username_input = browser.find_element_by_xpath('//*[@id="loginname"]')
        username_input.send_keys(username)
        password_input = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        print('login success')


    def catch_info(self):
        info = []
        browser = self.driver
        while(1):
            browser.get("http://weibo.com/u/"+ self.user['id'] +"?is_all=1")
            try:
                if WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="Pl_Official_MyProfileFeed__24"]/div'))
                ):
                    break
            except:
                print(self.user['id']+': '+'网页加载异常,重复访问...')
        weibo_list = browser.find_elements_by_class_name('WB_cardwrap')
        for weibo in weibo_list:
            content = weibo.find_elements_by_class_name('WB_text')
            if len(content)==1:
                info.append(self.parse_original_weibo(weibo))
            elif len(content)==2:
                info.append(self.parse_transmit_weibo(weibo))
            else:
                pass
        return info

    def parse_original_weibo(self,weiboEle):
        content = weiboEle.find_element_by_class_name('WB_text').text
        return content

    def parse_transmit_weibo(self,weiboEle):
        content = weiboEle.find_elements_by_class_name('WB_text')[0].text
        return content

    def send_mail(self,subject,content,img_src):
        local_time = time.strftime("%H:%M:%S  %Y-%m-%d",time.localtime(time.time()))
        emailAI = Email(
            receiver='965606089@qq.com',
            sender='luyangaini@vip.qq.com',
            host = 'smtp.qq.com',
            port = 587,
            subject=subject+local_time,
            content=content,
            img_src=img_src,
        )
        emailAI.conn_server()
        emailAI.login(username='luyangaini@vip.qq.com',password='ptpkfdscqjkfbehe')
        emailAI.send()
        emailAI.close()


    def get_homepage_screenshot(self):
        userID = self.user['id']
        while(1):
            self.driver.get("http://weibo.com/u/"+ userID +"?is_all=1")
            self.driver.set_window_size(height=1050,width=1000)
            try:
                if WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="Pl_Official_MyProfileFeed__24"]/div'))
                ):
                    break
            except:
                print(self.user['id']+': '+'网页加载异常,重复访问...')
        ele = self.driver.find_element_by_xpath('//*[@id="plc_main"]')
        ele.location_once_scrolled_into_view
        local_time = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
        name = 'Screenshots/'+local_time+'by'+userID+'.png'
        try:
            self.driver.save_screenshot(name)
            print(self.user['id']+': '+'图片保存成功，文件名为'+name)
        except:
            print(self.user['id']+': '+'图片保存失败')
        return name

    def tearDown(self):
        self.driver.close()



