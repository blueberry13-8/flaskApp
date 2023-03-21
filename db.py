import psycopg2
con = psycopg2.connect(dbname='flask', user='postgres',
                       password=open('password.txt').read(), host="127.0.0.1", port="5432")
cur = con.cursor()

with open('schema.sql') as f:
    cur.execute(f.read())

cur.execute("INSERT INTO posts (title, content) VALUES ('First Post', 'Content for the first post')")

cur.execute("INSERT INTO posts (title, content) VALUES ('Second Post', 'Content for the second post')")

con.commit()
con.close()

