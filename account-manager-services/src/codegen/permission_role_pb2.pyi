from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class PermissionRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PERMISSION_ROLE_UNSPECIFIED: _ClassVar[PermissionRole]
    PERMISSION_ROLE_ADMIN: _ClassVar[PermissionRole]
    PERMISSION_ROLE_TEAM_MEMBER: _ClassVar[PermissionRole]
PERMISSION_ROLE_UNSPECIFIED: PermissionRole
PERMISSION_ROLE_ADMIN: PermissionRole
PERMISSION_ROLE_TEAM_MEMBER: PermissionRole
