from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional


from app.database import Base

class UserCreate(BaseModel):

	email:EmailStr
	password:str

class NewUserResponse(BaseModel):
	id:int
	email:EmailStr
	created_at:datetime
	active:bool
	class Config: #capital fucking C again!
		orm_mode = True

class UserLogin(BaseModel):
	email:EmailStr
	password:str


class PostBase(BaseModel):
	title:str
	content:str
	published: bool = True

class PostCreate(PostBase):
	pass

class PostResponse(PostBase): #this is how we define the data that comes back from the 
	id: int
	created_at: datetime
	created_by: int
	#must match the model column names. Obviously!
	owner: NewUserResponse
	#this connects to the owner relationship in the model. Tells it to return the pydantic models for user
	class Config:
		orm_mode = True

class PostOut(BaseModel): #the root of the class must extend from Base model though.
	Post: PostResponse #schema inherits from another schema.
	votes : int

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id:Optional[str] = None


class Vote(BaseModel):
	post_id: int
	dir: conint(ge=0,le=1) #conint allows specific values by expression. ge is greater than or equal and le is less than or equal.
	



		