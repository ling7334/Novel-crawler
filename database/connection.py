# Copyright (c) 2017 by ling7334. All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
获取数据库连接
通过config.ini文件配置要访问的数据库

Copyright (C) 2017 ling7334. All Rights Reserved.
"""
import os

def postgresql_instance(db=None):
    '''
    访问config.ini配置文件或系统环境变量中定义的PostgreSQL数据库，
    返回一个contextlib.closing类，
    使用时配合With语句使用，使用结束后，隐式地执行了文件句柄的关闭。
    contextlib是为了加强with语句，提供上下文机制的模块，它是通过Generator实现的。
    例:\n
        with postgresql_instance() as con:
            with con as cur:
                cur.execute()
    '''
    import contextlib
    import psycopg2
    try:
        postgre_url = os.environ['POSTGRE_URL']
        return contextlib.closing(psycopg2.connect(postgre_url))
    except KeyError:
        try:
            postgre_host = os.environ['POSTGRE_HOST']
            postgre_port = os.environ['POSTGRE_PORT']
            postgre_user = os.environ['POSTGRE_USER']
            postgre_pwd = os.environ['POSTGRE_PWD']
        except KeyError:
            import configparser
            config = configparser.ConfigParser()
            config.read("config.ini")

            postgre_host = config.get("postgre", "host")
            postgre_port = int(config.get("postgre", "port"))
            postgre_user = config.get("postgre", "user")
            postgre_pwd = config.get("postgre", "pwd")
        if db is None:
            db = postgre_user
        if postgre_pwd:
            return contextlib.closing(psycopg2.connect(host=postgre_host, port=postgre_port, user=postgre_user, password=postgre_pwd, dbname=db))
        return contextlib.closing(psycopg2.connect(host=postgre_host, port=postgre_port, user=postgre_user, dbname=db))

def redis_instance(db=0):
    '''
    访问config.ini配置文件或系统环境变量中定义的redis数据库，
    返回该连接的句柄
    '''
    import redis
    try:
        redis_host = os.environ['REDIS_URL']
        redis_port = int(os.environ['REDIS_PORT'])
    except KeyError:
        import configparser
        config = configparser.ConfigParser()
        config.read("config.ini")

        redis_host = config.get("redis", "host")
        redis_port = int(config.get("redis", "port"))
    return redis.StrictRedis(host=redis_host, port=redis_port, db=db)

def mysql_instance(db=None):
    '''
    访问config.ini配置文件或系统环境变量中定义的MYSQL数据库，
    返回一个contextlib.closing类，
    使用时配合With语句使用，使用结束后，隐式地执行了文件句柄的关闭。
    contextlib是为了加强with语句，提供上下文机制的模块，它是通过Generator实现的。
    例:\n
        with mysql_instance() as con:
            with con as cur:
                cur.execute()
    '''
    import contextlib
    import pymysql
    try:
        mysql_host = os.environ['MYSQL_URL']
        mysql_port = int(os.environ['MYSQL_PORT'])
        mysql_user = os.environ['MYSQL_USER']
        mysql_pwd = os.environ['MYSQL_PWD']
    except KeyError:
        import configparser
        config = configparser.ConfigParser()
        config.read("config.ini")

        mysql_host = config.get("mysql", "host")
        mysql_port = int(config.get("mysql", "port"))
        mysql_user = config.get("mysql", "user")
        mysql_pwd = config.get("mysql", "pwd")
    if mysql_pwd:
        return contextlib.closing(pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_pwd, db=db, charset='utf8'))
    return contextlib.closing(pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, db=db, charset='utf8'))
