#encoding:UTF-8
import os
import urllib
import urllib.request
import configparser
import pickle
from threading import Thread
from bs4 import BeautifulSoup

class RetrieveNovel:
    """该类包含一系列方法用以获取小说
    """
    identity = list()
    latest = list()
    link = list()
    chapter_name = list()
    chapter_link = list()
    
    noveldata = {}
    
    config = configparser.ConfigParser()
    
    
    def __init__(self):
        self.config.read('./config.ini')                                                #载入网站设置
        
    
    def search(self,novelname):
        """从config中规定的网站查找小说。
        novelname：小说名
        """
        __searchdata = {}

        #--------------------------------------------------搜索引擎找小说
        for item in self.config.sections():
            self.opts = self.config[item]
            __searchdata[self.opts['keyword']] = novelname                              #构建搜索关键词
            href = urllib.parse.urlencode(__searchdata, encoding='GBK')                 #关键词URL编码
            full_url = self.opts["slink"] + href                                        #构建搜索链接
            try:
                data=urllib.request.urlopen(full_url).read()                            #读取搜索页面内容
            except:
                continue                                                                #网站无法连接
            soup = BeautifulSoup(data,"html.parser")                                    #构建BS数据
            string = 'soup.' + self.opts["novel_link"]
            href = eval(string)                                                         #获取小说链接
            full_url = self.opts["url"] + href                                          #构建小说页面链接
            try:
                data = urllib.request.urlopen(full_url).read()                          #读取小说页面内容
            except:
                continue                                                                #小说页面无法连接
            #--------------------------------------------------记录有效网站
            self.identity.append(item)                                                  
            string = 'soup.' + self.opts['slatest']
            string = eval(string)
            self.latest.append(string)
            string = 'soup.' + self.opts['novel_link']
            string = eval(string)
            if not string.startswith('http'):
                string = self.opts["url"] + string                                      #link为绝对路径
            self.link.append(string)
        return self.identity,self.latest,self.link

    def Get_novel_info(self,url):
        """根据之前的搜索内容，获取小说信息
        """
        #url = self.link[self.identity.index(id)]
        try:
            data = urllib.request.urlopen(url).read()                       #读取小说页面内容
        except:
            return None                                                     #小说页面无法连接
        soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
        #--------------------------------------------------抓取小说信息
        self.noveldata['homepage'] = self.opts['url']
        self.noveldata['infolink'] = url
        self.noveldata['id'] = self.opts['id']
        
        string = 'soup.'+self.opts['title']
        self.noveldata['title'] = eval(string)
        
        try:
            string = 'soup.'+self.opts['content_link']
            string = eval(string)
            if not string.startswith('http'):
                string = self.noveldata['homepage'] + string
            self.noveldata['content_link'] = eval(string)
        except:
            pass
            
        try:
            string = 'soup.'+self.opts['description']
            self.noveldata['description'] = eval(string)
        except:
            pass
            
        try:
            string = 'soup.'+self.opts['category']
            self.noveldata['category'] = eval(string)
        except:
            pass
            
        try:
            string = 'soup.'+self.opts['author']
            self.noveldata['author'] = eval(string)
        except:
            pass
            
        try:
            string = 'soup.'+self.opts['status']
            self.noveldata['status'] = eval(string)
        except:
            pass
            
        try:
            string = 'soup.'+self.opts['update']
            self.noveldata['update'] = eval(string)
        except:
            pass
            
        try:
            string = 'soup.'+self.opts['latest']
            self.noveldata['latest'] = eval(string)
        except:
            pass
            
        try:
            string = 'soup.'+self.opts['image']
            
        except:
            pass
        string = eval(string)
        if not string.startswith('http'):
            string = self.noveldata['homepage'] + string
        self.noveldata['image'] = string
        
        #--------------------------------------------------创建小说文件夹
        filename = './novel/' + self.noveldata['title'] + '/'
        if not os.path.exists(filename):
            os.makedirs(filename)
        #--------------------------------------------------写入小说信息
        filename = './novel/' + self.noveldata['title'] + '/' + 'info.dat'
        pickle.dump(self.noveldata, open(filename, "wb"))
        #--------------------------------------------------写入小说列表
        filename = './novel/' + 'list.dat'
        novel_list = list()
        for item in os.listdir('./novel/'): 
            if os.path.isfile('./novel/'+item+'info.dat'): 
                novel_list.append(item)
        pickle.dump(novel_list, open(filename, "wb"))
        
        return self.noveldata
    
    def Get_content(self,url,start=0,end=-1):
        """从指定网站下载小说
        url：小说目录页URL
        start：下载起始章节
        end：下载结束章节
        """
        try:
            data = urllib.request.urlopen(url).read()                       #读取目录页面内容
        except:
            return False                                                    #目录页面无法连接
        soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
        #--------------------------------------------------抓取小说章节列表
        string = 'soup.'+self.opts['chapter_list']
        for chapter_list in eval(string):
            string = eval(self.opts['chapter_name'])
            string = str(string)
            self.chapter_name.append(string)
            url = eval(self.opts['chapter_link'])
            if  not url.startswith('http'):
                url = self.opts['url'] + eval(self.opts['chapter_link'])
            self.chapter_link.append(url)
        #--------------------------------------------------创建小说文件夹
        filename = './novel/' + self.noveldata['title'] + '/'
        if not os.path.exists(filename):
            os.makedirs(filename)
        #--------------------------------------------------写入小说信息
        
        filename = './novel/' + self.noveldata['title'] + '/info.dat'
        pickle.dump(self.noveldata, open(filename, "wb"))
        #--------------------------------------------------写入小说列表
        filename = './novel/list.dat'
        novel_list = list()
        for item in os.listdir('./novel/'): 
            if os.path.isfile('./novel/'+item+'/info.dat'): 
                novel_list.append(item)
        pickle.dump(novel_list, open(filename, "wb"))

        #--------------------------------------------------写入小说目录
        filename = './novel/' + self.noveldata['title'] + '/chapter_name.dat'
        pickle.dump(self.chapter_name, open(filename, "wb"))
        filename = './novel/' + self.noveldata['title'] + '/chapter_link.dat'
        pickle.dump(self.chapter_link, open(filename, "wb"))
        #--------------------------------------------------写入小说章节
        if end == -1:
            end = len(self.chapter_link)
        for i in range(start,end):
            data=urllib.request.urlopen(self.chapter_link[i]).read()            #读取章节内容
            soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
            text = eval('soup.'+self.opts['text'])
            filename = './novel/' + self.noveldata['title'] + '/' + repr(i) + '.txt'
            fo = open(filename, "wb")
            fo.write(text.encode('utf8'))
            fo.close()
        return True

def Get_ID():
    ID = list()
    config = configparser.ConfigParser()
    config.read('./config.ini')
    for item in config.sections():
        ID.append(item)
    return ID

def Search_By_ID(novelname,id):
    config = configparser.ConfigParser()
    config.read('./config.ini')
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
    url = eval(string)                                                          #获取小说页面链接
    if not url.startswith('http'):
        url = opts["url"] + url                                                 #构建小说页面链接
    # try:
    #     data = urllib.request.urlopen(url).read()                               #读取小说信息页面内容
    # except:
    #     return -1                                                               #小说信息页面无法连接
    return url

def Get_Novel_Info(url,id):
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
    """从指定网站下载章节列表
    noveldata:小说元数据
    start：下载起始章节
    end：下载结束章节
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
    filename = './novel/' + noveldata['title'] + '/'
    if not os.path.exists(filename):
        os.makedirs(filename)
    #--------------------------------------------------写入小说信息
    
    filename = './novel/' + noveldata['title'] + '/info.dat'
    pickle.dump(noveldata, open(filename, "wb"))
    #--------------------------------------------------写入小说列表
    filename = './novel/list.dat'
    novel_list = list()
    for item in os.listdir('./novel/'): 
        if os.path.isfile('./novel/'+item+'/info.dat'): 
            novel_list.append(item)
    pickle.dump(novel_list, open(filename, "wb"))

    #--------------------------------------------------写入小说目录
    filename = './novel/' + noveldata['title'] + '/chapter_name.dat'
    pickle.dump(chapter_name, open(filename, "wb"))
    filename = './novel/' + noveldata['title'] + '/chapter_link.dat'
    pickle.dump(chapter_link, open(filename, "wb"))
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
        #print("未找到该小说")
        return None
        
def Load_Chapter_List(novelname):
    chapter_name = list()
    filename = './novel/' + novelname + '/chapter_name.dat'
    #filename1 = './novel/' + novelname + '/chapter_link.dat'
    try:
        chapter_name = pickle.load(open(filename, "rb"))
        #chapter_link = pickle.load(open(filename1, "rb"))
        return chapter_name#, chapter_link
    except:
        print("未找到章节列表")
        return None

def Get_chapters(id,chapter_link,index,end=-1):
    config = configparser.ConfigParser()
    config.read('./config.ini')
    opts = config[id]
    if end == -1:
        end = len(chapter_link)
    for i in range(index,end):
        filename = './novel/' + novelname + repr(i) + '.txt'
        data=urllib.request.urlopen(chapter_link[i]).read()                 #读取章节内容
        soup = BeautifulSoup(data,"html.parser")                            #构建BS数据
        text = eval('soup.'+ opts['text'])
        fo = open(filename, "wb")
        fo.write(text.encode('utf8'))
        fo.close()
        return True

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
    config.read('./config.ini')                                         #载入网站设置
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