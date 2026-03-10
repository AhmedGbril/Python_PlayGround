from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from datetime import datetime
import psycopg
from psycopg.rows import dict_row

app=FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    created_at:datetime


try:
    conn=psycopg.connect(
        host="localhost",
        port=5432,
        dbname="fastapi",
        user="postgres",
        password="Pass@123456",
        row_factory=dict_row
    )

    cursor= conn.cursor()
    print("Database connected succesfully")\
    
except Exception as error:
    print(f"Error accured while connecting to the database:  {error}")


@app.get("/post")
def get_all_posts():
 cursor.execute("select * from post;")
 posts=cursor.fetchall()
 return{"data":posts}

@app.get("/post/{id}")
def get_post_byId(id:int):
   cursor.execute(""" select * from post where id=%s """,(id,))
   post=cursor.fetchone()
   return {"data":post}

@app.post("/post")
def create_post(post:Post):
   cursor.execute("insert into post (title,content,published) Values (%s,%s,%s) returning *;",
                  (post.title,post.content,post.published,))
   post=cursor.fetchone()
   conn.commit()
   return {"post":post}

@app.put("/post/{id}")
def update_post(post:Post,id:int):
   cursor.execute(""" update post set title=%s ,content=%s , published=%s where id=%s Returning * ;  """,(post.title,post.content,post.published,id,))
   updated_post=cursor.fetchone()
   conn.commit()
   if updated_post== None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"There is no post with the Id:{id} to delete")
   
   return {"data":updated_post}

@app.delete("/post/{id}")
def delete_post(id:int):
   cursor.execute(""" delete from post where id=%s Returning *; """,(id,))
   post=cursor.fetchone()
   conn.commit()
   if post== None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"There is no post with the Id:{id} to delete")
   return {"data":post}



