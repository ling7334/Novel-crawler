#encoding:UTF-8
#import re
#import shutil
import json
import pickle
import threading
from urllib.parse import unquote
from os import path,mkdir,remove,getenv
from flask import request,jsonify,Flask,send_from_directory,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bookcase.html')

@app.route('/favicon.ico')
def ico():
    return send_from_directory('static','img/favicon.ico')

@app.errorhandler(404) 
def page_not_found(error):
    return render_template("404.html"), 404
# @app.errorhandler(500) 
# def server_error(error):
#     return render_template("500.html"), 500

if __name__ == '__main__':
    PORT = int(getenv('PORT', 5000))
    app.run(host='0.0.0.0',port=PORT, threaded=True, debug=False)
