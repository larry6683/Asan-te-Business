from error import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Beneficiary(_message.Message):
    __slots__ = ("id", "beneficiary_name", "email", "website_url", "phone_number", "location_city", "location_state", "ein", "beneficiary_description", "beneficiary_size")
    ID_FIELD_NUMBER: _ClassVar[int]
    BENEFICIARY_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_URL_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LOCATION_CITY_FIELD_NUMBER: _ClassVar[int]
    LOCATION_STATE_FIELD_NUMBER: _ClassVar[int]
    EIN_FIELD_NUMBER: _ClassVar[int]
    BENEFICIARY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    BENEFICIARY_SIZE_FIELD_NUMBER: _ClassVar[int]
    id: str
    beneficiary_name: str
    email: str
    website_url: str
    phone_number: str
    location_city: str
    location_state: str
    ein: str
    beneficiary_description: str
    beneficiary_size: str
    def __init__(self, id: _Optional[str] = ..., beneficiary_name: _Optional[str] = ..., email: _Optional[str] = ..., website_url: _Optional[str] = ..., phone_number: _Optional[str] = ..., location_city: _Optional[str] = ..., location_state: _Optional[str] = ..., ein: _Optional[str] = ..., beneficiary_description: _Optional[str] = ..., beneficiary_size: _Optional[str] = ...) -> None: ...

class GetBeneficiaryRequest(_message.Message):
    __slots__ = ("beneficiary_id",)
    BENEFICIARY_ID_FIELD_NUMBER: _ClassVar[int]
    beneficiary_id: str
    def __init__(self, beneficiary_id: _Optional[str] = ...) -> None: ...

class GetBeneficiaryResponse(_message.Message):
    __slots__ = ("beneficiary", "errors")
    BENEFICIARY_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    beneficiary: Beneficiary
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, beneficiary: _Optional[_Union[Beneficiary, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...

class CreateBeneficiaryRequest(_message.Message):
    __slots__ = ("beneficiary_name", "email", "website_url", "phone_number", "location_city", "location_state", "ein", "beneficiary_description", "beneficiary_size", "user_email")
    BENEFICIARY_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_URL_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LOCATION_CITY_FIELD_NUMBER: _ClassVar[int]
    LOCATION_STATE_FIELD_NUMBER: _ClassVar[int]
    EIN_FIELD_NUMBER: _ClassVar[int]
    BENEFICIARY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    BENEFICIARY_SIZE_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    beneficiary_name: str
    email: str
    website_url: str
    phone_number: str
    location_city: str
    location_state: str
    ein: str
    beneficiary_description: str
    beneficiary_size: str
    user_email: str
    def __init__(self, beneficiary_name: _Optional[str] = ..., email: _Optional[str] = ..., website_url: _Optional[str] = ..., phone_number: _Optional[str] = ..., location_city: _Optional[str] = ..., location_state: _Optional[str] = ..., ein: _Optional[str] = ..., beneficiary_description: _Optional[str] = ..., beneficiary_size: _Optional[str] = ..., user_email: _Optional[str] = ...) -> None: ...

class CreateBeneficiaryResponse(_message.Message):
    __slots__ = ("beneficiary", "errors")
    BENEFICIARY_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    beneficiary: Beneficiary
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, beneficiary: _Optional[_Union[Beneficiary, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...
