from ..error import user_error_pb2 as _user_error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateBusinessRequest(_message.Message):
    __slots__ = ("business", "user_email")
    class Business(_message.Message):
        __slots__ = ("business_name", "email", "website_url", "phone_number", "location_city", "location_state", "ein", "business_description", "business_size")
        BUSINESS_NAME_FIELD_NUMBER: _ClassVar[int]
        EMAIL_FIELD_NUMBER: _ClassVar[int]
        WEBSITE_URL_FIELD_NUMBER: _ClassVar[int]
        PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
        LOCATION_CITY_FIELD_NUMBER: _ClassVar[int]
        LOCATION_STATE_FIELD_NUMBER: _ClassVar[int]
        EIN_FIELD_NUMBER: _ClassVar[int]
        BUSINESS_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        BUSINESS_SIZE_FIELD_NUMBER: _ClassVar[int]
        business_name: str
        email: str
        website_url: str
        phone_number: str
        location_city: str
        location_state: str
        ein: str
        business_description: str
        business_size: str
        def __init__(self, business_name: _Optional[str] = ..., email: _Optional[str] = ..., website_url: _Optional[str] = ..., phone_number: _Optional[str] = ..., location_city: _Optional[str] = ..., location_state: _Optional[str] = ..., ein: _Optional[str] = ..., business_description: _Optional[str] = ..., business_size: _Optional[str] = ...) -> None: ...
    BUSINESS_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    business: CreateBusinessRequest.Business
    user_email: str
    def __init__(self, business: _Optional[_Union[CreateBusinessRequest.Business, _Mapping]] = ..., user_email: _Optional[str] = ...) -> None: ...

class CreateBusinessResponse(_message.Message):
    __slots__ = ("business", "errors")
    class Business(_message.Message):
        __slots__ = ("id", "business_name", "email", "website_url", "phone_number", "location_city", "location_state", "ein", "business_description", "business_size")
        ID_FIELD_NUMBER: _ClassVar[int]
        BUSINESS_NAME_FIELD_NUMBER: _ClassVar[int]
        EMAIL_FIELD_NUMBER: _ClassVar[int]
        WEBSITE_URL_FIELD_NUMBER: _ClassVar[int]
        PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
        LOCATION_CITY_FIELD_NUMBER: _ClassVar[int]
        LOCATION_STATE_FIELD_NUMBER: _ClassVar[int]
        EIN_FIELD_NUMBER: _ClassVar[int]
        BUSINESS_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        BUSINESS_SIZE_FIELD_NUMBER: _ClassVar[int]
        id: str
        business_name: str
        email: str
        website_url: str
        phone_number: str
        location_city: str
        location_state: str
        ein: str
        business_description: str
        business_size: str
        def __init__(self, id: _Optional[str] = ..., business_name: _Optional[str] = ..., email: _Optional[str] = ..., website_url: _Optional[str] = ..., phone_number: _Optional[str] = ..., location_city: _Optional[str] = ..., location_state: _Optional[str] = ..., ein: _Optional[str] = ..., business_description: _Optional[str] = ..., business_size: _Optional[str] = ...) -> None: ...
    BUSINESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    business: CreateBusinessResponse.Business
    errors: _containers.RepeatedCompositeFieldContainer[_user_error_pb2.UserError]
    def __init__(self, business: _Optional[_Union[CreateBusinessResponse.Business, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_user_error_pb2.UserError, _Mapping]]] = ...) -> None: ...
