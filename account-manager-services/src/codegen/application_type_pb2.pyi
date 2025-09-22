from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    APPLICATION_TYPE_UNSPECIFIED: _ClassVar[ApplicationType]
    APPLICATION_TYPE_WEB: _ClassVar[ApplicationType]
    APPLICATION_TYPE_MOBILE_APP: _ClassVar[ApplicationType]
APPLICATION_TYPE_UNSPECIFIED: ApplicationType
APPLICATION_TYPE_WEB: ApplicationType
APPLICATION_TYPE_MOBILE_APP: ApplicationType
