import json
from os import getenv

from flask import Flask, abort, render_template, request, send_from_directory

from database.connection import postgresql_instance

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    '''主页书架'''
    with postgresql_instance('novel') as con:
        with con, con.cursor() as cur:
            cur.execute("""SELECT id,name,image FROM public.novel;""")
            novellist = [dict(zip('id', 'name', 'image', x)) for x in cur.fetchall()]
            for i, novel in enumerate(novellist):
                cur.execute("""SELECT serial,name FROM public.chapter WHERE novelid=%s AND bookmark=1;""", (novel['id']))
                novellist[i]['lastread']['id'], novellist[i]['lastread']['name'] = cur.fetchone()
                cur.execute("""SELECT serial,name FROM public.chapter WHERE novelid=%s AND serial=max(serial);""", (novel['id']))
                novellist[i]['latest']['id'], novellist[i]['latest']['name'] = cur.fetchone()
    return render_template('bookcase.html', novellist=novellist)


@app.route('/search', methods=['GET'])
def search():
    '''搜索页'''
    return render_template('search.html')


@app.route('/book/<novelname>', methods=['GET'])
def book(novelname):
    '''小说章节目录'''
    # 获取章节ID，如果存在则渲染章节页
    chapter = request.args.get('chapter')
    if chapter:
        with postgresql_instance('novel') as con:
            with con, con.cursor() as cur:
                length = cur.execute("""SELECT public.chapter.name,content FROM public.chapter INNER JOIN public.novel ON novelid=public.novel.id WHERE public.novel.name = %s AND public.chapter.chapter = %s;""", (novelname, chapter))
                if not length:
                    abort(404)
                chaptername, text = cur.fetchone()
        return render_template('chapter.html', novelname=novelname, chaptername=chaptername, text=text)
    # 如果不存在，则渲染目录页
    with postgresql_instance('novel') as con:
        with con, con.cursor() as cur:
            length = cur.execute(
                """SELECT id,name,image,description,author,category,status,update_time,resource,resourcehref FROM public.novel WHERE name=%s;""", (novelname,))
            if not length:
                abort(404)
            novel = {}
            novelid, novel['name'], novel['image'], novel['description'], novel['author'], novel['category'], novel['status'], novel['update'], novel['resource'], novel['resourcehref'] = cur.fetchone()
            cur.execute("""SELECT chapter,name,bookmark FROM public.chapter WHERE novelid=%s;""", (novelid,))
            chapters = [dict(zip(('id', 'name', 'bookmark'), x)) for x in cur.fetchall()]
    return render_template('book.html', novel=novel, chapters=chapters)


@app.route('/favicon.ico')
def ico():
    '''网站图标'''
    return send_from_directory('static', 'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(error):
    '''404错误'''
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    '''500错误'''
    return render_template("500.html"), 500


if __name__ == '__main__':
    PORT = int(getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)
