from typing import TYPE_CHECKING
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, func
from datetime import datetime

if TYPE_CHECKING:
    from .users import User


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    guest_limit: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    author: Mapped["User"] = relationship("User", back_populates="event_list")

    def __repr__(self) -> str:
        return (f"<Event id={self.id} "
                f"title={self.title} "
                f"guest_limit={self.guest_limit} "
                f"guest_limit={self.guest_limit} "
                f"author_id={self.author_id} "
                f"created_at={self.created_at} "
                f"started_at={self.started_at} "
                f"finished_at={self.finished_at}>")
