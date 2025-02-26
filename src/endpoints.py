import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users import models, exceptions
from fastapi_users.manager import BaseUserManager
from sqlalchemy.ext.asyncio import AsyncSession

from cruds import (
    create_user_project,
    delete_user_project,
    get_user_project_by_id,
    get_user_project_by_name,
    get_user_projects,
    projects_has_same_name,
)
from db import get_async_session
from models import User
from schemas import ProjectCreate, ProjectRead, ProjectsRead
from auth import current_active_user, settings, get_user_manager

projects_router = APIRouter()

logger = logging.getLogger(__name__)


@projects_router.get(
    "/projects",
    response_model=ProjectsRead,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
    },
)
async def get_projects(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    projects = await get_user_projects(db, user.id)
    return ProjectsRead(projects=projects)


@projects_router.post(
    "/projects",
    response_model=ProjectRead,
    response_model_exclude={"application_id"},
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Conflict when creating...",
        },
    },
)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    project_exist = await get_user_project_by_name(db, user.id, project.name)
    if project_exist:
        logger.warning("Проект с именем: {} уже существует.".format(project.name))
        raise HTTPException(
            status_code=409,
            detail="Проект с именем: {} уже существует.".format(project.name),
        )
    new_project = await create_user_project(db, user.id, project)
    return new_project
