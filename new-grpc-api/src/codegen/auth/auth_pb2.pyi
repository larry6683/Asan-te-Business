from auth import entity_type_pb2 as _entity_type_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Auth(_message.Message):
    __slots__ = ("user", "entity")
    class User(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class Entity(_message.Message):
        __slots__ = ("entity_type", "id")
        ENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        entity_type: _entity_type_pb2.EntityType
        id: str
        def __init__(self, entity_type: _Optional[_Union[_entity_type_pb2.EntityType, str]] = ..., id: _Optional[str] = ...) -> None: ...
    USER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    user: Auth.User
    entity: Auth.Entity
    def __init__(self, user: _Optional[_Union[Auth.User, _Mapping]] = ..., entity: _Optional[_Union[Auth.Entity, _Mapping]] = ...) -> None: ...
