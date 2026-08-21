from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import Role
from sqlalchemy import select


async def get_roles(db: AsyncSession) -> Sequence[Role]:
    sql_query = select(Role)
    result = await db.scalars(sql_query)

    roles: Sequence[Role] = result.all()

    return roles


async def get_role(role_id: int, db: AsyncSession) -> Role:
    sql_query = select(Role).where(Role.id == role_id)
    result = await db.scalars(sql_query)

    role: Role | None = result.first()

    return role

