#encoding:UTF-8

import os
import sys
import urllib
import urllib.request
import re
import usrlib
import codecs
import pickle


novelname = "贩罪"

_Pattern = {}
_searchdata = {}
_noveldata = {}

Identity = list()
Chapter_link = list()
Chapter_name = list()

#--------------------------------------------------载入网站列表
Identity = usrlib.LoadID()
#--------------------------------------------------载入网站模式
_Pattern = usrlib.LoadPattern(Identity[0])
#--------------------------------------------------确定搜索集
_searchdata[_Pattern["keyword"]] = novelname
#--------------------------------------------------确定字符集
_Charset = usrlib.URL_GetCharset(_Pattern["url"])
_noveldata['charset']=_Charset
#--------------------------------------------------搜索引擎找小说
url_values=urllib.parse.urlencode(_searchdata, encoding=_Charset)
full_url=_Pattern["slink"] + url_values
data=urllib.request.urlopen(full_url).read()
data=data.decode(_Charset)
#--------------------------------------------------提取小说地址
pattern = re.compile(_Pattern["novel_link"],re.S)
items = re.findall(pattern,data)
#--------------------------------------------------提取小说目录页面
full_url = _Pattern["url"]+items[0]
data=urllib.request.urlopen(full_url).read()
data=data.decode(_Charset)
_noveldata['link'] = full_url
#--------------------------------------------------获取小说标题
pattern = re.compile(_Pattern["title"],re.S)
Title = re.findall(pattern,data)
_noveldata['title'] = Title[0]
#--------------------------------------------------获取小说简介
pattern = re.compile(_Pattern["description"],re.S)
Description = re.findall(pattern,data)
_noveldata['description'] = Description[0]
#--------------------------------------------------获取小说类型
pattern = re.compile(_Pattern["category"],re.S)
Category = re.findall(pattern,data)
_noveldata['category'] = Category[0]
#--------------------------------------------------获取小说作者
pattern = re.compile(_Pattern["author"],re.S)
Author = re.findall(pattern,data)
_noveldata['author'] = Author[0]
#--------------------------------------------------获取小说更新状态
pattern = re.compile(_Pattern["status"],re.S)
Status = re.findall(pattern,data)
_noveldata['status'] = Status[0]
#--------------------------------------------------获取小说更新时间
pattern = re.compile(_Pattern["update_time"],re.S)
Update_time = re.findall(pattern,data)
_noveldata['update'] = Update_time[0]
#--------------------------------------------------获取小说最新章
pattern = re.compile(_Pattern["latest_chapter_name"],re.S)
Latest_chapter_name = re.findall(pattern,data)
_noveldata['latest'] = Latest_chapter_name[0]
#--------------------------------------------------获取小说封面
pattern = re.compile(_Pattern["image"],re.S)
Image = re.findall(pattern,data)
_noveldata['image'] = Image[0]
#--------------------------------------------------获取小说目录列表
pattern = re.compile(_Pattern["chapter_list"],re.S)
Chapter_list = re.findall(pattern,data)
Chapter_list = Chapter_list[0].split(_Pattern["chapter_split"])
for i in Chapter_list:
    data=i.split('">')
    Chapter_link.append(data[0])
    Chapter_name.append(data[1])



#--------------------------------------------------创建小说文件夹
filename = 'novel/' + Title[0] + '/'
if not os.path.exists(filename):
    os.makedirs(filename)
#--------------------------------------------------创建小说信息
filename = 'novel/' + Title[0] + '/' + 'info.dat'
fo = open(filename, "wb")
pickle.dump(_noveldata, fo, True)
fo.close()
#--------------------------------------------------创建小说目录
filename = 'novel/' + Title[0] + '/' + 'list.txt'
fo = open(filename, "w")
for i in Chapter_name:
    fo.write(i)
    fo.write('\n')
fo.close()

DownChapnum = 10
#--------------------------------------------------获取小说章节
for i in range(DownChapnum):
    full_url=_Pattern["url"] + Chapter_link[i]
    data=urllib.request.urlopen(full_url).read()
    data=data.decode(_Charset)
    pattern = re.compile(_Pattern["text"],re.S)
    Text = re.findall(pattern,data)
    Text = Text[0]
#--------------------------------------------------写入文件
    filename = 'novel/' + Title[0] + '/' + str(i) + '.txt'
    fo = open(filename, "w")
    fo.write(Text)
    fo.close()
