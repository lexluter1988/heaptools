import pymysql.cursors
connection = pymysql.connect(host='localhost', user='xxx', password='xxx', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
     sql = "show databases;"
     cursor.execute(sql)
     result = cursor.fetchall()
     # if you don't specify database and use admin user -> you can list all databases and create new
