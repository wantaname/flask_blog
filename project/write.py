""""
写博客api，登录模块暂时搁置
"""
from flask import Blueprint, request,g
import os
from db import database_conn
import pymysql
from datetime import datetime
from mytoken import login_required
from werkzeug.utils import secure_filename
from config import blogImgDir,baseDir
bp = Blueprint('write', __name__, url_prefix='/write')

"""
保存博客
请求：post
参数：{title:'',category:'',content:'',id:,from:}
操作：写入数据表blogs
返回：{status:,msg:'',id:1}
+ 404 未登录
+ 300 自定义错误
+ 200 保存成功
"""
@bp.route('/saveBlog', methods=['POST'])
def saveBlog():
    from time import time as getTime
    '''获取参数'''
    params=request.json
    title=params.get('title')
    content=params.get('content')
    category=params.get('category')
    _id=params.get('id')

    # 防止sql语句引号错误
    title=pymysql.escape_string(title)
    content=pymysql.escape_string(content)
    category=pymysql.escape_string(category)
    # 保存时间
    time = datetime.now().date()
    date = time.strftime("%Y-%m-%d")

    '''数据库操作'''
    blog_id=_id
    try:

        # 连接
        conn = database_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #
        if int(_id) >= 1:
            # sql
            sql = """
            update blogs set title='{}',`date`='{}',content='{}',category='{}',completed={} WHERE id={}
            """.format(title, date, content, category, 0, _id)
            cursor.execute(sql)
            cursor.execute(sql)
        else:
            sql = """
            insert into blogs(title,`date`,content,category,completed) VALUES ('{}','{}','{}','{}',{})
            """.format(title,date,content,category,0)
            cursor.execute(sql)
        #     返回id
            sql='SELECT LAST_INSERT_ID() as id'
            cursor.execute(sql)
            blog_id=(cursor.fetchone())['id']
            print(blog_id)


        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        return {
            'status': 300,
            'msg': '保存失败,数据库错误',

        }

    '''数据处理及返回'''
    return {
        'status': 200,
        'msg': "保存成功",
        'id': blog_id
    }

@bp.route('/commitBlog', methods=['POST'])
def commitBlog():
    '''获取参数'''
    params=request.json
    title=params.get('title')
    content=params.get('content')
    category=params.get('category')
    _id=params.get('id')
    # 防止sql语句引号错误
    title = pymysql.escape_string(title)
    content = pymysql.escape_string(content)
    category = pymysql.escape_string(category)
    # 保存时间
    time = datetime.now().date()
    date = time.strftime("%Y-%m-%d")

    '''数据库操作'''

    try:

        # 连接
        conn = database_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        if int(_id) >= 1:
            # sql
            sql = """
                update blogs set title='{}',`date`='{}',content='{}',category='{}',completed={} WHERE id={}
                """.format(title,date,content,category,1,_id)
            cursor.execute(sql)
        # 要判断该id是否存在
        else:
            sql = """
            insert into blogs(title,`date`,content,category,completed) VALUES ('{}','{}','{}','{}',{})
            """.format(title, date, content, category, 1)
            cursor.execute(sql)



        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        return {
            'status': 300,
            'msg': '保存失败,数据库错误'
        }

    '''数据处理及返回'''
    return {
        'status': 200,
        'msg': "保存成功"
    }





"""
获取分类
请求：GET
参数：无
操作：查询数据表category
返回：{status:200,msg:'',categorys:[{id:0,category:''},]}
+ 404 未登录
+ 300 自定义错误
+ 200 获取成功
"""
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
图片保存
请求：post
参数：{image:$file},为图片数据
返回：{status:0,msg:'',url:''},url为静态文件路径
"""
@bp.route('/saveImg', methods=['POST'])
def saveImg():
    from time import time as getTime
    '''获取上传的图片'''
    img=request.files['image']

    # 获取文件名
    fileName=secure_filename(img.filename)
    if '.' in fileName:
        imgType='.'+fileName.rsplit('.')[-1]
    else:
        imgType=''
    # 文件名用时间戳命名
    imgName = str(getTime()).replace('.','')+imgType
    imgPath=os.path.join(baseDir,blogImgDir,imgName)
    url=os.path.join(blogImgDir,imgName)

    try:
        # 保存文件
        img.save(imgPath)
    except Exception as e:
        print(e)
        return {
            'status': 300,
            'msg': "图片上传失败",

        }
    '''数据处理及返回'''
    return {
        'status': 200,
        'msg': "图片上传成功",
        'url':url
    }

"""
图片删除
请求：delete
参数：{imgName:''},为图片数据
返回：{status:0,msg:''}
"""
@bp.route('/deleteImg', methods=['delete'])
def deleteImg():

    '''获取参数'''
    imgName=request.args.get('imgName')


    try:
        os.remove(imgName)
    except Exception as e:
        print(e)
        '''数据处理及返回'''
        return {
            'status': 300,
            'msg': "删除失败",

        }





    '''数据处理及返回'''
    return {
        'status': 200,
        'msg': "删除成功",

    }

"""
图片批量保存:已弃用
请求：post
参数：{'1':$file,'2':$file},为图片数据
返回：{status:0,msg:'',urls:[['1',url]]}
"""
@bp.route('/saveImgs', methods=['POST'])
def saveImgs():
    from time import time as getTime
    '''获取上传的图片'''
    imgFiles=request.files

    urls=[]
    for pos in imgFiles.keys():
        item=[]
        # 获取文件名
        fileName = secure_filename(imgFiles[pos].filename)
        imgType =  fileName.rsplit('.')[-1]
        # 文件名用时间戳命名,由于cpu速度太快，时间戳可能会重复，加上pos
        imgName = str(getTime()).replace('.','')+pos + '.'+imgType
        imgPath = os.path.join(blogImgDir, imgName)
        try:
            # 保存文件
            imgFiles[pos].save(imgPath)
        except Exception as e:
            print(e)
            return {
                'status': 300,
                'msg': "图片上传失败",

            }
        item.append(pos)
        item.append(imgPath)
        urls.append(item)

    return {
        'status': 200,
        'msg': "图片上传成功",
        'urls':urls
    }

"""
获取博客信息
请求：GET
参数：{id:博客id,from:来源,blog}
操作：查询数据表category
返回：{status:200,msg:'',blog:{id,title,date,category,content}}
+ 404 未登录
+ 300 自定义错误
+ 200 获取成功
"""
@bp.route('/getBlogInfo', methods=['GET'])
@login_required
def getBlogInfo():
    #获取参数
    _id=int(request.args.get('id'))



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
            'status': 300,
            'msg': '文章不存在！'
        }


    blog= {
        'id':data['id'],
        'title':data['title'],
        'date':data['date'].strftime("%Y-%m-%d"),
        'content':data['content'],
        'category':data['category'],
        'completed':bool(data['completed'])
    }
    return {
        'status': 200,
        'blog': blog
    }



