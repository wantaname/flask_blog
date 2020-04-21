""""
简单登录
"""
from flask import Blueprint, request
from db import database_conn
import pymysql

from mytoken import create_token
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['POST'])
def login():
    # 获取请求体
    params = request.json#type:dict

    username=params.get('username')
    password=params.get('password')

    # 检查数据库
    try:
        conn = database_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        sql = 'select * from user where username="{}" and password="{}"'.format(username,password)
        cursor.execute(sql)

        res = cursor.fetchone()

        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        return {
            'status': 400,
            'msg':'系统错误'
        }

    # 成功
    if res:
        token = create_token(username=username)
        return {
            'status':200,
            'token':token,
            'msg':'登录成功'
        }
    else:
        return {
            'status': 300,

            'msg': '账号或密码错误！'
        }