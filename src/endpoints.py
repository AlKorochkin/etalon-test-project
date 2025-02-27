import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cruds import (
    create_user_project,
    get_user_project_by_name,
    get_user_projects,
)
from db import get_async_session
from models import User
from schemas import ProjectCreate, ProjectRead, ProjectsRead
from auth import current_active_user
from utils import get_weather_data

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

    projects_with_weather = []
    for project in projects:
        weather = None
        project_read = ProjectRead(
            id=project.id,
            name=project.name,
            location=project.location,
            weather=weather
        )
        projects_with_weather.append(project_read)

    return ProjectsRead(projects=projects_with_weather)


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
