import mysql.connector

db_conn = mysql.connector.connect(host="a01022269-lab8.westus2.cloudapp.azure.com",
                                  user="root",
                                  password="P@ssw0rd",
                                  database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
 DROP TABLE sell_request, buy_request
''')

db_conn.commit()
db_conn.close()