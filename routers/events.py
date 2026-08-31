from collections.abc import Sequence
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import EventCreateDTO, EventResponseDTO, EventUpdateDTO
from models import Event
from dto import ResponseMessageDTO
from services import event as event_service
from errors import EventNotFound, UserNotFound

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=list[EventResponseDTO])
async def get_events(db: AsyncSession = Depends(get_db)) -> list[EventResponseDTO]:
    events: Sequence[Event] = await event_service.get_events(db)

    return [EventResponseDTO.model_validate(event) for event in events]


@router.get("/{event_id}", response_model=EventResponseDTO)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)) -> EventResponseDTO:
    try:
        event: Event = await event_service.get_event(event_id, db)
    except EventNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return EventResponseDTO.model_validate(event)


@router.post("/", response_model=EventResponseDTO)
async def create_event(new_event: EventCreateDTO, author_id: int,
                       db: AsyncSession = Depends(get_db)) -> EventResponseDTO:
    try:
        event: Event = await event_service.create_event(new_event, author_id, db)
    except UserNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return EventResponseDTO.model_validate(event)


@router.delete("/{event_id}", response_model=ResponseMessageDTO)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)) -> ResponseMessageDTO:
    try:
        result: ResponseMessageDTO = await event_service.delete_event(event_id, db)
    except EventNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ResponseMessageDTO.model_validate(result)


@router.put("/{event_id}", response_model=EventResponseDTO)
async def update_event(event_id: int, new_event: EventUpdateDTO,
                       db: AsyncSession = Depends(get_db)) -> EventResponseDTO:
    try:
        event: Event = await event_service.update_event(event_id, new_event, db)
    except EventNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return EventResponseDTO.model_validate(event)


