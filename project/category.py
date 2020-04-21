from flask import Blueprint, request

from db import database_conn
import pymysql

from mytoken import login_required
bp = Blueprint('category', __name__, url_prefix='/category')


@bp.route('/getCategory', methods=['GET'])
@login_required
def getCategory():
    conn = database_conn()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = """
        select category from category
        """
    cursor.execute(sql)
    all_data = cursor.fetchall()

    sql = """
    select category,count(*) as number from blogs GROUP by category
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    has_data_list=[]
    if(not data):
        data=[]
    for item in data:
        has_data_list.append(item['category'])
    for item in all_data:
        if item['category'] not in has_data_list:
            data.append({'category':item['category'],'number':0})
    return {
        'status':200,
        'categorys':data
    }


@bp.route('/deleteCategory', methods=['delete'])
@login_required
def deleteCategory():

    category_list =request.json.get('select')

    conn = database_conn()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    for item in category_list:
        try:
            sql = """
                delete from category WHERE category='{}'
                """.format(item)
            cursor.execute(sql)
        except:
            cursor.close()
            conn.close()
            return {
                'status':300,
                'msg':'该分类下有博客'
            }
    cursor.close()
    conn.close()
    return {
        'status': 200,
        'msg': '删除成功'
    }

@bp.route('/addCategory', methods=['POST'])
@login_required
def addCategory():

    category=request.json.get('category')

    conn = database_conn()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        sql = """
            insert into category(category) VALUES ('{}')
            """.format(category)
        cursor.execute(sql)
    except:
        cursor.close()
        conn.close()
        return {
            'status':300,
            'msg':'该分类已存在'
        }
    cursor.close()
    conn.close()
    return {
        'status': 200,
        'msg': '添加成功'
    }