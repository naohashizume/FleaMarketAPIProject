import mysql.connector

db_conn = mysql.connector.connect(host="a01022269-lab8.westus2.cloudapp.azure.com",
                                  user="root",
                                  password="P@ssw0rd",
                                  database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
 CREATE TABLE sell_request
(id INT NOT NULL AUTO_INCREMENT,
 customer_id VARCHAR(250) NOT NULL, 
 seller_id VARCHAR(250) NOT NULL,
 item_id VARCHAR(250) NOT NULL,
 item_name VARCHAR(250) NOT NULL,
 time_stamp VARCHAR(100) NOT NULL,
 date_created VARCHAR(100) NOT NULL,
 CONSTRAINT sell_request_pk PRIMARY KEY (id))
 ''')

db_cursor.execute('''
 CREATE TABLE buy_request
(id INT NOT NULL AUTO_INCREMENT,
 customer_id VARCHAR(250) NOT NULL, 
 seller_id VARCHAR(250) NOT NULL,
 item_id VARCHAR(250) NOT NULL,
 item_name VARCHAR(250) NOT NULL,
 time_stamp VARCHAR(100) NOT NULL,
 date_created VARCHAR(100) NOT NULL,
 CONSTRAINT buy_request_pk PRIMARY KEY (id))
 ''')

db_conn.commit()
db_conn.close()