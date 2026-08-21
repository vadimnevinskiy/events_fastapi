from pydantic import BaseModel
from enums import RoleType


class RoleDTO(BaseModel):
    title: str
    code: RoleType
    description: str


class RoleCreateDTO(RoleDTO):
    pass


class RoleResponseDTO(RoleDTO):
    id: int

    model_config = {"from_attributes": True}
