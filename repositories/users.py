from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy import select
from dto import ResponseMessageDTO


async def get_users(db: AsyncSession) -> Sequence[User]:
    sql_query = select(User)
    result = await db.scalars(sql_query)

    users: Sequence[User] = result.all()

    return users


async def get_user(user_id: int, db: AsyncSession) -> User | None:
    sql_query = select(User).where(User.id == user_id)
    result = await db.scalars(sql_query)

    user: User | None = result.first()

    return user


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    sql_query = select(User).where(User.email == email)
    result = await db.scalars(sql_query)

    user: User | None = result.first()

    return user


async def create_user(user: User, db: AsyncSession) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(user: User, db: AsyncSession) -> ResponseMessageDTO:
    await db.delete(user)
    await db.commit()

    return ResponseMessageDTO(status_code=200, message=f"User {user.id} was deleted")


async def update_user(user: User, db: AsyncSession) -> User:
    await db.commit()
    await db.refresh(user)

    return user
