#coding:utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time,datetime

def access_homepage(user_account_id,browser=None):
    if not browser:
        browser = webdriver.Chrome()
    userHomeLink = 'http://weibo.com/u/'+ user_account_id + '?is_all=1'
    browser.set_window_size(
        width=1000,height=800
    )
    while(1):
        print ('Homepage_url: '+userHomeLink)
        try:
            browser.get(userHomeLink)
            if WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'WB_frame'))
            ):
                if browser.find_elements_by_class_name('tb_counter') and browser.find_elements_by_class_name('ul_detail'):
                    print(user_account_id+': '+'homepage加载正常,尝试获取用户信息...')
                    break
                else:
                    print('元素显示不正常，重复访问...')
        except:
            print(user_account_id+': '+'homepage加载异常,重复访问...')
            time.sleep(3)


def time_str_convert_list(time_str):
    #time_str形如2016-08-06 19:26:01
    #转为[2016, 8, 6, 19, 26, 1]
    date = time_str.split(' ')[0]
    time = time_str.split(' ')[1]
    time_info_list = date.split('-')
    time_info_list.extend(time.split(':'))
    return time_info_list


def public_parse(weiboEle):
    ret = {'content':None,'submit_time':None,'source':None}
    ret['content'] = weiboEle.find_element_by_class_name('WB_text').text
    wb_from_div = weiboEle.find_element_by_class_name('WB_from')
    submit_time = wb_from_div.find_element_by_tag_name('a').get_attribute('title')
    time_info_list = time_str_convert_list(time_str=submit_time)
    time_info_list = map(lambda x:int(x),time_info_list)
    ret['submit_time'] = datetime.datetime(*time_info_list)
    wb_from = wb_from_div.text
    if u'来自' in wb_from:
        ret['source'] = wb_from.split('来自 ')[-1]
    return ret