from sqlalchemy.sql import func
from app import (
	schema,
	models,
	oauth2
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
from typing import (
	List, 
	Optional
)
router = APIRouter(
	prefix = "/posts",
	tags = ['Posts']
)
@router.get("/",response_model=List[schema.PostOut])
#@router.get("/")
def get_all_posts(
	db:Session = Depends(get_db),
	current_user:int = Depends(oauth2.get_current_user),
	limit:int = 10,
	skip:int = 0,
	search:Optional[str] = ""
	):

	#query parameters are enabled at limit and offset.
	#if you want to login to get all posts for a user, change line above to: 
	#posts = db.query(models.Post).filter(models.Post.created_by == current_user.id)
	
	#join the posts and the votes table, with a left outer join, 
	#group by posts.id
	#then the search filter, the limits and the skip
	#and last of all return all records (all())
	posts = db.query(
		models.Post,
		func.count(models.Votes.post_id).label("votes")
		).join(
			models.Votes, 
			models.Votes.post_id == models.Post.id,
			isouter=True
			).group_by(
				models.Post.id
				).filter(
					models.Post.title.contains(search)
					).limit(
						limit
						).offset(
							skip
							).all()

	return posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.PostResponse)
def create_posts(
	post:schema.PostCreate, 
	db:Session = Depends(get_db),
	current_user:int = Depends(oauth2.get_current_user)
	): #this always to access the database instance
	#create an object with the model and call it new_posts

	new_posts = models.Post(created_by = current_user.id,**post.dict()) #creates a dictionary from pydantic model, then unpacks the dict into separate columns for the database model.
	db.add(new_posts) #add the new_posts to the db
	db.commit() #then we have to commit it
	db.refresh(new_posts) #refresh to 

	return new_posts

@router.get("/{id}",response_model=schema.PostOut)
def get_post_by_id(
	id : int, db : Session = Depends(get_db),
	current_user:int = Depends(oauth2.get_current_user)
	): 
	#get the id as int, and open a database instance
	post_query = db.query(
		models.Post,
		func.count(models.Votes.post_id).label("votes")
		).join(
			models.Votes, 
			models.Votes.post_id == models.Post.id,
			isouter=True
			).group_by(
				models.Post.id
				).filter(models.Post.id == id) #filter is a where
	post = post_query.first() #method to retrieve the first record
	
	if not post:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail = f"Post with id {id}, does not exist."
			)

	'''if post.created_by != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN, 
			detail = 'Not authorised to perform this action'
			)'''
	
	return post

@router.delete("/{id}",response_model=schema.PostResponse)
def delete_post(
	id : int, db: Session = Depends(get_db),
	current_user:int = Depends(oauth2.get_current_user)
	):

	post_query = db.query(models.Post).filter(models.Post.id == id)

	post = post_query.first()
	#you cannot kill that which has no life!
	if not post: 
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail = f"post with id number {id} not found"
			)

	#are you the right person to delete this?
	if post.created_by != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN, 
			detail = 'Not authorised to perform this action'
			)

	post_query.delete(synchronize_session = False) #delete the actual post
	db.commit() #confirm the changes
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.PostResponse)
def update_post(
	id: int, updated_post: schema.PostCreate, 
	db: Session = Depends(get_db),
	current_user:int = Depends(oauth2.get_current_user)
	):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	post = post_query.first()

	if not post:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail = f"post with id number {id} does not exist"
			)
	
	#are you the right person to delete this?
	if post.created_by != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail = 'Not authorised to perform this action'
			)

	post_query.update(
		updated_post.dict(),
		synchronize_session = False
		)

	db.commit()

	return post_query.first()

@router.get("/latest",response_model=schema.PostResponse)
def get_latest(db:Session = Depends(get_db)):
	latest = db.query(func.max(models.Post.created_at).label("latest"))
	result = latest.one()
	latest_date = result.latest

	latest_post = db.query(models.Post).filter(models.Post.created_at == latest_date).first()
	return latest_post