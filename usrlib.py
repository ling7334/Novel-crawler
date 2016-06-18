#encoding:UTF-8
import os
import urllib
import urllib.request
import configparser
import pickle
from flask import jsonify
#from threading import Thread
from bs4 import BeautifulSoup


def Get_ID():
    '''获取搜索网站设置的ID列表'''
    ID = list()
    config = configparser.ConfigParser()
    config.read('./config.ini',encoding='utf8')
    for item in config.sections():
        ID.append(item)
    return ID

def Search_By_ID(novelname,id):
    '''获取小说信息（目录）页
    novelname：小说名
    id：网站设置ID
    '''
    config = configparser.ConfigParser()
    config.read('./config.ini',encoding='utf8')
    opts = config[id]
    __searchdata = {}
    __searchdata[opts['keyword']] = novelname	                                #构建搜索关键词
    url =opts["slink"] + urllib.parse.urlencode(__searchdata, encoding='GBK')   #关键词URL编码
    try:
        data=urllib.request.urlopen(url).read()                                 #读取搜索页面内容
    except:
        return -1                                                               #网站无法连接
    soup = BeautifulSoup(data,"html.parser")                                    #构建BS数据
    string = 'soup.' + opts["novel_link"]
    try:
        url = eval(string)                                                          #获取小说页面链接
    except:
        return -1
    if not url.startswith('http'):
        url = opts["url"] + url                                                 #构建小说页面链接
    # try:
    #     data = urllib.request.urlopen(url).read()                               #读取小说信息页面内容
    # except:
    #     return -1                                                               #小说信息页面无法连接
    return url

def Get_Novel_Info(url,id):
    '''获取小说信息
    url：小说信息（目录）页
    id：网站ID'''
    config = configparser.ConfigParser()
    config.read('./config.ini',encoding='utf8')
    opts = config[id]
    noveldata = {}
    try:
        data = urllib.request.urlopen(url).read()                       #读取小说页面内容
    except:
        return -1                                                       #小说页面无法连接
    soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
    #--------------------------------------------------抓取小说信息
    noveldata['homepage'] = opts['url']
    noveldata['infolink'] = url
    noveldata['id'] = opts['id']
    noveldata['website'] = opts['name']
    
    string = 'soup.'+ opts['title']
    noveldata['title'] = eval(string)
    
    try:
        string = 'soup.'+opts['content_link']
        string = eval(string)
        if not string.startswith('http'):
            string = noveldata['homepage'] + string
        noveldata['content_link'] = eval(string)
    except:
        pass
        
    try:
        string = 'soup.'+opts['description']
        noveldata['description'] = eval(string)
    except:
        pass
        
    try:
        string = 'soup.'+opts['category']
        noveldata['category'] = eval(string)
    except:
        pass
        
    try:
        string = 'soup.'+opts['author']
        noveldata['author'] = eval(string)
    except:
        pass
        
    try:
        string = 'soup.'+opts['status']
        noveldata['status'] = eval(string)
    except:
        pass
        
    try:
        string = 'soup.'+opts['update']
        noveldata['update'] = eval(string)
    except:
        pass
        
    try:
        string = 'soup.'+opts['latest']
        noveldata['latest'] = eval(string)
    except:
        pass
        
    try:
        string = 'soup.'+opts['image']
        
    except:
        pass
    string = eval(string)
    if not string.startswith('http'):
        string = noveldata['homepage'] + string
    noveldata['image'] = string
    
    # #--------------------------------------------------创建小说文件夹
    # filename = './novel/' + noveldata['title'] + '/'
    # if not os.path.exists(filename):
    #     os.makedirs(filename)
    # #--------------------------------------------------写入小说信息
    # filename = './novel/' + noveldata['title'] + '/' + 'info.dat'
    # pickle.dump(noveldata, open(filename, "wb"))
    # #--------------------------------------------------写入小说列表
    # filename = './novel/' + 'list.dat'
    # novel_list = list()
    # for item in os.listdir('./novel/'): 
    #     if os.path.isfile('./novel/'+item+'info.dat'): 
    #         novel_list.append(item)
    # pickle.dump(novel_list, open(filename, "wb"))
    
    return noveldata

def Save_Content(noveldata):
    """从预定网站下载章节列表
    noveldata:小说信息字典
    """
    chapter_name=[]
    chapter_link=[]

    config = configparser.ConfigParser()
    config.read('./config.ini',encoding='utf8')
    opts = config[noveldata['id']]

    if 'content_link' in noveldata:
        url = noveldata['content_link']
    else:
        url = noveldata['infolink']
    try:
        data = urllib.request.urlopen(url).read()                       #读取目录页面内容
    except:
        return -1                                                       #目录页面无法连接
    soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
    #--------------------------------------------------抓取小说章节列表
    string = 'soup.'+opts['chapter_list']
    for chapter_list in eval(string):
        string = eval(opts['chapter_name'])
        string = str(string)
        chapter_name.append(string)
        url = eval(opts['chapter_link'])
        if  not url.startswith('http'):
            url = opts['url'] + eval(opts['chapter_link'])
        chapter_link.append(url)
    #--------------------------------------------------创建小说文件夹
    if not os.path.exists('./novel/' + noveldata['title'] + '/'):
        os.makedirs('./novel/' + noveldata['title'] + '/')
    #--------------------------------------------------写入小说信息

    pickle.dump(noveldata, open('./novel/' + noveldata['title'] + '/info.dat', "wb"))
    #--------------------------------------------------写入小说列表
    novel_list = list()
    for item in os.listdir('./novel/'): 
        if os.path.isfile('./novel/'+item+'/info.dat'): 
            novel_list.append(item)
    pickle.dump(novel_list, open('./novel/list.dat', "wb"))

    #--------------------------------------------------写入小说目录
    pickle.dump(chapter_name, open('./novel/' + noveldata['title'] + '/chapter_name.dat', "wb"))
    pickle.dump(chapter_link, open('./novel/' + noveldata['title'] + '/chapter_link.dat', "wb"))
    #--------------------------------------------------写入小说章节
    # if end == -1:
    #     end = len(self.chapter_link)
    # for i in range(start,end):
    #     data=urllib.request.urlopen(self.chapter_link[i]).read()            #读取章节内容
    #     soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
    #     text = eval('soup.'+self.opts['text'])
    #     filename = './novel/' + self.noveldata['title'] + '/' + repr(i) + '.txt'
    #     fo = open(filename, "wb")
    #     fo.write(text.encode('utf8'))
    #     fo.close()
    return True

def Get_New_Chapter_List(noveldata):
    '''从预定网页更新章节列表
    noveldata：小说信息字典'''
    Dnoveldata ={}
    chapter_name=[]
    chapter_link=[]
    Dchapter_name =[]
    rt=[]

    if 'content_link' in noveldata:
        url = noveldata['content_link']
    else:
        url = noveldata['infolink']
    Dnoveldata = Get_Novel_Info(url,noveldata['id'])
    if Dnoveldata == -1:
            return '-1'
    if Dnoveldata['latest'] == noveldata['latest']:
        return '0'

    config = configparser.ConfigParser()
    config.read('./config.ini',encoding='utf8')
    opts = config[noveldata['id']]
    chapter_name = pickle.load(open('./novel/' + noveldata['title'] + '/chapter_name.dat', "rb"))
    try:
        data = urllib.request.urlopen(url).read()                       #读取目录页面内容
    except:
        return '-1'                                                       #目录页面无法连接
    soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
    #--------------------------------------------------抓取小说章节列表
    string = 'soup.'+opts['chapter_list']
    for chapter_list in eval(string):
        string = eval(opts['chapter_name'])
        string = str(string)
        Dchapter_name.append(string)
        url = eval(opts['chapter_link'])
        if  not url.startswith('http'):
            url = opts['url'] + eval(opts['chapter_link'])
        chapter_link.append(url)
    for chapter in Dchapter_name:
        if not chapter in chapter_name:
            rt.append({"index": Dchapter_name.index(chapter), "name": chapter})
    Dnoveldata['lastread'] = noveldata['lastread']
    pickle.dump(Dnoveldata, open('./novel/' + noveldata['title'] + '/info.dat', "wb"))
    #--------------------------------------------------写入小说目录
    pickle.dump(Dchapter_name, open('./novel/' + noveldata['title'] + '/chapter_name.dat', "wb"))
    pickle.dump(chapter_link, open('./novel/' + noveldata['title'] + '/chapter_link.dat', "wb"))
    t = {"list": rt}
    return jsonify(t)



def escape(txt,space):
    '''将txt文本中的空格、&、<、>、（"）、（'）转化成对应的的字符实体，以方便在html上显示'''
    txt = txt.replace('&','&amp;')
    txt = txt.replace(' ','&nbsp;')
    txt = txt.replace('<','&lt;')
    txt = txt.replace('>','&gt;')
    txt = txt.replace('"','&quot;')
    txt = txt.replace('\'','&apos;')
    txt = txt.replace('\r',space*'<br />')
    txt = txt.replace('\n',space*'<br />')
    return txt

def Load_Novel_List():
    '''载入小说列表'''
    try:
        return pickle.load(open('./novel/list.dat', "rb"))
    except:
        print("小说列表未创建")
        return None
    
def Load_Novel_Data(novelname):
    '''载入小说信息
    novelname：小说名
    '''
    try:
        return pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
    except:
        print("未找到该小说")
        return None
        
def Load_Chapter_List(novelname):
    '''载入小说章节列表
    novelname：小说名'''
    try:
        return pickle.load(open('./novel/' + novelname + '/chapter_name.dat', "rb"))#, chapter_link = pickle.load(open('./novel/' + novelname + '/chapter_link.dat', "rb"))
    except:
        print("未找到章节列表")
        return None

def Load_Chapter(novelname,index):
    '''载入本地章节内容
    novelname：小说名
    index：章节标志位
    '''
    if os.path.isfile('./novel/' + novelname + '/' + repr(index) + '.txt'):
        return open('./novel/' + novelname + '/' + repr(index) + '.txt',encoding='utf8').read()
    else:
        return -1

def Search_Chapter(novelname,index):
    '''从预定网站下载指定章节
    novelname：小说名
    index：章节标志位
    '''
    noveldata = {}
    chapter_link = []
    try:
        noveldata = pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
        chapter_link = pickle.load(open('./novel/' + novelname + '/chapter_link.dat', "rb"))
    except:
        return -1
    
    config = configparser.ConfigParser()
    config.read('./config.ini',encoding='utf8')                                         #载入网站设置
    config = config[noveldata['id']]
    
    try:
        data=urllib.request.urlopen(chapter_link[index]).read()         #读取章节内容
    except:
        return -2
    soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
    text = eval('soup.'+ config['text'])
    return text

def Get_Chapter(novelname,index):
    '''尝试从本地与网站载入章节
    novelname：小说名
    index：章节标志位
    '''
    text = Load_Chapter(novelname,index)
    if text == -1:
        text = Search_Chapter(novelname,index)
        if text == -1:
            return '未找到章节信息！'
        elif text == -2:
            return '未找到章节！'
        else:
            open('./novel/' + novelname + '/' + repr(index) + '.txt', "wb").write(text.encode('utf8'))
    return text