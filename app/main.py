#whoopa ORM style. heeeyyy with alembic!!
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#get your routes via the router files
from app.routers import(
	post,
	user,
	auth,
	vote
) 
#get the models file
from app import models

#importing from database.py file
from app.database import engine

#bind the models in models.py to the database engine
#enable this if you do not have alembic initialised.
#models.Base.metadata.create_all(bind=engine)

#create fast api app body
app = FastAPI()

origins = ['https://www.google.com']

#get the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def get_root():
	return {'message':'Hello World'}


#add cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)














