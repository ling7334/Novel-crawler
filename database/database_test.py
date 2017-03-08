import os
import redis
import unittest
import contextlib

from database.connection import redis_instance, mysql_instance, postgresql_instance

def unsetenv(key):
    if hasattr(os, 'unsetenv'):
        os.unsetenv(key)
    else:
        os.putenv(key, '')

class TestRedis(unittest.TestCase):
    """Redis测试实例"""

    def setUp(self):
        self.r = redis_instance


    def tearDown(self):
        pass

    def test_redis(self):
        """Redis测试实例"""
        unsetenv("REDIS_URL")
        unsetenv("REDIS_PORT")
        self.assertTrue(isinstance(self.r(0), redis.StrictRedis))
        os.environ["REDIS_URL"] = "localhost"
        os.environ["REDIS_PORT"] = "6379"
        self.assertTrue(isinstance(self.r(0), redis.StrictRedis))
        unsetenv("REDIS_URL")
        unsetenv("REDIS_PORT")

class TestMYSQL(unittest.TestCase):
    """MYSQL测试实例"""
    def setUp(self):
        self.mysql = mysql_instance

    def tearDown(self):
        pass

    def test_mysql(self):
        """MYSQL测试实例"""
        unsetenv("MYSQL_URL")
        unsetenv("MYSQL_PORT")
        unsetenv("MYSQL_USER")
        unsetenv("MYSQL_PWD")
        self.assertTrue(isinstance(self.mysql(), contextlib.closing))
        os.environ["MYSQL_URL"] = "127.0.0.1"
        os.environ["MYSQL_PORT"] = "3306"
        os.environ["MYSQL_USER"] = "root"
        os.environ["MYSQL_PWD"] = ""
        self.assertTrue(isinstance(self.mysql(), contextlib.closing))
        unsetenv("MYSQL_URL")
        unsetenv("MYSQL_PORT")
        unsetenv("MYSQL_USER")
        unsetenv("MYSQL_PWD")

class TestPostgre(unittest.TestCase):
    """PostgreSQL测试实例"""
    def setUp(self):
        self.postgresql = postgresql_instance

    def tearDown(self):
        pass

    def test_mysql(self):
        """PostgreSQL测试实例"""
        unsetenv("POSTGRE_HOST")
        unsetenv("POSTGRE_PORT")
        unsetenv("POSTGRE_USER")
        unsetenv("POSTGRE_PWD")
        self.assertTrue(isinstance(self.postgresql(), contextlib.closing))
        os.environ["POSTGRE_HOST"] = "127.0.0.1"
        os.environ["POSTGRE_PORT"] = "5432"
        os.environ["POSTGRE_USER"] = "postgres"
        os.environ["POSTGRE_PWD"] = ""
        self.assertTrue(isinstance(self.postgresql("travis_ci_test"), contextlib.closing))
        unsetenv("POSTGRE_URL")
        unsetenv("POSTGRE_PORT")
        unsetenv("POSTGRE_USER")
        unsetenv("POSTGRE_PWD")
        os.environ["POSTGRE_URL"] = "postgres://postgres@127.0.0.1:5432/travis_ci_test"
        self.assertTrue(isinstance(self.postgresql(), contextlib.closing))
        unsetenv("POSTGRE_URL")
