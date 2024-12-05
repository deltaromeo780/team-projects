from typing import List

from sqlalchemy.orm import Session

from src.database.models import Tag, Picture
from src.schemas import TagModel


async def get_tags(skip: int, limit: int, db: Session) -> list[Tag] | None:
    return db.query(Tag).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, db: Session) -> Tag:
    return db.query(Tag).filter(Tag.id == tag_id).first()

async def get_tag_by_name_or_create(name: str, db: Session) -> Tag:
    if db.query(Tag).filter(Tag.name == name).first():
        return db.query(Tag).filter(Tag.name == name).first()
    else:
        return await create_tag_form(name, db)

async def create_tag_form(name: str, db: Session) -> Tag:

    tag = Tag(name=name)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag

async def create_tag(body: TagModel, db: Session) -> Tag:

    tag = Tag(name=body.name.lower())

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag

async def get_picture_tags(picture_id: int, db: Session) -> list[Tag] | None:
    picture = db.query(Picture).filter(Picture.id == picture_id).first()
    return picture.tags

