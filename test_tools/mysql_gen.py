import pymysql.cursors
from contextlib import closing

table_template = """
CREATE TABLE {table_name} (
    id int(11) NOT NULL AUTO_INCREMENT,
    data_1 varchar(255) COLLATE utf8_bin NOT NULL,
    data_2 varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;"""

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='xxx',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with closing(connection.cursor()) as cursor:
    sql = "show databases;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
     # if you don't specify database and use admin user -> you can list all databases and create new

    sql = "create database perf_test"
    cursor.execute("use perf_test;")
    for i in range(300000):
        sql = table_template.format(table_name='one_{}'.format(i))
        cursor.execute(sql)

# TODO: size checker
# TODO: fill tables with data
