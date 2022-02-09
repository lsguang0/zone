import time
import pymysql
from flask import jsonify
from dbpool import POOL


userList = [
    {
        'username': 'abcd',
        'password': '1234'
    }
]


# 打开连接
def create_conn():
    conn = POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    return conn, cursor


# 关闭连接
def close_conn(conn, cursor):
    cursor.close()
    conn.close()


# 插入一条数据
def insert(sql, args):
    conn, cursor = create_conn()
    res = cursor.execute(sql, args)
    conn.commit()
    close_conn(conn, cursor)
    return res


# 查询一条数据
def fetch_one(sql, args):
    conn, cursor = create_conn()
    cursor.execute(sql, args)
    res = cursor.fetchone()
    close_conn(conn, cursor)
    return res


# 查询所有数据
def fetch_all(sql, args):
    conn, cursor = create_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


search_sql = 'select * from user where username = %s'
insert_sql = 'insert into user (username, password, create_time) VALUES (%s, %s, %s)'


def check_user_list(username, password):  # 查询数据库列表返回结果
    data = fetch_one(sql=search_sql, args=username)
    print(data)
    if not data:
        return jsonify({'status': 400, 'msg': '账号不存在'})
    elif data and password == data['password']:
        msg = f'欢迎用户{username}登陆'
        return jsonify({'status': 200, 'msg': msg})
    else:
        return jsonify({'status': 400, 'msg': '账号或密码不正确，请重新输入'})


def check_user_register(username, password):
    data = fetch_one(sql=search_sql, args=username)
    if data:
        return jsonify({'status': 400, 'msg': '账号名已被注册，请修改'})
    res = insert(sql=insert_sql, args=(username, password, time.strftime("%Y-%m-%d %H:%M:%S")))
    if res >= 1:
        return jsonify({'status': 200, 'msg': '注册成功，请登录'})
    else:
        return jsonify({'status': 400, 'msg': '注册失败，请尝试重新注册'})



