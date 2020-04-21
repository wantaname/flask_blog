""""
写博客api，登录模块暂时搁置
"""
from flask import Blueprint
from db import database_conn
import pymysql
from mytoken import login_required

bp = Blueprint('timeline', __name__, url_prefix='/timeline')



"""
获取博客信息
请求：GET
返回：{status:200,msg:'',blog:{id,title,date}}
+ 404 未登录
+ 300 自定义错误
+ 200 获取成功
"""
@bp.route('/getTimeline', methods=['GET'])
@login_required
def getTimeline():

    # 数据库操作
    try:
        #连接
        conn = database_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #sql
        sql = """
        select id,title,date from blogs
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        # 关闭
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        return {
            'status': 300,
            'msg': '获取数据失败！'
        }
    if not data:
        data=[]
    for i in range(0, len(data)):
        data[i]['date'] = data[i]['date'].strftime("%Y-%m-%d")
    return {
        'status': 200,
        'blog': data
    }

