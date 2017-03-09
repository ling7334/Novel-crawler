#encoding:UTF-8
#import re
#import shutil
import json
import usrlib
import pickle
import threading
from urllib.parse import unquote
from os import (path,mkdir,remove,getenv)
from flask import (request,jsonify,Flask,send_from_directory,render_template)

app = Flask(__name__)

@app.route('/')
def index():
    noveldata={}
    html = open('./webui/index.html',encoding='utf8').read()
    #novellist = pickle.load(open('./novel/list.dat', "rb"))
    content=''

    novellist = list()
    if not path.isdir('./novel/'): 
        mkdir('./novel')
    if not path.isfile('./novel/list.dat'):
        pickle.dump(novellist,open('./novel/list.dat', "wb"))

    novellist = pickle.load(open('./novel/list.dat', "rb"))
    for novelname in novellist:
        try:
            noveldata = pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
        except:
            continue
        if not 'title' in noveldata:
            remove('./novel/' + novelname + '/info.dat')
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
            content += '<p  class="text-primary">最新章节：<a href="/'+ noveldata['title'] +'/'+ repr(len(chapter_name)-1) +'">' + noveldata['latest'] + '</a></p>'
        except:
            content += '<p  class="text-primary">最新章节：</p>'
        try:
            content += '<p  class="text-primary">最后阅读：<a href="/'+ noveldata['title'] +'/'+repr(noveldata['lastread'])+'/">' + chapter_name[noveldata['lastread']] + '</a></p></div></div>'
        except:
            content += '<p  class="text-primary">最后阅读：</p></div></div>'
        if novellist.index(novelname) %2==0:                #分列排布
            content += '<div class="col-md-2"></div>'
    html = html.replace('#novellist',content)
    return html

@app.route('/<novelname>/')
@app.route('/<novelname>', methods=['GET', 'POST'])
def Novel(novelname):
    
    chapterlist = ''
    noveldata = {}
    novelname = unquote(novelname)

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
            chapterlist += '<a class="list-group-item col-lg-4" id="chapterlink" href="' + '/' + novelname + '/' + repr(i) + '">' + item + '</a>'
        i=i+1
    html = html.replace('#novelname',novelname)
    html = html.replace('#chapterlist',chapterlist)
    return html

@app.route('/<novelname>/<int:chapter>/')
@app.route('/<novelname>/<int:chapter>', methods=['GET', 'POST'])
def Chpater(novelname,chapter=None):
    noveldata ={}
    novelname = unquote(novelname)
    try:
        noveldata = pickle.load(open('./novel/' + novelname + '/info.dat', "rb"))
        chapter_name = pickle.load(open('./novel/' + novelname + '/chapter_name.dat', "rb"))
    except:
        return "咦，这里也没有！"

    if request.method == 'POST':

        if chapter is None:
            return '-1'

        text = usrlib.Get_Chapter(novelname,chapter)
        if  text == '未找到章节信息！':
            return json.dumps({"status":"404","message":text})
        elif text == '未找到章节！':
            return json.dumps({"status":"404","message":text})
        text = usrlib.escape(text,2)
        #rt = {"title": chapter_name[chapter], "description": text}
        try:
            lastread = noveldata['lastread']
        except:
            lastread = -1
        if chapter >= lastread:
            noveldata['lastread'] = chapter
            pickle.dump(noveldata, open('./novel/' + novelname + '/info.dat', "wb"))
        return json.dumps({"status":"OK","title": chapter_name[chapter], "description": text})
    else:
        reading_setting ={}
        try:
            reading_setting = pickle.load(open('./setting.dat', "rb"))
        except:
            reading_setting['continuously'] = 'true'
        continuously = reading_setting['continuously']

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
            rt = {"error" : request.form['id'] + ' 无法连接，请检查设置或网站。' }
            return jsonify(rt)
        elif url == -2:
            rt = {"error" : request.form['id'] + ' 没有搜索到小说。' }
            return jsonify(rt)
        noveldata = usrlib.Get_Novel_Info(url,request.form['id'])
        if noveldata == -1:
            rt = {"error" : request.form['id'] + ' 获取小说错误，请重试。' }
            return jsonify(rt)
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
        if request.form['restrict']=='1':
            local_noveldata = pickle.load(open('./novel/'+request.form['novelname']+'/info.dat', "rb"))
            if 'lastread' in local_noveldata:
                noveldata['lastread'] = local_noveldata['lastread']
            if not usrlib.Save_Content(noveldata):
                return 'Fail_Save_Info'
            return 'SUCCESS'
        else:
            if not usrlib.Save_Content(noveldata):
                return 'Fail_Save_Info'
            return 'SUCCESS'
    if path.isfile('./novel/'+request.form['novelname']+'/info.dat'): 
        return 'EXIST'
    if not usrlib.Save_Content(noveldata):
        return 'Fail_Save_Info'
    return 'SUCCESS'

@app.route('/del', methods=['POST'])
def delfo():
    #print(request.form)
    if not 'novelname' in request.form:
        return '-1'
    if path.isdir('./novel/'+request.form['novelname']): 
        remove('./novel/'+request.form['novelname']+'/info.dat')
        remove('./novel/'+request.form['novelname']+'/chapter_name.dat')
        remove('./novel/'+request.form['novelname']+'/chapter_link.dat')
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
                    setting = pickle.load(open('./setting.dat', "rb"))
                except:
                    setting['continuously']= 'true'
                    setting['bold']= 'false'
                    setting['fontcolor'] = "black"
                    setting['bkcolor'] = "#f5f5f5"
                    setting['fontfamily'] = "微软雅黑"
                    setting['fontsize'] = "19px"
                try:
                    setting['config'] = open('./config.ini',encoding='utf8').read()
                except:
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
                string = unquote(request.form['config'])
                #print (string)
                fo = open("./config.ini", "wb")
                fo.write(string.encode('utf8'))
                fo.close()
                return '0'
        return '-1'
    else:
        html = open('./webui/config.html',encoding='utf8').read()
        return html

@app.route('/bookcase')
def send_ico():
    return render_template('bookcase.html')

# @app.errorhandler(404) 
# def page_not_found(error):
#     return render_template("404.html")
# @app.errorhandler(500) 
# def server_error(error):
#     return render_template("500.html")

if __name__ == '__main__':
    PORT = int(getenv('PORT', 5000))
    app.run(host='0.0.0.0',port=PORT, threaded=True, debug=False)
