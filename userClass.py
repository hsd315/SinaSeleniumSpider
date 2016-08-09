#coding:utf-8
import requests
from bs4 import BeautifulSoup
from mytools.stringHandleByMyself import stripWithParamString
import time

class User(object):
    def __init__(self,user_account_id,headers):
        self.userHomePageLink = 'http://weibo.cn/' + user_account_id
        self.userInfoLink =  self.userHomePageLink + '/info'
        self.account_id = user_account_id
        self.username = ''
        self.sex = 1
        self.area = ''
        self.authentication = None
        self.birthday = None
        self.abstract_info = None
        self.tag_list = []
        self.tag_string = ''
        self.daren_info = None
        self.fans_cot = 888888
        self.weibo_cot = 888888
        self.focus_cot = -1
        self.headers = headers
        response = requests.get(url=self.userInfoLink,headers=self.headers)
        self.soup = BeautifulSoup(response.text)
        self.detailParseCoreRun()
        self.homepageParseCoreRun()
        
    def show_in_cmd(self):
        print('**************用户信息**************')
        print('account_id :\t\t',self.account_id)
        print('fans_cot :\t\t',self.fans_cot)
        print('weibo_cot :\t\t',self.weibo_cot)
        print('focus_cot :\t\t',self.focus_cot)
        print('head_pic_url :\t\t',self.head_pic_url)
        print('username :\t\t',self.username)
        print('sex :\t\t\t',self.sex)
        print('area :\t\t\t',self.area)
        print('authentication :\t',self.authentication)
        print('birthday :\t\t',self.birthday)
        print('abstract_info :\t\t',self.abstract_info)
        print('tag_string :\t\t',self.tag_string)
        print('tag_list :\t\t',self.tag_list)
        print('daren_info :\t\t',self.daren_info)
        print('**************用户信息**************')
        
    @property
    def head_pic_url(self):
        head_pic = self.soup.find('img')
        url = head_pic['src']
        return url
    
    def homepageParseCoreRun(self):
        hpurl = self.userHomePageLink
        response = requests.get(url=hpurl,headers=self.headers)
        soup = BeautifulSoup(response.text)
        #得到发的微博数目
        try:
            weibo_cot_string = soup.select('.tc')[0].text
            weibo_cot_string = stripWithParamString(weibo_cot_string, '微博[')
            weibo_cot_string = weibo_cot_string[:-1]
            self.weibo_cot = int(weibo_cot_string)
            #得到关注数和被关注数
            a_list = soup.select('.tip2')[0].select('a')
            focus_cot_string = a_list[0].text
            fans_cot_string = a_list[1].text
            focus_cot_string = stripWithParamString(focus_cot_string, '关注[')
            focus_cot_string = focus_cot_string[:-1]
            self.focus_cot = int(focus_cot_string)
            fans_cot_string = stripWithParamString(fans_cot_string, '粉丝[')
            fans_cot_string = fans_cot_string[:-1]
            self.fans_cot = int(fans_cot_string)
        except:
            print(soup)
                
    def detailParseCoreRun(self):
        detail_list = self.soup.select('.c')
        try:
            tag_href_list = detail_list[2].select('a')
            tag_href_list = tag_href_list[:-1]
            for tag_href in tag_href_list:
                tag = {}
                tag['tag_name'] = tag_href.text
                tag['url'] = 'http://weibo.cn/' + str(tag_href['href'])
                self.tag_list.append(tag)
                self.tag_string += (str(tag['tag_name'])+',')
            match_string = str(detail_list[2])
            match_string = stripWithParamString(match_string, '<div class="c">')
            match_string = match_string[:-10]
            detail_list = match_string.split('<br/>')
            def set_name(name):
                self.username = name
            def set_sex(sex):
                if sex=='女':
                    self.sex = 0
            def set_area(area):
                self.area = area
            def set_abstract_info(abstract_info):
                self.abstract_info = abstract_info
            def set_authentication(authentication):
                self.authentication = authentication
            def set_birthday(birthday):
                self.birthday = birthday
            def set_daren_info(daren_info):
                self.daren_info = daren_info    
            def void_func(arg):
                pass
            def set_tag(tag):
                pass
                
            str_vs_func_dict = {
                        '昵称':       set_name,
                        '认证':       set_authentication,
                        '性别':       set_sex,
                        '地区':       set_area,
                        '简介':       set_abstract_info,
                        '生日':       set_birthday,
                        '标签':       set_tag,
                        '达人':       set_daren_info,
                    }
            
            for info in detail_list:
                try:
                    key_value = info.split(':')
                    func = str_vs_func_dict[key_value[0]]
                    func(key_value[1])
                except:
                    pass
                    #print('Exception:',info,'match failed')
        except Exception as e:
            print(e)
            print('ERROR:detail_list:',detail_list)
                    
    def save_to_db(self,dbObj):
        if self.weibo_cot == 888888:
            print('weibo_cot = 888888')
            return
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #保存用户数据
        try:
            dbObj.cur.execute(
                "insert into user_copy(create_time,account_id,area,username,sex,authentication,birthday,abstract_info,tag,head_pic_url,fans_cot,weibo_cot,focus_cot)"
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (now,self.account_id,self.area,self.username,self.sex,self.authentication,self.birthday,self.abstract_info,self.tag_string,self.head_pic_url,self.fans_cot,self.weibo_cot,self.focus_cot)
            )
            dbObj.conn.commit()
            self.show_in_cmd()
        except Exception as e:
            print(e)
        #保存标签数据    
        for tag in self.tag_list:
            try:
                dbObj.cur.execute(
                  "insert into tag(url,tag_name)"
                  "values (%s,%s)",
                  (tag['url'],tag['tag_name'])
                              )
                dbObj.conn.commit()
            except Exception as e:
                print(e)
