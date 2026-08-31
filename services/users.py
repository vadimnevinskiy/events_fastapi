from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserCreateDto
from dto import ResponseMessageDTO
from repositories import users as user_repository
from errors import UserNotFound, UserAlreadyExists


async def get_users(db: AsyncSession) -> Sequence[User]:
    users: Sequence[User] = await user_repository.get_users(db)

    return users


async def get_user(user_id: int, db: AsyncSession) -> User:
    user: User | None = await user_repository.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id)

    return user


async def get_user_detail(user_id: int, db: AsyncSession) -> User:
    user: User | None = await user_repository.get_user_detail(user_id, db)

    if user is None:
        raise UserNotFound(user_id)

    return user


async def create_user(new_user: UserCreateDto, db: AsyncSession) -> User:
    user: User | None = await user_repository.get_user_by_email(new_user.email, db)

    if user is not None:
        raise UserAlreadyExists(str(new_user.email))

    user: User = User(name=new_user.name, email=new_user.email, role_id=new_user.role_id)

    return await user_repository.create_user(user, db)


async def delete_user(user_id: int, db: AsyncSession) -> ResponseMessageDTO:
    user: User | None = await user_repository.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id)

    result: ResponseMessageDTO = await user_repository.delete_user(user, db)

    return result


async def update_user(user_id: int, new_user: UserCreateDto, db: AsyncSession) -> User:
    user: User | None = await user_repository.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id)

    existing_user: User | None = await user_repository.get_user_by_email(new_user.email, db)

    if existing_user is not None and existing_user.id != user.id:
        raise UserAlreadyExists(user.email)

    user.name = new_user.name
    user.email = new_user.email
    user.role_id = new_user.role_id

    updated_user: User = await user_repository.update_user(user, db)

    return updated_user
