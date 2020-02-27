import sqlite3

conn = sqlite3.connect('requests.sqlite')

c = conn.cursor()
c.execute('''
    CREATE TABLE sell_request
    (id INTEGER PRIMARY KEY ASC,
     customer_id VARCHAR(250) NOT NULL, 
     seller_id VARCHAR(250) NOT NULL,
     item_id VARCHAR(250) NOT NULL,
     item_name VARCHAR(250) NOT NULL,
     time_stamp VARCHAR(100) NOT NULL,
     date_created VARCHAR(100) NOT NULL)
''')

c.execute('''
    CREATE TABLE buy_request
    (id INTEGER PRIMARY KEY ASC,
     customer_id VARCHAR(250) NOT NULL,
     seller_id VARCHAR(250) NOT NULL,
     item_id VARCHAR(250) NOT NULL,
     item_name VARCHAR(250) NOT NULL,
     time_stamp VARCHAR(100) NOT NULL,
     date_created VARCHAR(100) NOT NULL)
''')

conn.commit()
conn.close()