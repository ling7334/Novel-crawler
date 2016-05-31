#encoding:UTF-8
import usrlib
import const
import urllib
from flask import Flask
from flask import send_from_directory

app = Flask(__name__)

@app.route('/<novelname>/<int:chapter>')
def ReadText(novelname,chapter=None):
    novelname = urllib.parse.unquote(novelname)
    chapter_name, chapter_link = usrlib.Load_Chapter_List(novelname)
    chaptername=chapter_name[chapter]
    text = usrlib.Load_Chapter(novelname,chapter)
    text = usrlib.escape(text)
    html = open('./webui/chapter.html',encoding='utf8').read()
    html = html.replace('#novelname',novelname)
    html = html.replace('#chaptername',chaptername)
    html = html.replace('#text',text)
    html = html.replace('#pager',const.pager)
    html = html.replace('#script',const.script_pager)
    html = html.replace('#next','/' + novelname + '/' + repr(chapter+1))
    html = html.replace('#previous','/' + novelname + '/' + repr(chapter-1))
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

    
if __name__ == '__main__':
    app.run()