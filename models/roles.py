from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum
from enums import RoleType


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[RoleType] = mapped_column(Enum(RoleType), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(250), nullable=True)

    def __repr__(self) -> str:
        return f"<Role id={self.id} title={self.title} code={self.code} description={self.description}>"
