from mysql import connector

handle = connector.connect(
    host="localhost",
    user="user1",
    password="P@ssw0rd12",
    database="Alpha2"
)


cursor = handle.cursor(dictionary=True)
cursor.reset()
cursor.execute("SELECT * FROM ITEM")
results = cursor.fetchall()

print(type(results))

for r in results:
    print(r)