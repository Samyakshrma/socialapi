from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException ,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, Session, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='social', user='postgres', password='hellothere',
                                cursor_factory=RealDictCursor)

        cur = conn.cursor()
        print("Database Connection Successful!")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error : ", error)
        time.sleep(2)


@app.get("/get")
def root():
    cur.execute("SELECT * FROM POSTS")
    Posts = cur.fetchall()
    return {"data": Posts}


@app.get("/get/{Id}")
def get_posts(Id: int):
    try:
        cur.execute(f"SELECT * FROM POSTS WHERE ID ={Id} ;")
        post = cur.fetchall()
        return post
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {Id} not found")


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.post("/posts")
def Create_posts(post: Post):
    cur.execute("""INSERT INTO POSTS(title,content,published) VALUES( %s,%s,%s) RETURNING * """, (post.title,
                                                                                                  post.content,
                                                                                                  post.published))
    content = cur.fetchone()
    conn.commit()
    return {"data": content}


@app.delete("/posts/{Id}", status_code=status.HTTP_204_NO_CONTENT)
def Delete_post(Id: int):
    cur.execute("""DELETE FROM POSTS WHERE ID = %s RETURNING *""", (str(Id),))
    deleted_post = cur.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Deleted post {Id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{Id}")
def Update_post(Id: int, post: Post):
    cur.execute("""UPDATE POSTS SET title = %s,content = %s,published  = %s WHERE Id= %s RETURNING *""", (post.title,
                                                                                                          post.content,
                                                                                                          post.published,
                                                                                                          str(Id)))
    update = cur.fetchone()
    conn.commit()

    if update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Deleted post {Id} does not exist")

    return {"data": update}

@app.get("/alchemy")
def alc(db: Session = Depends(get_db)):
    post = db.query(models.Posts).all()
    return {"Result": post}
