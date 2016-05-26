#encoding:UTF-8

import os
import sys
import urllib
import urllib.request
import re
import usrlib
from usrlib import RetrieveNovel
import codecs
import pickle
import configparser
from bs4 import BeautifulSoup


novelname = '12亿武装女仆的皇帝'#input('请输入小说名：')

identity = list()
link = list()
latest = list()

noveldata = {}

novel = RetrieveNovel()
identity,latest,link = novel.search(novelname)
noveldata = novel.Get_novel_info(link[0])
try:
    url = noveldata['content_link']
except:
    url = noveldata['infolink']
novel.Get_content(url,0,10)
