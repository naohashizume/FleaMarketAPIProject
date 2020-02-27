import mysql.connector

db_conn = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="ktcf8774",
                                  database="lab4")

db_cursor = db_conn.cursor()

db_cursor.execute('''
 DROP TABLE sell_request, buy_request
''')

db_conn.commit()
db_conn.close()