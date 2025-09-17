from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOURCE_CATEGORY_UNSPECIFIED: _ClassVar[ResourceCategory]
    RESOURCE_CATEGORY_HARDWARE: _ClassVar[ResourceCategory]
    RESOURCE_CATEGORY_SOFTWARE: _ClassVar[ResourceCategory]
    RESOURCE_CATEGORY_SERVICE: _ClassVar[ResourceCategory]
RESOURCE_CATEGORY_UNSPECIFIED: ResourceCategory
RESOURCE_CATEGORY_HARDWARE: ResourceCategory
RESOURCE_CATEGORY_SOFTWARE: ResourceCategory
RESOURCE_CATEGORY_SERVICE: ResourceCategory
