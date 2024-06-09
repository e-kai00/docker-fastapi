import requests
from fastapi import APIRouter
from pydantic import ValidationError
from ..db.models import Post, Comment
from ..db.db_connect import connectDB

router = APIRouter()

client, db, posts_collection, comments_collection = connectDB()


def fetch_data():
    post_response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = post_response.json()

    comment_response = requests.get('https://jsonplaceholder.typicode.com/comments')
    comments = comment_response.json()

    return posts, comments


def validate_and_save_data(posts, comments):
    validated_posts = []
    for post in posts:
        try:
            valid_post = Post(**post)
            validated_posts.append(valid_post.model_dump())
        except ValidationError as e:
            print(e)

    validated_comments = []
    for comment in comments:
        try:
            valid_comment = Comment(**comment)
            validated_comments.append(valid_comment.model_dump())
        except ValidationError as e:
            print(e)

    if validated_posts:
        posts_collection.insert_many(validated_posts)

    if valid_comment:
        comments_collection.insert_many(validated_comments)


@router.get('/api_data', tags=['api_data'])
async def fetch_and_save_data():
    # posts_collection.delete_many({})
    # comments_collection.delete_many({})

    posts, comments = fetch_data()
    validate_and_save_data(posts, comments)
    return {"msg": "Data fetched and saved successfully"}


