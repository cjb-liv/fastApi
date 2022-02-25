from sqlalchemy.sql.functions import user
from app import (
	schema,
	models,
	utils,
	oauth2
)
from fastapi import (
	Response,
	status,
	HTTPException,
	Depends,
	APIRouter,

)

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database import (
	get_db,
	Session
)

from typing import List 

#this saves on writing the full route everytime route file layout
router = APIRouter(
	tags = ['Authentication']     
)

@router.post('/login',response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	
	#return username
	#return password
	#users credentials now compares form username == model email.
	user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

	if not user:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN, 
			detail=f"Invalid Credentials"
			)
	
	if not utils.verify_password(user_credentials.password,user.password):
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail = "Password Incorrect"
		)
	#create a token at this point..........
	access_token = oauth2.create_access_token(data = {"user_id":user.id})

	return {"access_token":access_token,"token_type":"bearer",}
	
	