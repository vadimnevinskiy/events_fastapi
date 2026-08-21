from typing import TYPE_CHECKING
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

if TYPE_CHECKING:
    from .events import Event
    from .roles import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    role: Mapped["Role"] = relationship("Role")

    event_list: Mapped[list["Event"]] = relationship("Event", back_populates="author")

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name} email={self.email} role_id={self.role_id}>"
