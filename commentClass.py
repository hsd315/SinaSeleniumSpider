#coding:utf-8



class Comment(object):
    def __init__(self,weiboID,authorID,content):
        self.id = ''
        self.content = content
        self.authorID = authorID
        self.weiboID = weiboID
        
    def save_to_database(self,db):
        pass
        