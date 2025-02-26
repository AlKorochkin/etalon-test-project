from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import uuid
from pydantic import UUID4, BaseModel, Field
from fastapi_users import schemas


class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    location: str = Field(min_length=1, max_length=100)


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class ProjectsRead(BaseModel):
    projects: List[Optional[ProjectRead]]


@dataclass(frozen=True)
class PasswordPattern:
    min_len: int = 6
    max_len: int = 18
    regex: str = rf"^[0-9a-zA-Z]{{{min_len}, {max_len}}}$"
    description: str = (
        f"Пароль может состоять из цифр и латинских букв. Длина от {min_len} до {max_len} символов."
    )


@dataclass(frozen=True)
class FIOPattern:
    min_len: int = 5
    max_len: int = 150
    regex: str = rf"^[a-zA-Zа-яА-Я.\s]{{{min_len}, {max_len}}}$"
    description: str = (
        f"ФИО может состоять латинских или русских букв, пробелов, точек. Длина от {min_len} до {max_len} символов."
    )


@dataclass(frozen=True)
class INNPattern:
    min_len: int = 10
    max_len: int = 12
    regex: str = rf"^[0-9]{{{min_len}, {max_len}}}$"
    description: str = f"ИНН должен быть от {min_len} до {max_len} цифр."


class UserRead(schemas.BaseUser[uuid.UUID]):
    fio: str
    email_notify: bool


class UserCreate(schemas.BaseUserCreate):
    fio: str = Field(
        min_length=FIOPattern.min_len,
        max_length=FIOPattern.max_len,
        pattern=FIOPattern.regex,
    )
    inn: str = Field(
        min_length=INNPattern.min_len,
        max_length=INNPattern.max_len,
        pattern=INNPattern.regex,
    )
    password: str = Field(
        min_length=PasswordPattern.min_len,
        max_length=PasswordPattern.max_len,
        pattern=PasswordPattern.regex,
    )


class UserUpdate(schemas.CreateUpdateDictModel):
    fio: str = Field(
        min_length=FIOPattern.min_len,
        max_length=FIOPattern.max_len,
        pattern=FIOPattern.regex,
    )
    inn: str = Field(
        min_length=INNPattern.min_len,
        max_length=INNPattern.max_len,
        pattern=INNPattern.regex,
    )
    email_notify: Optional[bool] = False


class UserPasswordReset(schemas.CreateUpdateDictModel):
    password: str = Field(
        min_length=PasswordPattern.min_len,
        max_length=PasswordPattern.max_len,
        pattern=PasswordPattern.regex,
    )
