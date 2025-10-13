from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class EntityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTITY_UNSPECIFIED: _ClassVar[EntityType]
    ENTITY_BUSINESS: _ClassVar[EntityType]
    ENTITY_BENEFICIARY: _ClassVar[EntityType]
    ENTITY_CONSUMER: _ClassVar[EntityType]
ENTITY_UNSPECIFIED: EntityType
ENTITY_BUSINESS: EntityType
ENTITY_BENEFICIARY: EntityType
ENTITY_CONSUMER: EntityType
