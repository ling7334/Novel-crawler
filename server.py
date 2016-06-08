#encoding:UTF-8
import usrlib
import const
import urllib
import pickle
import json
from flask import request
from flask import jsonify
from flask import Flask
from flask import send_from_directory
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    html = open('./webui/index.html',encoding='utf8').read()
    novellist = pickle.load(open('./novel/list.dat', "rb"))
    content=''
    for novelname in novellist:
        filename = './novel/' + novelname + '/info.dat'
        try:
            noveldata = pickle.load(open(filename, "rb"))
        except:
            next
        filename = './novel/' + novelname + '/chapter_name.dat'
        try:
            chapter_name = pickle.load(open(filename, "rb"))
        except:
            next
        try:
            image = noveldata['image']
        except:
            image = '/img/default.jpg'
        content += '<div class="col-md-5 well row">'
        content += '<img class="col-md-4" width="120" height="150" style="max-width: 120px; max-height: 150px;" alt="" src="' + image + '" border="0">'
        content += '<div class="col-md-8">'
        content += '<p><a href="/'+ noveldata['title'] +'/"><strong>' + noveldata['title'] + '</strong></a></p>'
        try:
            content += '<p  class="text-primary">最新章节：<a href="/'+ noveldata['title'] +'-1">' + noveldata['latest'] + '</a></p>'
        except:
            content += '<p  class="text-primary">最新章节：</p>'
        try:
            content += '<p  class="text-primary">最后阅读：<a href="/'+ noveldata['title'] +'/'+repr(noveldata['lastread'])+'/">' + chapter_name[noveldata['lastread']] + '</a></p></div></div>'
        except:
            content += '<p  class="text-primary">最后阅读：</p></div></div>'
        if novellist.index(novelname) %2==0:
            content += '<div class="col-md-2"></div>'
    html = html.replace('#novellist',content)
    return html

@app.route('/json/<novelname>/<int:chapter>')
def chapter_json(novelname,chapter):
    noveldata ={}
    novelname = urllib.parse.unquote(novelname)
    filename = './novel/' + novelname + '/chapter_name.dat'
    chapter_name = pickle.load(open(filename, "rb"))
    filename = './novel/' + novelname + '/info.dat'
    noveldata = pickle.load(open(filename, "rb"))
    chaptername=chapter_name[chapter]
    text = usrlib.Get_Chapter(novelname,chapter)
    text = usrlib.escape(text,2)
    rt = {"title": chaptername, "description": text}
    try:
        lastread = noveldata['lastread']
    except:
        lastread = -1
    if chapter >= lastread:
        noveldata['lastread'] = chapter
        filename = './novel/' + novelname + '/info.dat'
        pickle.dump(noveldata, open(filename, "wb"))
    return jsonify(rt)

@app.route('/<novelname>/')
@app.route('/<novelname>')
def Novel(novelname):
    chapterlist = ''
    noveldata = {}
    novelname = urllib.parse.unquote(novelname)
    filename = './novel/' + novelname + '/chapter_name.dat'
    try:
        chapter_name = pickle.load(open(filename, "rb"))
    except:
        return "咦，这里也没有！"
    filename = './novel/' + novelname + '/info.dat'
    try:
        noveldata = pickle.load(open(filename, "rb"))
    except:
        return "咦，这里也没有！"
    try:
        lastread = noveldata['lastread']
    except:
        lastread = -1
        
    html = open('./webui/book.html',encoding='utf8').read()
    try:
        string = noveldata['image']
    except:
        string = '/img/default.jpg'
    html = html.replace('#image',string)
    try:
        string = noveldata['description']
        string = usrlib.escape(string,1)
    except:
        string = ''
    html = html.replace('#description',string)
    try:
        string = noveldata['author']
        string = '作者：' + string + ' | '
    except:
        string = ''
    html = html.replace('#author',string)
    try:
        string = noveldata['category']
        string = '分类：' + string + ' | '
    except:
        string = ''
    html = html.replace('#category',string)
    try:
        string = noveldata['status']
        string = '状态：' + string + ' | '
    except:
        string = ''
    html = html.replace('#status',string)
    try:
        string = noveldata['update']
        string = '更新时间：' + string + ' | '
    except:
        string = ''
    html = html.replace('#update',string)
    try:
        string = noveldata['homepage']
        string = '来源：' + '<a href="' + string + '">' + string +'</a>' + ' | '
    except:
        string = ''
    html = html.replace('#resource',string)
    
    i=0
    for item in chapter_name:
        if i == lastread:
            chapterlist += '<a class="list-group-item col-lg-4" id="chapterlink" href="' + '/' + novelname + '/' + repr(i) + '">' + item + '<span class="badge">书签</span></a>'
        else:
            chapterlist += '<a class="list-group-item col-lg-4" id="chapterlist" href="' + '/' + novelname + '/' + repr(i) + '">' + item + '</a>'
        i=i+1
    html = html.replace('#novelname',novelname)
    html = html.replace('#chapterlist',chapterlist)
    return html

@app.route('/<novelname>/<int:chapter>/')
@app.route('/<novelname>/<int:chapter>')
def Chpater(novelname,chapter=None):
    continuously = 1
    noveldata = {}
    novelname = urllib.parse.unquote(novelname)
    filename = './novel/' + novelname + '/info.dat'
    try:
        noveldata = pickle.load(open(filename, "rb"))
    except:
        return "咦，这里也没有！"
    filename = './novel/' + novelname + '/chapter_name.dat'
    chapter_name = pickle.load(open(filename, "rb"))
    if chapter == -1:
        chapter= len(chapter_name)-1
    if (chapter >= 0 and chapter <= len(chapter_name)-1):
        chaptername=chapter_name[chapter]
        text = usrlib.Get_Chapter(novelname,chapter)
        text = usrlib.escape(text,2)
        html = open('./webui/chapter.html',encoding='utf8').read()
        html = html.replace('#novelname',novelname)
        html = html.replace('#chaptername',chaptername)
        html = html.replace('#NovelLink','/'+novelname+'/')
        html = html.replace('#text',text)
        html = html.replace('#chapter',repr(chapter))
        html = html.replace('#novelpage','/' + novelname + '/')
        if chapter<len(chapter_name)-1:
            html = html.replace('#next','/' + novelname + '/' + repr(chapter+1))
        else:
            html = html.replace('#next','/' + novelname + '/')
        if chapter>0:
            html = html.replace('#previous','/' + novelname + '/' + repr(chapter-1))
        else:
            html = html.replace('#previous','/' + novelname + '/')
        if continuously == 1:
            html = html.replace('#script','/js/continuously.js')
            html = html.replace('#novelname',novelname)
            html = html.replace('#chapter',repr(chapter+1))
        else:
            html = html.replace('#script','/js/pager.js')
        try:
            lastread = noveldata['lastread']
        except:
            lastread = -1
        if chapter >= lastread:
            noveldata['lastread'] = chapter
            filename = './novel/' + novelname + '/info.dat'
            pickle.dump(noveldata, open(filename, "wb"))
        return html
    else:
        return Novel(novelname)

#@app.route('/search/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def Search():
    if request.method == 'POST':
        if not 'id' in request.form:
            rt = {"id" : usrlib.Get_ID() }
            return jsonify(rt)
        #print(request.form['novelname'],request.form['id'])
        url = usrlib.Search_By_ID(request.form['novelname'],request.form['id'])
        if url == -1:
            return '-1'
        noveldata = usrlib.Get_Novel_Info(url,request.form['id'])
        if noveldata == -1:
            return '-1'
        return jsonify(noveldata)
    else:
        html = open('./webui/search.html',encoding='utf8').read()
        return html

@app.route('/retrieve', methods=['POST'])
def Retrieve():
    if not 'id' in request.form:
        return '-1'
    if  not 'novelname' in request.form:
        return '-2'
    url = usrlib.Search_By_ID(request.form['novelname'],request.form['id'])
    if url == -1:
        return '-3'
    noveldata = usrlib.Get_Novel_Info(url,request.form['id'])
    if noveldata == -1:
        return '-4'
    if not usrlib.Save_Content(noveldata):
        return '-5'
    return '0'

@app.route('/config', methods=['GET', 'POST'])
@app.route('/config/', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        return 0
    else:
        html = open('./webui/config.html',encoding='utf8').read()
        return html

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./webui/js', path)
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./webui/css', path)
@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('./webui/fonts', path)
@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('./webui/img', path)
    
if __name__ == '__main__':
    app.run(debug=True)