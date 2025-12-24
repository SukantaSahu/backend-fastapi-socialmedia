from fastapi import FastAPI
import models
#from database import engine, SessionLocal
from database import engine
from routers import post,user,auth,vote
from config import settings
#models.Base.metadata.create_all(bind=engine) #Comment out because alembic used now which will create tables.
        # Connect to the database

app=FastAPI()

#my_posts= [{"title":"this is first title","content":"this is first content", "id":1},{"title":"this is second title","content":"this is second content","id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p
        
# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
async def root():
    return {"Message": "Hellow World"}

# @app.post("/createpost")
# def createpost(payload: dict =Body(...)):
    
#     return {f"title = {payload['title']}, content = {payload['content']}"}


    

