import sys
import urllib
import urllib.request
import re

def LoadID():
    """从libaray文件夹下的list.txt文件中导入网站Identity。返回列表。
    """
    result = list()
    
    f = open('libaray/list.txt','r')

    for line in open('libaray/list.txt'):
        line = f.readline()
        result.append(line)
    f.close()
    return result

def LoadPattern(Identity):
    """载入指定网站Identity的网站数据模式。返回字典。
    filename：网站Identity。
    """
    Pattern={}
    
    fo = open("libaray/"+Identity+".txt", "r", encoding='utf8')
    data=fo.read()
    fo.close()
    
    raw=data.split("\n")
    for item in raw:
        data=item.split("=",1)
        Pattern[data[0]]=data[1]
    return Pattern

def URL_GetCharset(url):
    """从指定url获取字符集。返回字符串，如无连接返回-1，不包含字符集的返回空值。
    """
    try:
        data = urllib.request.urlopen(url).read()
    except:
        return -1
    else:
        return GetCharset(data)

def GetCharset(data):
    """获取网页内容的字符集。返回字符串，不包含字符集的返回空值。
    data：网页源代码。
    """
    pattern = re.compile(b'content="text/html; charset=(.*?)"',re.S)
    items = re.findall(pattern,data)
    #仅返回第一个找到的字符集定义
    return items[0].decode("utf-8")