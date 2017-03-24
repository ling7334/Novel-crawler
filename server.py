import json
from os import getenv
from flask import request, Flask,send_from_directory, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bookcase.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/book/<novelname>')
def book(novelname):
    chapter = request.args.get('chapter')
    if chapter:
        #TODO: 从数据库读出小说章节信息
        return render_template('chapter.html', novelname=novelname, chaptername=None, text=None)
    #TODO: 从数据库读出小说信息及章节信息
    return render_template('book.html', novel=None, chapters=None)

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
    app.run(host='0.0.0.0',port=PORT, threaded=True, debug=False)
