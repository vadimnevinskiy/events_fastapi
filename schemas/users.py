from pydantic import BaseModel, EmailStr
from datetime import datetime


class EventBriefDto(BaseModel):
    id: int
    title: str
    description: str | None
    guest_limit: str
    created_at: datetime
    started_at: datetime
    finished_at: datetime

    model_config = {"from_attributes": True}


class UserDTO(BaseModel):
    name: str
    email: EmailStr


class UserCreateDto(UserDTO):
    pass


class UserResponseDTO(UserDTO):
    id: int

    model_config = {"from_attributes": True}


class UserDetailResponseDto(UserDTO):
    id: int
    event_list: list[EventBriefDto]

    model_config = {"from_attributes": True}
