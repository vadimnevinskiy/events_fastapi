from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import Role
from sqlalchemy import select
from dto import ResponseMessageDTO
from enums import RoleType


async def get_roles(db: AsyncSession) -> Sequence[Role]:
    sql_query = select(Role)
    result = await db.scalars(sql_query)

    roles: Sequence[Role] = result.all()

    return roles


async def get_role(role_id: int, db: AsyncSession) -> Role | None:
    sql_query = select(Role).where(Role.id == role_id)
    result = await db.scalars(sql_query)

    role: Role | None = result.first()

    return role


async def get_role_by_code(code: RoleType, db: AsyncSession) -> Role | None:
    sql_query = select(Role).where(Role.code == code)
    result = await db.scalars(sql_query)

    role: Role | None = result.first()

    return role


async def create_role(role: Role, db: AsyncSession) -> Role:
    db.add(role)
    await db.commit()
    await db.refresh(role)

    return role


async def delete_role(role: Role, db: AsyncSession) -> ResponseMessageDTO:
    """Created roles cannot be deleted."""
    # await db.delete(role)
    # await db.commit()
    #
    # return ResponseMessageDTO(status_code=200, message=f"Role {role.id} was deleted")
    pass


async def update_role(role: Role, db: AsyncSession) -> Role:
    await db.commit()
    await db.refresh(role)

    return role
