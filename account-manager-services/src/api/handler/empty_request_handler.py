from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic

TRequest = TypeVar('TRequest')

# Request handler which returns no result
# May be able to re-use Notification ?
class RequestHandler(ABC, Generic[TRequest]):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, request: Type[TRequest]) -> None:
        pass