from collections.abc import Sequence
from fastapi import APIRouter, HTTPException, Depends
from schemas import UserCreateDto, UserResponseDTO, UserDetailResponseDto
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import users as user_service
from errors import UserNotFound, UserAlreadyExists
from dto import ResponseMessageDTO

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponseDTO])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[UserResponseDTO]:
    users: Sequence[User] = await user_service.get_users(db)

    return [UserResponseDTO.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserDetailResponseDto)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserDetailResponseDto:
    try:
        user: User = await user_service.get_user_detail(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return UserDetailResponseDto.model_validate(user)


@router.post("/", response_model=UserResponseDTO)
async def create_user(new_user: UserCreateDto, db: AsyncSession = Depends(get_db)) -> UserResponseDTO:
    try:
        user: User = await user_service.create_user(new_user, db)
    except UserAlreadyExists as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return UserResponseDTO.model_validate(user)


@router.delete("/{user_id}", response_model=ResponseMessageDTO)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> ResponseMessageDTO:
    try:
        result = await user_service.delete_user(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ResponseMessageDTO.model_validate(result)


@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(user_id: int, new_user: UserCreateDto, db: AsyncSession = Depends(get_db)) -> UserResponseDTO:
    try:
        user: User = await user_service.update_user(user_id, new_user, db)
    except UserNotFound as exc_not_found:
        raise HTTPException(status_code=404, detail=str(exc_not_found))
    except UserAlreadyExists as exc_exists:
        raise HTTPException(status_code=404, detail=str(exc_exists))

    return UserResponseDTO.model_validate(user)
