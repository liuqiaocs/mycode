# coding: utf-8
'''
需要安装python-MySQLdb--一个接口程序，python通过它对mysql数据实现各种操作
'''
import pymysql

'''
conn常用方法：
commit()
rollback()
cursor([cursorclass]),通过游标执行SQL语句
close()
'''

'''
curcor常用方法：
close()
execute(query[,args])
executemany(query, pseq)    对序列pseq中的每个参数执行sql语句
fetchone()  返回一条查询结果
fetchall()
fetchmany([size])
nextset()   移动到下一个结果
scroll(value,mode='relative')   移动游标到指定行，如果mode='relative',则表示从当前所在行移动value条,如果mode='absolute',
                                则表示从结果集的第一行移动value条.
'''

def mysql_init():
    return pymysql.connect(host="localhost",user="root",passwd="123456",db="python",port=3306,charset="utf8")

def mysql_insert(conn):
    cur = conn.cursor()
    cur.execute('insert into users (username, password, email) values (%s, %s, %s)', ('jack', '123456', 'jack@163.com'))
    #cur.executemany("insert into users (username,password,email) values (%s,%s,%s)",(("google","111222","g@gmail.com"),("facebook","222333","f@face.book"),("github","333444","git@hub.com"),("docker","444555","doc@ker.com")))
    conn.commit()

#查询所有，默认字典类型
def mysql_query1(conn):
    cur = conn.cursor()
    cur.execute('select * from users')
    lines = cur.fetchall()
    for line in lines:
        print(line)
    cur.close()

#游标的使用
def mysql_query2(conn):
    cur = conn.cursor()
    cur.execute('select * from users')
    lines = cur.fetchone()
    print(lines)
    print(cur.fetchone())
    print('--------------------------')
    print(cur.fetchall())
    cur.scroll(1, 'absolute')
    print('--------------------------')
    print(cur.fetchmany(4))
    cur.close()

def mysql_update(conn):
    cur = conn.cursor()
    try:
        cur.execute('update users set username = %s where id = 2', ('mypython'))
        conn.commit()
    except:
        print('update failed')
    cur.execute('select * from users where id = 2')
    print(cur.fetchone())
    cur.close()

def mysql_close(conn):
    try:
        conn.close()
    except:
        print('close failed')


if __name__ == '__main__':
    conn = mysql_init()
    #mysql_insert(conn)
    #mysql_query1(conn)
    #mysql_query2(conn)
    mysql_update(conn)

    mysql_close(conn)



























