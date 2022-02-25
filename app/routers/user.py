from app import (
	schema,
	models,
	utils
)
from fastapi import (
	Response,
	status,
	HTTPException,
	Depends,
	APIRouter
)
from app.database import (
	get_db,
	Session
)

from typing import List 

#this saves on writing the full route everytime route file layout
router = APIRouter(
	prefix = "/users",
	tags = ['Users']     
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.NewUserResponse)
def create_user(user:schema.UserCreate,db:Session = Depends(get_db)):
	
	#hash the password - user.password
	hashed_password = utils.hash_it(user.password)
	user.password = hashed_password
	
	#--- Create User -----
	new_user = models.User(**user.dict()) #creates a dictionary from pydantic model, 
	#then unpacks the dict into separate columns(**user.dict()) for the database model(models.User).
	db.add(new_user) #add the new users to the db
	db.commit() #then we have to commit it
	db.refresh(new_user) #refresh to 
	
	return new_user


@router.get("/{id}",response_model=schema.NewUserResponse)
def get_user_by_id(id : int, db : Session = Depends(get_db)):
	user_query = db.query(models.User).filter(models.User.id == id) #filter is a where
	user = user_query.first() #method to retrieve the first record

	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail = f"User with id {id}, does not exist."
			)
	return user