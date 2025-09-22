from ..auth import auth_pb2 as _auth_pb2
from ..error import user_error_pb2 as _user_error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserByEmailRequest(_message.Message):
    __slots__ = ("auth", "email")
    AUTH_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    auth: _auth_pb2.Auth
    email: str
    def __init__(self, auth: _Optional[_Union[_auth_pb2.Auth, _Mapping]] = ..., email: _Optional[str] = ...) -> None: ...

class GetUserByEmailResponse(_message.Message):
    __slots__ = ("user", "errors")
    class User(_message.Message):
        __slots__ = ("id", "email", "user_type")
        ID_FIELD_NUMBER: _ClassVar[int]
        EMAIL_FIELD_NUMBER: _ClassVar[int]
        USER_TYPE_FIELD_NUMBER: _ClassVar[int]
        id: str
        email: str
        user_type: str
        def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., user_type: _Optional[str] = ...) -> None: ...
    USER_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    user: GetUserByEmailResponse.User
    errors: _containers.RepeatedCompositeFieldContainer[_user_error_pb2.UserError]
    def __init__(self, user: _Optional[_Union[GetUserByEmailResponse.User, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_user_error_pb2.UserError, _Mapping]]] = ...) -> None: ...
