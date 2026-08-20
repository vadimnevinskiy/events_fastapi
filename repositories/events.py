from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import Event
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from dto import ResponseMessageDTO


async def get_events(db: AsyncSession) -> Sequence[Event]:
    sql_query = select(Event)
    result = await db.scalars(sql_query)

    events: Sequence[Event] = result.all()

    return events


async def get_event(event_id: int, db: AsyncSession) -> Event | None:
    sql_query = select(Event).options(selectinload(Event.author)).where(Event.id == event_id)
    result = await db.scalars(sql_query)

    event: Event | None = result.first()

    return event


async def create_event(event: Event, db: AsyncSession) -> Event:
    db.add(event)
    await db.commit()
    await db.refresh(event)

    refreshed_event: Event = await get_event(event.id, db)

    return refreshed_event


async def delete_event(event: Event, db: AsyncSession) -> ResponseMessageDTO:
    await db.delete(event)
    await db.commit()

    return ResponseMessageDTO(status_code=200, message=f"Event {event.id} was deleted")


async def update_event(event: Event, db: AsyncSession) -> Event:
    await db.commit()
    await db.refresh(event)
    refreshed_event = await get_event(event.id, db)

    return refreshed_event
