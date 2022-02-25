
#this is where we set up our database tables. This is also where we set up our constraints.

#import the relavant column 
from sqlalchemy import (
	Column, 
	Integer,
	String,
	Boolean
)
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import(
	TIMESTAMP, 
	Boolean
) 

#get the base model from database.py
from .database import Base

#this class defines the table called posts in the database
class Post(Base):

	#define the table name
	__tablename__ = "posts"
	#id, title and content columns. Not they do use python datatypes. Datatypes imported from SQLAlchemy
	id = Column(Integer,primary_key=True,nullable=False)
	title = Column(String,nullable=False)
	content = Column(String,nullable=False)
	#needs server default because true in sql does not = True in python
	published = Column(Boolean, server_default = 'true',nullable=False)
	#add timestamp later
	created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default=text('NOW()'))
	#set up a new column in the post table, with the foreignkey integrity constraint
	#klike creating manually in postgres, ForeignKey method args id column of user table, action, null constraint
	created_by = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False) 
	#this sets a relationship in the model without using a foreign key constraint.
	owner = relationship("User")


#this class defines the user table
class User(Base):
	#define the table name
	__tablename__ = "users"

	id = Column(Integer,primary_key=True,nullable=False)
	email = Column(String,nullable=False, unique=True) #use uinique constraint = true to only have unique email addresses
	phone = Column(String,nullable=True)
	password = Column(String,nullable=False) 
	created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default=text('NOW()'))
	active = Column(Boolean,server_default='true')


class Votes(Base):
	#votes table where the composite primary key columns are foreign keys in the posts and user tables
	__tablename__ = "votes"

	user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
	post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True,nullable=False)

