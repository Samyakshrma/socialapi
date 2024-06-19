from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
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
def get_posts(Id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == Id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {Id} not found")


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.post("/posts")
def Create_posts(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Posts(title=post.title, content=post.content, published=post.published) is same as below
    new_post = models.Posts(**post.dict())  # ** unpacks the dict
    # It automatically takes the fields as a dict and then unpacks it to get the necessary result
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.delete("/posts/{Id}", status_code=status.HTTP_204_NO_CONTENT)
def Delete_post(Id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == Id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Deleted post {Id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{Id}")
def Update_post(Id: int, post: Post, db: Session = Depends(get_db)):

    # cur.execute("""UPDATE POSTS SET title = %s,content = %s,published  = %s WHERE Id= %s RETURNING *""", (post.title,
    #                                                                                                     post.content,
    #                                                                                                    post.published,
    #                                                                                                   str(Id)))

    post_query = db.query(models.Posts).filter(models.Posts.id == Id)
    posts = post_query.first()

    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Deleted post {Id} does not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}


@app.get("/alchemy")
def alc(db: Session = Depends(get_db)):
    post = db.query(models.Posts).all()
    return {"Result": post}
