from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import Role
from schemas import RoleCreateDTO
from repositories import roles as role_repository
from errors import RoleNotFound, RoleAlreadyExists
from dto import ResponseMessageDTO


async def get_roles(db: AsyncSession) -> Sequence[Role]:
    roles: Sequence[Role] = await role_repository.get_roles(db)

    return roles


async def get_role(role_id: int, db: AsyncSession) -> Role:
    role: Role | None = await role_repository.get_role(role_id, db)

    if role is None:
        raise RoleNotFound(role_id)

    return role


async def create_role(new_role: RoleCreateDTO, db: AsyncSession) -> Role:
    role: Role | None = await role_repository.get_role_by_code(new_role.code, db)

    if role is not None:
        raise RoleAlreadyExists(str(new_role.code))

    role_inst: Role = Role(title=new_role.title, code=new_role.code, description=new_role.description)

    role: Role = await role_repository.create_role(role_inst, db)

    return role


async def delete_role(role_id: int, db: AsyncSession) -> ResponseMessageDTO:
    role: Role | None = await role_repository.get_role(role_id, db)

    if role is None:
        raise RoleNotFound(role_id)

    result: ResponseMessageDTO = await role_repository.delete_role(role, db)

    return result


async def update_role(role_id: int, new_role: RoleCreateDTO, db: AsyncSession) -> Role:
    role: Role | None = await role_repository.get_role(role_id, db)

    if role is None:
        raise RoleNotFound(role_id)

    updated_role: Role = await role_repository.update_role(role, db)

    return updated_role
