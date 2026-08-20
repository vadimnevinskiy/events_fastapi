from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBriefTDO(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}


class EventDTO(BaseModel):
    title: str
    description: str
    guest_limit: int
    author_id: int
    started_at: datetime
    finished_at: datetime


class EventCreateDTO(EventDTO):
    pass


class EventResponseDTO(EventDTO):
    id: int
    created_at: datetime
    author: UserBriefTDO

    model_config = {"from_attributes": True}
