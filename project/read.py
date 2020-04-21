""""
写博客api，登录模块暂时搁置
"""
from flask import Blueprint, request,g

from db import database_conn
import pymysql

bp = Blueprint('read', __name__, url_prefix='/read')



"""
获取博客信息
请求：GET
参数：{id:博客id,from:来源,draft或者blog}
返回：{status:200,msg:'',blog:{id,title,date,content,category}}
+ 404 未登录
+ 300 自定义错误
+ 200 获取成功
"""
@bp.route('/getBlog', methods=['GET'])
def getBlog():
    #获取参数
    _id=int(request.args.get('id'))
    _from=request.args.get('from')


    if _from=='blog':
        # 数据库操作
        try:
            #连接
            conn = database_conn()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            #sql
            sql = """
            select * from blogs WHERE id={}
            """.format(_id)
            cursor.execute(sql)
            data = cursor.fetchone()
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
            return {
                'status':300,
                'msg':"文章不存在"
            }

        blog= {
            'id':data['id'],
            'title':data['title'],
            'date':data['date'].strftime("%Y-%m-%d"),
            'content':data['content'],

        }
        return {
            'status': 200,
            'blog': blog
        }
    else:
        return {
            'status': 300,
            'msg': '请求错误！'
        }
