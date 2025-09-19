from ..auth import auth_pb2 as _auth_pb2
from ..error import account_error_pb2 as _account_error_pb2
import resource_category_pb2 as _resource_category_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateResourceRequest(_message.Message):
    __slots__ = ("auth", "resource")
    class Resource(_message.Message):
        __slots__ = ("name", "category", "description")
        NAME_FIELD_NUMBER: _ClassVar[int]
        CATEGORY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        name: str
        category: _resource_category_pb2.ResourceCategory
        description: str
        def __init__(self, name: _Optional[str] = ..., category: _Optional[_Union[_resource_category_pb2.ResourceCategory, str]] = ..., description: _Optional[str] = ...) -> None: ...
    AUTH_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    auth: _auth_pb2.Auth
    resource: CreateResourceRequest.Resource
    def __init__(self, auth: _Optional[_Union[_auth_pb2.Auth, _Mapping]] = ..., resource: _Optional[_Union[CreateResourceRequest.Resource, _Mapping]] = ...) -> None: ...

class CreateResourceResponse(_message.Message):
    __slots__ = ("resource", "errors")
    class Resource(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    resource: CreateResourceResponse.Resource
    errors: _containers.RepeatedCompositeFieldContainer[_account_error_pb2.AccountError]
    def __init__(self, resource: _Optional[_Union[CreateResourceResponse.Resource, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_account_error_pb2.AccountError, _Mapping]]] = ...) -> None: ...
