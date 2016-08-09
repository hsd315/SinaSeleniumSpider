#coding:utf-8
import smtplib,time
from email.mime.text import MIMEText  
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Email(object):
    def __init__(self,sender,receiver,subject,content,
                 host=None,port=0,subtype='plain',img_src=None):
        self.msg = MIMEMultipart('mixed')
        msgText = MIMEText(content,_subtype=subtype,_charset='utf-8')
        self.msg.attach(msgText)
        if img_src:
            fp = open(img_src,'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID','<meinv_image.png>')
            self.msg.attach(msgImage)
        self.msg['Subject'] = Header(subject, 'utf-8')
        self.msg['From'] = sender
        self.msg['To'] = receiver
        self.sender = sender
        self.receiver = receiver
        self.host = host
        self.port = port
        self.smtp = smtplib.SMTP()
    
    def conn_server(self,host='',port=0):
        #连接服务器,并启动tls服务
        if self.host is '' and self.port is 0:
            self.host = host
            self.port = port
        try:
            self.smtp.connect(self.host,self.port)
            self.smtp.starttls() 
        except Exception as e:
            print('conn_server():',e)
                
    def login(self,username,password):
        try:
            self.smtp.login(username, password)
            log_string = username+'登陆成功'+'\n'
            print(log_string)
        except Exception as e:
            print('login():',e)
    
    def send(self):
        try:
            self.smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
            log_string = '邮件已投至'+self.receiver+'\n'
            print(log_string)
        except Exception as e:
            print('send():',e)
    
    def close(self):
        self.smtp.close()
