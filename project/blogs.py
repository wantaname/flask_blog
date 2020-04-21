"""
文章列表API
"""

from flask import Blueprint, request,g
import os,re
from db import database_conn
import pymysql
from config import baseDir

bp = Blueprint('blogs', __name__, url_prefix='/blogs')
from mytoken import login_required
'''
获取全部分类
'''
@bp.route('/getCategorys', methods=['GET'])
@login_required
def getCategorys():
    #获取参数

    # 数据库操作
    try:
        #连接
        conn = database_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #sql
        sql = """
        select * from category
        """
        cursor.execute(sql)
        categorys = cursor.fetchall()
        # 关闭
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        return {
            'status': 300,
            'msg': '获取分类失败！'
        }

    return {
        'status': 200,
        'categorys': categorys
    }

"""
获取所有博客
请求：GET
参数:pagenum,pagesize
返回：{status:0,blogs:[{id:,title:,date:,category:}],total:,}
"""
@bp.route('/getBlogs', methods=['GET'])
@login_required
def getBlogs():
    #获取参数
    pagenum=request.args.get('pagenum')
    pagesize=request.args.get('pagesize')
    category=request.args.get('category')

    if category=='全部':
        # sql
        sql = """
        select id,title,`date`,completed from blogs
        """
    else:
        # sql
        sql = """
        select id,title,`date`,completed from blogs WHERE category='{}'
        """.format(category)
    # 数据库操作
    try:
        #连接
        conn = database_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute(sql)
        data = cursor.fetchall()#type:list
        # 关闭
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        return {
            'status': 300,
            'msg': '获取失败！'
        }
    """处理数据"""

    total=len(data)
    if data:
        data.reverse()
    start = (int(pagenum) - 1) * int(pagesize)
    end = int(pagenum) * int(pagesize)
    blogs= data[start:end]

    for i in range(0,len(blogs)):
        blogs[i]['date']=blogs[i]['date'].strftime("%Y-%m-%d")

    """返回"""
    return {
        'status': 200,
        'blogs': blogs,
        'total':total,
    }

"""
删除博客
请求方法：delete
操作：根据id删除博客和图片
参数：id
"""
@bp.route('/deleteBlog', methods=['delete'])
@login_required
def deleteBlog():

    id =request.json.get('id')

    try:
        conn = database_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = """
        select * from blogs WHERE id='{}'
        """.format(id)
        cursor.execute(sql)
        data=cursor.fetchone()

        sql = """
            delete from blogs WHERE id='{}'
            """.format(id)
        cursor.execute(sql)
        cursor.close()
        conn.close()
    except:

        return {
            'status':300,
            'msg':'删除失败'
        }
    if not data:
        return {
            'status': 300,
            'msg': '文章不存在'
        }
    """删除图片"""

    try:

        pattern = '!\[image\.png\]\([\S]*?\)'
        pattern = re.compile(pattern)
        result = pattern.findall(string=data['content'])  # type:list
        imgPaths = []
        for item in result:
            imgPaths.append(item[13:-1])
        for img in imgPaths:
            path=os.path.join(baseDir,img)
            os.remove(path)
    except Exception as e:
        print(e)

    return {
        'status': 200,
        'msg': '删除成功'
    }

