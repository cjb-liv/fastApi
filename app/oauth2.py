from sqlalchemy.orm import Session
from fastapi.param_functions import Depends

from jose import(
	JWTError,
	jwt
) 
from datetime import(
	datetime, 
	timedelta
)
from app import(
	schema,
	database,
	models
)

from fastapi import (
	Depends,
	status,
	HTTPException
)
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#-------env variable ----


SECRET_KEY=settings.secret_key
ALGORITHM = settings.Algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire

#-------------------------------------------------------------------
#function recieves dict from auth.py router.post(/login), currently {"current_user_id":user.id}


def create_access_token(data:dict): 
	to_encode = data.copy() 
	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE) #create the expiry time using utc
	to_encode.update({"exp":expire}) #update the copy of the data with the exp key and variable

	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #jwt encode, 1st arg is the input data copy, the second is the secret and third is the algorithm

	return encoded_jwt

def verify_access_token(token: str, credentials_exception):
	#because it may not always work
	try:
		payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
		id: str = payload.get("user_id")
		#print(id)
		if id is None:
			raise credentials_exception
		token_data = schema.TokenData(id=id)
	except JWTError as J:
		print(J)
		raise credentials_exception
	except AssertionError as A:
		print(A)
	return token_data


def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
	
	credentials_exception = HTTPException(
		status_code = status.HTTP_401_UNAUTHORIZED,
		detail = "Could not validate Credentials", 
		headers = {"WWW-Authenitcate":"Bearer"}
		)
	#get token from verify token
	token = verify_access_token(token, credentials_exception)
	
	#set variable: user_id with the result of querying the user table (models) 
	# get the id from token and match in filter
	user = db.query(models.User).filter(models.User.id == token.id).first()
	return user
