'''
THIS SOFTWARE, ITS SOURCE CODE, AND ANY DISTRIBUTIONS THEREOF IS PROPERTY OF GEORGE MASON UNIVERSITY.
AUTHOR : MARTIN HAYNESWORTH
'''

from mysql import connector

handle = connector.connect(
    host="localhost",
    user="u",
    password="p",
    database="Alpha2"
)


cursor = handle.cursor(dictionary=True)
cursor.reset()
cursor.execute("SELECT * FROM ITEM")
results = cursor.fetchall()

print(type(results))

for r in results:
    print(r)