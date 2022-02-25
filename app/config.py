from pydantic import BaseSettings


#Tell the computer what env variable we need to set.
class Settings(BaseSettings):
	database_hostname: str 
	database_port: str
	database_name: str 
	database_password: str
	database_username: str
	secret_key:str
	Algorithm:str
	access_token_expire:int

	class Config:
		env_file = ".env"

settings = Settings()