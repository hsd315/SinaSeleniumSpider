#coding:utf-8
__author__ = 'Administrator'

from SpidersHandler import SpidersHandler


if __name__=='__main__':
    user_list = ['277772655','5360104594','5842071290']

    file = open('record.txt')

    spiders = SpidersHandler(user_list,file)

    spiders.run()
