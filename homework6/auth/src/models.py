from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.alias_generators import to_camel
from pydantic.main import _model_construction

class PydanticBase(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True


class AllOptional(_model_construction.ModelMetaclass):
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
        alias_generator = to_camel
    

class ToCamelCase(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class ActiveMixin(PydanticBase):
    active: bool


class TimestampMixin(PydanticBase):
    created_at: datetime
    updated_at: datetime