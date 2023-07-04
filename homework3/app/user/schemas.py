from pydantic import root_validator, ValidationError
from app.models import PydanticBase, FromCamelCase, ToCamelCase, AllOptional


class UserBase(PydanticBase):
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str


class UserSchema(UserBase):
    id: int


class CreateUserSchema(UserBase, FromCamelCase):
    pass


class UpdateUserSchema(UserBase, FromCamelCase, metaclass=AllOptional):
    @root_validator(pre=True)
    def has_any_field_value(cls, values):
        if not values:
            possible_fields = ', '.join(list(cls.__fields__.keys()))
            raise TypeError(f'request body must contain at least one of following fields ({possible_fields})')
        return values



class UserOutSchema(UserSchema, ToCamelCase):
    pass
        
