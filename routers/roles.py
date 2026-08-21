from collections.abc import Sequence
from fastapi import APIRouter, HTTPException, Depends
from schemas import RoleCreateDTO, RoleResponseDTO
from models import Role
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import roles as role_service
from dto import ResponseMessageDTO
from errors import RoleNotFound, RoleAlreadyExists

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleResponseDTO])
async def get_roles(db: AsyncSession = Depends(get_db)) -> list[RoleResponseDTO]:
    roles: Sequence[Role] = await role_service.get_roles(db)

    return [RoleResponseDTO.model_validate(role) for role in roles]


@router.get("/{role_id}", response_model=RoleResponseDTO)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)) -> RoleResponseDTO:
    try:
        role: Role = await role_service.get_role(role_id, db)
    except RoleNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return RoleResponseDTO.model_validate(role)


@router.post("/", response_model=RoleResponseDTO)
async def create_role(new_role: RoleCreateDTO, db: AsyncSession = Depends(get_db)) -> RoleResponseDTO:
    try:
        role: Role = await role_service.create_role(new_role, db)
    except RoleAlreadyExists as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return RoleResponseDTO.model_validate(role)


@router.delete("/{role_id}", response_model=ResponseMessageDTO)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)) -> ResponseMessageDTO:
    try:
        result: ResponseMessageDTO = await role_service.delete_role(role_id, db)
    except RoleNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ResponseMessageDTO.model_validate(result)


@router.put("/{role_id}", response_model=RoleResponseDTO)
async def update_role(role_id: int, new_role: RoleCreateDTO, db: AsyncSession = Depends(get_db)) -> RoleResponseDTO:
    try:
        role: Role = await role_service.update_role(role_id, new_role, db)
    except RoleNotFound as exc_not_found:
        raise HTTPException(status_code=404, detail=str(exc_not_found))
    except RoleAlreadyExists as exc_exists:
        raise HTTPException(status_code=409, detail=str(exc_exists))

    return RoleResponseDTO.model_validate(role)
