from typing import Optional
from pydantic import BaseModel
from pydantic.utils import to_lower_camel
from pydantic.main import ModelMetaclass

class PydanticBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True


class AllOptional(ModelMetaclass):
    def __new__(cls, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)


class FromCamelCase(BaseModel):
    class Config:
        alias_generator = to_lower_camel
    

class ToCamelCase(BaseModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True