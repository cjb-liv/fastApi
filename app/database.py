from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,session
from app.config import settings



#SQLALCHEMY_DATABASE_URL = 'postgressq://<username>:<password>@<ipdaddress/hostname>/<databasename>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#now create engine from database url
engine = create_engine(SQLALCHEMY_DATABASE_URL)


#create a session
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Session = session
#base class - all models extend from this class

Base = declarative_base()


#create the dependency to database.py
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()




