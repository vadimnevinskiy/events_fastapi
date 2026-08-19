from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings as conf
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

engine = create_async_engine(conf.settings.database_url)
SessionLocal = async_sessionmaker(bind=engine)


async def get_db():
    async with SessionLocal() as db:
        yield db


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
