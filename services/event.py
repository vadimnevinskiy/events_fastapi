from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import Event, User
from schemas import EventCreateDTO
from repositories import events as event_repository
from repositories import users as user_repository
from errors import EventNotFound, UserNotFound
from dto import ResponseMessageDTO


async def get_events(db: AsyncSession) -> Sequence[Event]:
    events: Sequence[Event] = await event_repository.get_events(db)

    return events


async def get_event(event_id: int, db: AsyncSession) -> Event:
    event: Event | None = await event_repository.get_event(event_id, db)

    if event is None:
        raise EventNotFound(event_id)

    return event


async def create_event(new_event: EventCreateDTO, author_id: int, db: AsyncSession) -> Event:
    user: User | None = await user_repository.get_user(author_id, db)

    if user is None:
        raise UserNotFound(author_id)

    event_inst: Event = Event(
        title=new_event.title,
        description=new_event.description,
        guest_limit=new_event.guest_limit,
        author_id=user.id,
        started_at=new_event.started_at,
        finished_at=new_event.finished_at
    )

    event: Event = await event_repository.create_event(event_inst, db)

    return event


async def delete_event(event_id: int, db: AsyncSession) -> ResponseMessageDTO:
    event: Event | None = await event_repository.get_event(event_id, db)

    if event is None:
        raise EventNotFound(event_id)

    result: ResponseMessageDTO = await event_repository.delete_event(event, db)

    return result


async def update_event(event_id: int, new_event: EventCreateDTO, db: AsyncSession) -> Event:
    event: Event | None = await event_repository.get_event(event_id, db)

    if event is None:
        raise EventNotFound(event_id)

    event.title = new_event.title
    event.description = new_event.description
    event.guest_limit = new_event.guest_limit
    event.started_at = new_event.started_at
    event.finished_at = new_event.finished_at

    updated_event: Event = await event_repository.update_event(event, db)

    return updated_event
