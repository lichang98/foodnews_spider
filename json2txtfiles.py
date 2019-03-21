# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:35:40 2019

将爬取的json数据按照标记保存为文本文件

@author: 李畅
"""
import json
import sys

if __name__=='__main__':
    for i in range(1,len(sys.argv)):
        with open(sys.argv[i],encoding='utf-8',mode='r') as fr:
            for line in fr.readlines():
                if line.find('title')==-1 or line.find('content')==-1:
                    continue
                else:
                    title=line[line.find('title')+7:line.find('content')-3]
                    with open('news_'+title.replace('\\','').replace('/','').
                              replace('?','').replace('*','').replace('<','').
                              replace('>','').replace('|','').replace('"','').
                              replace('“','').replace('”','').
                              replace('\'','').replace('‘','').
                                     replace('’','').replace('.','_')+'.txt',encoding='utf-8',
                              mode='w') as fw:
                        content=line[line.find('content')+9:-4]
                        if content.find(',') !=-1:
                            lst=content.split(',')
                        else:
                            lst=[content]
                        lst=[item.replace('[','').replace('\'','').replace(']','').
                             replace('"','') for item in lst]
                        for item in lst:
                            print(item,file=fw)

