#coding:utf-8

class File(object):
    def __init__(self,repo_str,mode_str):
        self.repo = repo_str
        self.mode = mode_str
        self.open()
        
    def open(self):
        try:
            self.subject = open(self.repo,self.mode)
        except Exception as e:
            print(e)
        
    def write(self,content):
        try:
            self.subject.write(content)
        except Exception as e:
            print(e)
    
    def read(self):
        pass
    
    def close(self):
        #相当于保存
        self.subject.close()