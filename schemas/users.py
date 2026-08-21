from pydantic import BaseModel, EmailStr
from datetime import datetime
from enums import RoleType


class EventBriefDto(BaseModel):
    id: int
    title: str
    description: str | None
    guest_limit: int
    created_at: datetime
    started_at: datetime
    finished_at: datetime

    model_config = {"from_attributes": True}


class RoleBriefDTO(BaseModel):
    id: int
    title: str
    code: RoleType
    description: str

    model_config = {"from_attributes": True}


class UserDTO(BaseModel):
    name: str
    email: EmailStr
    role_id: int


class UserCreateDto(UserDTO):
    pass


class UserResponseDTO(UserDTO):
    id: int

    model_config = {"from_attributes": True}


class UserDetailResponseDto(UserDTO):
    id: int
    role: RoleBriefDTO
    event_list: list[EventBriefDto]

    model_config = {"from_attributes": True}
