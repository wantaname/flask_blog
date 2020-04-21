"""
采用连接池优化性能
"""

import pymysql

# from DBUtils.PooledDB import PooledDB
#
# pool = PooledDB(
#     creator=pymysql,  # 使用链接数据库的模块
#     maxconnections=None,  # 连接池允许的最大连接数，0和None表示不限制连接数
#     mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
#     maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
#     maxshared=3,
#     maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
#     setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
#
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     password='981011yzp',
#     database='mysite',
#     charset='utf8',
#     autocommit=True,
# )

host = '127.0.0.1'
port = 3306
user = ''
password = ''
database = 'myblog'
charset = 'utf8'



# 连接数据库
def database_conn():
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset=charset,
        autocommit=True,
    )
    return conn
