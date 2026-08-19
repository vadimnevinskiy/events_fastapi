from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name} email={self.email}>"
