from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic

from google.protobuf.message import Message

TResult = TypeVar('TResult')
TResponse = TypeVar('TResponse', bound=Message)

class ResponseMapper(ABC, Generic[TResponse, TResult]):
    """
    ResponseMapper is an abstract base class that defines a method for mapping a query result to a gRPC response.
    """
    
    @classmethod
    @abstractmethod
    def to_response(cls, result: Type[TResult]) -> Type[TResponse]:
        """Maps a result to a gRPC response"""
        raise NotImplementedError(f"{cls.__name__} does not implement {cls.to_response.__name__} method")
