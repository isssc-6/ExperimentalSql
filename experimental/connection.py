import psycopg

conn = psycopg.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="db",
    port="5432"
)

cur = conn.cursor()

print(conn)