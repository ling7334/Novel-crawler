import json
from os import getenv
from flask import request, Flask,send_from_directory, render_template, abort

from database.connection import postgresql_instance

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    with postgresql_instance('novel') as con:
        with con, con.cursor() as cur:
            pass
    return render_template('bookcase.html', novellist=[])

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/book/<novelname>', methods=['GET'])
def book(novelname):
    chapter = request.args.get('chapter')
    print(chapter)
    if chapter:
        with postgresql_instance('novel') as con:
            with con, con.cursor() as cur:
                len = cur.execute("""SELECT public.chapter.name,content FROM public.chapter INNER JOIN public.novel ON novelid=public.novel.id WHERE public.novel.name = %s AND public.chapter.chapter = %s;""", (novelname, chapter))
                if not len: abort(404)
                chaptername, text = cur.fetchone()
        return render_template('chapter.html', novelname=novelname, chaptername=chaptername, text=text)
    with postgresql_instance('novel') as con:
        with con, con.cursor() as cur:
            len = cur.execute("""SELECT id,name,image,description,author,category,status,update_time,resource,resourcehref FROM public.novel WHERE name=%s;""", (novelname,))
            if not len: abort(404)
            novel = {}
            novelid, novel['name'], novel['image'], novel['description'], novel['author'], novel['category'], novel['status'], novel['update'], novel['resource'], novel['resourcehref'] = cur.fetchone()
            cur.execute("""SELECT chapter,name,bookmark FROM public.chapter WHERE novelid=%s;""", (novelid,))
            chapters = map(lambda x: zip(('id', 'name', 'bookmark'), x), list(cur.fetchall()))
    return render_template('book.html', novel=novel, chapters=chapters)

@app.route('/favicon.ico')
def ico():
    return send_from_directory('static','img/favicon.ico')

@app.errorhandler(404) 
def page_not_found(error):
    return render_template("404.html"), 404
@app.errorhandler(500) 
def server_error(error):
    return render_template("500.html"), 500

if __name__ == '__main__':
    PORT = int(getenv('PORT', 5000))
    app.run(host='0.0.0.0',port=PORT, threaded=True, debug=True)
