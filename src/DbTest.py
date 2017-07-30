import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='fuzj', passwd='123123', db='fuzj')

# 创建游标
cursor = conn.cursor()

#conn.set_charset('utf-8')
# 执行SQL，并返回收影响行数
#effect_row = cursor.execute("create table user (id int not NULL auto_increment primary key  ,name char(16) not null) ")    #创建一个user表
#print(effect_row)
# 执行SQL，并返回受影响行数，使用占位符 实现动态传参
cursor.execute('SET CHARACTER SET utf8;')
effect_row = cursor.execute("insert into user (name) values (%s) ", ('323'))
effect_row = cursor.executemany("insert into user (name) values (%s) ", [('123',),('456',),('789',),('0',),('1',),('2',),('3',)])

#print(effect_row)
# 执行多个SQL，并返回受影响行数，列表中每个元素都相当于一个条件
effect_row = cursor.executemany("update user set name = %s WHERE  id = %s", [("fuzj",1),("jeck",2)])
print(effect_row)