from pydantic import Field

from src.clients.profile.schemas import CreateProfileSchema
from src.models import (
    FromCamelCase, ToCamelCase, PydanticBase, ActiveMixin, TimestampMixin
)


class LoginUserSchema(PydanticBase):
    email: str
    password: str


class UserSchema(ActiveMixin, TimestampMixin):
    id: int
    email: str
    password: str
    profile_id: int


class RegisterUserSchema(CreateProfileSchema, FromCamelCase):
    email: str
    password: str


class CreateUserSchema(PydanticBase):
    email: str
    password: str
    profile_id: int


class UserOutSchema(UserSchema, ToCamelCase):
    password: str = Field(exclude=True)
        