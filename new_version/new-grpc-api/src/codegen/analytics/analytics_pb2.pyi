from error import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegistrationStep(_message.Message):
    __slots__ = ("id", "code", "step_name", "step_order", "description", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    STEP_NAME_FIELD_NUMBER: _ClassVar[int]
    STEP_ORDER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    code: int
    step_name: str
    step_order: int
    description: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., code: _Optional[int] = ..., step_name: _Optional[str] = ..., step_order: _Optional[int] = ..., description: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class RegistrationInteraction(_message.Message):
    __slots__ = ("id", "app_user_id", "session_id", "registration_step_id", "previous_step_id", "next_step_id", "step_began_at", "step_completed_at", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_STEP_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_STEP_ID_FIELD_NUMBER: _ClassVar[int]
    NEXT_STEP_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_BEGAN_AT_FIELD_NUMBER: _ClassVar[int]
    STEP_COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    app_user_id: str
    session_id: str
    registration_step_id: str
    previous_step_id: str
    next_step_id: str
    step_began_at: str
    step_completed_at: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., app_user_id: _Optional[str] = ..., session_id: _Optional[str] = ..., registration_step_id: _Optional[str] = ..., previous_step_id: _Optional[str] = ..., next_step_id: _Optional[str] = ..., step_began_at: _Optional[str] = ..., step_completed_at: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class TrackStepRequest(_message.Message):
    __slots__ = ("session_id", "app_user_id", "step_code", "previous_step_code", "next_step_code")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    APP_USER_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_CODE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_STEP_CODE_FIELD_NUMBER: _ClassVar[int]
    NEXT_STEP_CODE_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    app_user_id: str
    step_code: int
    previous_step_code: int
    next_step_code: int
    def __init__(self, session_id: _Optional[str] = ..., app_user_id: _Optional[str] = ..., step_code: _Optional[int] = ..., previous_step_code: _Optional[int] = ..., next_step_code: _Optional[int] = ...) -> None: ...

class TrackStepResponse(_message.Message):
    __slots__ = ("interaction", "errors")
    INTERACTION_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    interaction: RegistrationInteraction
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, interaction: _Optional[_Union[RegistrationInteraction, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...

class CompleteStepRequest(_message.Message):
    __slots__ = ("interaction_id", "next_step_code")
    INTERACTION_ID_FIELD_NUMBER: _ClassVar[int]
    NEXT_STEP_CODE_FIELD_NUMBER: _ClassVar[int]
    interaction_id: str
    next_step_code: int
    def __init__(self, interaction_id: _Optional[str] = ..., next_step_code: _Optional[int] = ...) -> None: ...

class CompleteStepResponse(_message.Message):
    __slots__ = ("interaction", "errors")
    INTERACTION_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    interaction: RegistrationInteraction
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, interaction: _Optional[_Union[RegistrationInteraction, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...

class GetRegistrationStepsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRegistrationStepsResponse(_message.Message):
    __slots__ = ("steps", "errors")
    STEPS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    steps: _containers.RepeatedCompositeFieldContainer[RegistrationStep]
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, steps: _Optional[_Iterable[_Union[RegistrationStep, _Mapping]]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...

class GetUserJourneyRequest(_message.Message):
    __slots__ = ("app_user_id",)
    APP_USER_ID_FIELD_NUMBER: _ClassVar[int]
    app_user_id: str
    def __init__(self, app_user_id: _Optional[str] = ...) -> None: ...

class GetUserJourneyResponse(_message.Message):
    __slots__ = ("interactions", "errors")
    INTERACTIONS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    interactions: _containers.RepeatedCompositeFieldContainer[RegistrationInteraction]
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, interactions: _Optional[_Iterable[_Union[RegistrationInteraction, _Mapping]]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...

class GetSessionJourneyRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class GetSessionJourneyResponse(_message.Message):
    __slots__ = ("interactions", "errors")
    INTERACTIONS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    interactions: _containers.RepeatedCompositeFieldContainer[RegistrationInteraction]
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, interactions: _Optional[_Iterable[_Union[RegistrationInteraction, _Mapping]]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...

class RegistrationStats(_message.Message):
    __slots__ = ("total_sessions", "completed_registrations", "incomplete_registrations", "completion_rate", "dropoff_by_step", "average_duration_seconds")
    class DropoffByStepEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    TOTAL_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_REGISTRATIONS_FIELD_NUMBER: _ClassVar[int]
    INCOMPLETE_REGISTRATIONS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_RATE_FIELD_NUMBER: _ClassVar[int]
    DROPOFF_BY_STEP_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    total_sessions: int
    completed_registrations: int
    incomplete_registrations: int
    completion_rate: float
    dropoff_by_step: _containers.ScalarMap[str, int]
    average_duration_seconds: float
    def __init__(self, total_sessions: _Optional[int] = ..., completed_registrations: _Optional[int] = ..., incomplete_registrations: _Optional[int] = ..., completion_rate: _Optional[float] = ..., dropoff_by_step: _Optional[_Mapping[str, int]] = ..., average_duration_seconds: _Optional[float] = ...) -> None: ...

class GetRegistrationStatsRequest(_message.Message):
    __slots__ = ("start_date", "end_date")
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    start_date: str
    end_date: str
    def __init__(self, start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class GetRegistrationStatsResponse(_message.Message):
    __slots__ = ("stats", "errors")
    STATS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    stats: RegistrationStats
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, stats: _Optional[_Union[RegistrationStats, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...
