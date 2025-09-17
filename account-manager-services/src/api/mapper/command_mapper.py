from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic

from google.protobuf.message import Message

TCommand = TypeVar('TCommand')
TRequest = TypeVar('TRequest', bound=Message)

class CommandMapper(ABC, Generic[TRequest, TCommand]):
    """
    CommandMapper is an abstract base class that defines a method for mapping a gRPC request to a command.
    """

    @classmethod
    @abstractmethod
    def to_command(cls, request: Type[TRequest]) -> Type[TCommand]:
        """Maps a gRPC request to a command"""
        raise NotImplementedError(f"{cls.__name__} does not implement {cls.to_command.__name__} method")