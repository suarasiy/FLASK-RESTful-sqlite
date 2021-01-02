import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id INT, username TEXT, password TEXT)"
cursor.execute(create_table)

user = (1, "suara", "123")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (1, "suara", "123"),
    (2, "siy", "456")
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()