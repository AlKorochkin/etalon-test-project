from typing import List, Optional
from uuid import UUID

from pydantic import UUID4
from sqlalchemy import and_, or_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Project
from models import User
from schemas import ProjectCreate


async def get_user_projects(db: AsyncSession, user_id: UUID):
    async with db as session:
        stmt = select(Project).where(Project.owner_id == user_id)
        result = await session.scalars(stmt)
        projects = result.all()
    return projects


async def get_user_project_by_name(db: AsyncSession, user_id: UUID, project_name: str):
    async with db as session:
        stmt = select(Project).where(
            and_(
                Project.owner_id == user_id,
                Project.name == project_name,
            )
        )
        result = await session.scalars(stmt)
        project = result.one_or_none()
    return project


async def projects_has_same_name(
    db: AsyncSession, project_name: str, project_id: int
) -> bool:
    async with db as session:
        stmt = select(Project).where(
            and_(
                Project.name == project_name,
                Project.id != project_id,
            )
        )
        result = await session.scalars(stmt)
        has_same_name = result.one_or_none()
        if has_same_name:
            return True
    return False


async def get_user_project_by_id(
    session: AsyncSession,
    user_id: UUID,
    project_id: int,
):
    stmt = select(Project).where(
        and_(Project.id == project_id, Project.owner_id == user_id)
    )
    result = await session.scalars(stmt)
    project = result.one_or_none()
    return project


async def create_user_project(
    db: AsyncSession, user_id: UUID4, project: ProjectCreate
) -> Optional[Project]:
    async with db as session:
        stmt = (
            insert(Project)
            .values(
                name=project.name,
                location=project.location,
                owner_id=user_id,
            )
            .returning(Project)
        )
        result = await session.scalars(stmt)
        await session.commit()
    return result.one_or_none()


async def delete_user_project(db: AsyncSession, project: Project) -> None:
    async with db as session:
        await session.delete(project)
        await session.commit()
    return None
