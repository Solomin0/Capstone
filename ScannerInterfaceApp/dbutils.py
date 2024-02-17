import mysql.connector

def get_connection_handle(targ_host: str, db: str, user: str, pwd: str):
    '''Connect to database and return db cursor'''
    db_handle = mysql.connector.connect(
        host=targ_host,
        database=db,
        user=user,
        password=pwd
    )
    return db_handle

# connect to db
db = get_connection_handle(
    'localhost',
    'testdb',
    'user1',
    'P@ssw0rd12'
)

#cursor.execute('TRUNCATE assets')
#db_handle.commit()
# init db cursor
cursor = db.cursor()
# execute query
cursor.execute(" SELECT * FROM assets")
# fetch query results
result = cursor.fetchall()
# print results
print(result)
print(cursor.rowcount)
# reset cursor
cursor.reset()

#sql = "INSERT INTO assets (serial_number, short_desc, location) VALUES (%s, %s, %s)"

#val = ('00', 'Desktop', 'here')
#cursor.execute(sql, val)
#db_handle.commit()

db.disconnect() # disconnect from db