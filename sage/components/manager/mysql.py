import logging

import pymysql
from dbutils.pooled_db import PooledDB

from sage.complex.config.inventory import MysqlSettings


class MySQLManager:
    """MySQL 连接管理器（带连接池）"""

    _pool = None

    @classmethod
    def initialize_pool(cls):
        """初始化连接池"""
        if cls._pool is None:
            cls._pool = PooledDB(
                creator=pymysql,
                maxconnections=10,
                mincached=2,
                maxcached=5,
                blocking=True,
                ping=1,
                host=MysqlSettings.HOST,
                port=MysqlSettings.PORT,
                user=MysqlSettings.USER,
                password=MysqlSettings.PASSWORD,
                database=MysqlSettings.DB,
                autocommit=False,
            )

    def __init__(self):
        self.__class__.initialize_pool()
        self.conn = self.__class__._pool.connection()
        self.cur = self.conn.cursor()

    def __enter__(self):
        """支持 with 语法"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭"""
        self.close()

    def close(self):
        """释放资源"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    # ----------------- 通用方法 -----------------

    def query(self, sql, params=None):
        """执行查询"""
        try:
            self.cur.execute(sql, params)
            return self.cur.fetchall()
        except Exception as e:
            logging.error(f"Query error: {e}, sql={sql}")
            return None

    def execute(self, sql, params=None):
        """执行单条 SQL"""
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Execute error: {e}, sql={sql}")
            return 0

    def executemany(self, sql, data_list):
        """批量执行 SQL"""
        try:
            self.cur.executemany(sql, data_list)
            self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Executemany error: {e}, sql={sql}")
            return 0
