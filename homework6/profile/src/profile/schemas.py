from typing import Optional
from pydantic import root_validator, ValidationError
from datetime import datetime, date


from src.models import (
    FromCamelCase, ToCamelCase, PydanticBase, TimestampMixin, AllOptional
)


class ProfileBaseSchema(PydanticBase):
    first_name: str
    last_name: str
    middle_name: str
    gender: str
    birthday: date
    address: str


class ProfileSchema(ProfileBaseSchema, TimestampMixin):
    id: int


class CreateProfileSchema(ProfileBaseSchema):
    ...


class UpdateProfileSchema(ProfileBaseSchema, FromCamelCase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    address: Optional[str] = None


class ProfileOutSchema(ProfileSchema, ToCamelCase):
    pass
    
