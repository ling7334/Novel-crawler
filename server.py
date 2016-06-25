#encoding:UTF-8
import usrlib
import urllib
import pickle
import json
import os
#import re
#import shutil
from flask import request
from flask import jsonify
from flask import Flask
from flask import send_from_directory
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    noveldata={}
    html = open('./webui/index.html',encoding='utf8').read()
    #novellist = pickle.load(open('./novel/list.dat', "rb"))
    content=''

    novellist = list()
    if not os.path.isdir('./novel/'): 
        os.mkdir('./novel')
    if not os.path.isfile('./novel/list.dat'):
        pickle.dump(novellist,open('./novel/list.dat', "wb"))

    novellist = pickle.load(open('./novel/list.dat', "rb"))
    for novelname in novellist:
        try:
            noveldata = pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
        except:
            continue
        if not 'title' in noveldata:
            os.remove('./novel/' + novelname + '/info.dat')
            del novellist[novellist.index(novelname)]
            pickle.dump(novellist,open('./novel/list.dat', "wb"))
            continue
        try:
            chapter_name = pickle.load(open('./novel/' + novelname + '/chapter_name.dat', "rb"))
        except:
            del novellist[novellist.index(novelname)]
            continue
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

@app.route('/<novelname>/')
@app.route('/<novelname>', methods=['GET', 'POST'])
def Novel(novelname):
    
    chapterlist = ''
    noveldata = {}
    novelname = urllib.parse.unquote(novelname)

    try:
        noveldata = pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
    except:
        return "咦，这里也没有！"
    try:
        lastread = noveldata['lastread']
    except:
        lastread = -1
    
    if request.method == 'POST':
        return usrlib.Get_New_Chapter_List(noveldata)

    try:
        chapter_name = pickle.load(open('./novel/' + novelname + '/chapter_name.dat', "rb"))
    except:
        return "咦，这里也没有！"

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
    except:
        string = ''
    html = html.replace('#author',string)
    try:
        string = noveldata['category']
    except:
        string = ''
    html = html.replace('#category',string)
    try:
        string = noveldata['status']
    except:
        string = ''
    html = html.replace('#status',string)
    try:
        string = noveldata['update']
    except:
        string = ''
    html = html.replace('#update',string)
    try:
        string = noveldata['website']
    except:
        string = ''
    html = html.replace('#resourceid',string)
    try:
        string = noveldata['homepage']
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
@app.route('/<novelname>/<int:chapter>', methods=['GET', 'POST'])
def Chpater(novelname,chapter=None):
    if request.method == 'POST':
        noveldata ={}
        novelname = urllib.parse.unquote(novelname)

        if chapter is None:
            return '-1'
        
        chapter_name = pickle.load(open('./novel/' + novelname + '/chapter_name.dat', "rb"))
        noveldata = pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
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
            pickle.dump(noveldata, open('./novel/' + novelname + '/info.dat', "wb"))
        return jsonify(rt)
    else:
        reading_setting ={}
        try:
            reading_setting = pickle.load(open('./setting.dat', "rb"))
        except:
            reading_setting['continuously'] = 'true'
        continuously = reading_setting['continuously']
        noveldata = {}
        novelname = urllib.parse.unquote(novelname)
        try:
            noveldata = pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
        except:
            return "咦，这里也没有！"
        chapter_name = pickle.load(open('./novel/' + novelname + '/chapter_name.dat', "rb"))
        if chapter == -1:
            chapter= len(chapter_name)-1
        if (0 <= chapter <= len(chapter_name)-1):
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
            if continuously == 'true':
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
                pickle.dump(noveldata, open('./novel/' + novelname + '/info.dat', "wb"))
            return html
        else:
            return Novel(novelname)

@app.route('/search/')
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
    noveldata = {}
    #print(request.form)
    
    if not 'id' in request.form:
        return '-1'
    if  not 'novelname' in request.form:
        return '-2'
    
    url = usrlib.Search_By_ID(request.form['novelname'],request.form['id'])
    if url == -1:
        return 'Cannot_Connect'
    noveldata = usrlib.Get_Novel_Info(url,request.form['id'])
    if noveldata == -1:
        return 'Fail_Downoad_Info'

    if 'restrict' in request.form:
        if request.form['restrict']=='1' and request.form['bookmark'] == '1':
            Lnoveldata = pickle.load(open('./novel/'+request.form['novelname']+'/info.dat', "rb"))
            noveldata['lastread'] = Lnoveldata['lastread']
            if not usrlib.Save_Content(noveldata):
                return 'Fail_Save_Info'
            return 'SUCCESS'
    if os.path.isfile('./novel/'+request.form['novelname']+'/info.dat'): 
        return 'EXIST'
    if not usrlib.Save_Content(noveldata):
        return 'Fail_Save_Info'
    return 'SUCCESS'

@app.route('/del', methods=['POST'])
def delfo():
    #print(request.form)
    if not 'novelname' in request.form:
        return '-1'
    if os.path.isdir('./novel/'+request.form['novelname']): 
        os.remove('./novel/'+request.form['novelname']+'/info.dat')
        os.remove('./novel/'+request.form['novelname']+'/chapter_name.dat')
        os.remove('./novel/'+request.form['novelname']+'/chapter_link.dat')
        novellist = pickle.load(open('./novel/list.dat','rb'))
        if request.form['novelname'] in novellist:
            novellist.remove(request.form['novelname'])
            pickle.dump(novellist, open('./novel/list.dat', "wb"))
        #shutil.rmtree('./novel/'+request.form['novelname'])
        return '0'
    return '-1'

@app.route('/config/', methods=['GET', 'POST'])
@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        if 'access' in request.form:
            setting = {}
            if request.form['access'] == 'getsetting':
                try:
                    config = open('./config.ini',encoding='utf8').read()
                    setting = pickle.load(open('./setting.dat', "rb"))
                    setting['config'] = config
                except:
                    setting['continuously']= 'true'
                    setting['bold']= 'false'
                    setting['fontcolor'] = "black"
                    setting['bkcolor'] = "#f5f5f5"
                    setting['fontfamily'] = "微软雅黑"
                    setting['fontsize'] = "30px"
                    setting['config'] = ''
                return jsonify(setting)
            elif request.form['access'] == 'savesetting':
                setting['continuously'] = request.form['continuously']
                setting['bold'] = request.form['bold']
                setting['fontcolor'] = request.form['fontcolor']
                setting['bkcolor'] = request.form['bkcolor']
                setting['fontfamily'] = request.form['fontfamily']
                setting['fontsize'] = request.form['fontsize']
                css='body{position: relative; padding-top: 70px; padding-bottom: 30px;} #text{font-weight: $bold; background: $bkcolor; color: $fontcolor; font-family: $fontfamily; font-size: $fontsize;}'
                if request.form['bold']=='true':
                    css = css.replace("$bold",'bold')
                else:
                    css = css.replace("$bold",'')
                css = css.replace("$fontcolor",setting['fontcolor'])
                css = css.replace("$bkcolor",setting['bkcolor'])
                css = css.replace("$fontfamily",setting['fontfamily'])
                css = css.replace("$fontsize",setting['fontsize'])
                fo = open("./webui/css/custom_theme.css", "wb")
                fo.write(css.encode('utf8'))
                fo.close()
                pickle.dump(setting, open('./setting.dat', "wb"))
                return '0'
            elif request.form['access'] == 'saveconfig':
                string = urllib.parse.unquote(request.form['config'])
                #print (string)
                fo = open("./config.ini", "wb")
                fo.write(string.encode('utf8'))
                fo.close()
                return '0'
        return '-1'
    else:
        html = open('./webui/config.html',encoding='utf8').read()
        return html

@app.route('/favicon.ico')
def send_ico():
    return send_from_directory('./webui/', 'favicon.ico')
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
    PORT = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0',port=PORT, debug=True)
