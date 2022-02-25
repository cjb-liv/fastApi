from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#function to handle the password hashing
def hash_it(password: str):
	return pwd_context.hash(password)

#pwd verify is a builtin function that compares hashes
def verify_password(plain, hashed):
	return pwd_context.verify(plain,hashed) 