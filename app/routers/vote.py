from app import (
	schema,
	models,
	oauth2
)
from fastapi import (
	status,
	HTTPException,
	Depends,
	APIRouter
)
from app.database import (
	get_db,
	Session
)


router = APIRouter(
	prefix = "/vote",
	tags = ['Votes']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(
	vote: schema.Vote,
	db: Session = Depends(get_db),
	current_user:int = Depends(oauth2.get_current_user)
	):
	
	#check if post exists before attempting to vote on it.
	post_exists = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

	if not post_exists:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"Post {vote.post_id} does not exist." )

	#filter allows multiple conditions, separated by a comma.
	vote_check = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == current_user.id)
	vote_found = vote_check.first()

	if (vote.dir == 1):
		#does vote exist?
		if vote_found:
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT, 
				detail = f"User: {current_user.email} id:{current_user.id} has already voted on this Post"
				)
		else:
			new_vote = models.Votes(post_id = vote.post_id,user_id = current_user.id)
			db.add(new_vote)
			db.commit()
			return {"message":"Vote successful"}
	else:
		if not vote_found:
			#tell the user that the vote doesnt exist
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,detail =f"User User: {current_user.email} id:{current_user.id} has never voted on this post"
			)
		else:
			#delete the vote from the vote table using vote_check
			vote_check.delete(synchronize_session = False)
			db.commit()
			return {"message":"Vote successfully deleted."}




