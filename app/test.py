import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(host='localhost',database='social',user='postgres',password='hellothere', cursor_factory=RealDictCursor)

cur = conn.cursor()

cur.execute("SELECT * FROM POSTS ;")
POSTS= cur.fetchall()
print(POSTS)