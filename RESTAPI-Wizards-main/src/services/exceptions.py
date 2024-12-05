from typing import List

from sqlalchemy.orm import Session

from src.database.models import Comment, Picture, User, Tag


from fastapi import HTTPException, status

PICTURE_HAS_ALREADY_5_TAGS_ASSIGNED = -1
TAG_IS_ALREADY_ASSIGNED_TO_PICTURE = -2
TAG_IS_ALREADY_ASSIGNED_TO_PICTURE_AND_PICTURE_HAS_ALREADY_5_TAGS_ASSIGNED = -3
TAG_IS_NOT_ASSIGNED_TO_PICTURE = -4


# async def check_if_picture_exists(picture_id: int, db: Session):
# tu raczej nie powinno być async bo to jest procedura pomocnicza
async def check_if_picture_exists(picture_id: int, db: Session):
    exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found"
    )
    picture = db.query(Picture).filter(Picture.id == picture_id).first()
    if bool(picture) == False:
        print("404 picture not found")
        raise exc

    if picture.is_deleted:
        print("404 picture not found")
        raise exc


def check_if_tag_exists(tag_id: int, db: Session):

    exc = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if bool(tag) == False:
        raise exc


async def check_if_comment_exists(
    picture_id: int, picture_comment_id: int, db: Session
):

    exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
    )
    comment = (
        db.query(Comment)
        .filter(
            Comment.picture_id == picture_id,
            Comment.picture_comment_id == picture_comment_id,
        )
        .first()
    )
    if bool(comment) == False:
        raise exc
    if comment.is_deleted:
        raise exc


def raise_404_exception_if_one_should(source, source_name=""):
    exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"{source_name} not found"
    )
    if bool(source) == False:
        raise exc

    try:
        if source.is_deleted:
            raise exc
    except:
        pass


def check_if_user_is_author(source, current_user: User):
    if source.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
