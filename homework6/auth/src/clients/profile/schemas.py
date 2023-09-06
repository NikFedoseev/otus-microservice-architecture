from datetime import  date
from src.models import PydanticBase, TimestampMixin, FromCamelCase

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
    pass