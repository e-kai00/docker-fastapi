from fastapi import APIRouter
from ..db.db_connect import connectDB


router = APIRouter()

client, db, posts_collection, comments_collection = connectDB()


@router.get('/report', tags=['report'])
def get_report():    
    pipeline = [
        {
            "$lookup": {
                "from": "comments",
                "localField": "id",
                "foreignField": "postId",
                "as": "comments"
            }
        },
        {
            "$group": {
                "_id": "$userId",
                "posts_count": {"$sum": 1},
                "comments_count": {"$sum": {"$size": "$comments"}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "user_id": "$_id",
                "posts_count": 1,
                "comments_count": 1
            }
        },
        {
            "$sort": {
                "user_id": 1
            }
        }
        
    ]
    result = list(posts_collection.aggregate(pipeline))
    return result

