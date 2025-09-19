from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic

from google.protobuf.message import Message

TQuery = TypeVar('TQuery')
TRequest = TypeVar('TRequest', bound=Message)

class QueryMapper(ABC, Generic[TRequest, TQuery]):
    """
    QueryMapper is an abstract base class that defines a method for mapping a gRPC request to a query.
    """

    @classmethod
    @abstractmethod
    def to_query(cls, request: Type[TRequest]) -> Type[TQuery]:
        """Maps a gRPC request to a query"""
        raise NotImplementedError(f"{cls.__name__} does not implement {cls.to_query.__name__} method")