from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic

TRequest = TypeVar('TRequest')
TResult = TypeVar('TResult')

class RequestHandler(ABC, Generic[TRequest, TResult]):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, request: Type[TRequest]) -> Type[TResult]:
        pass