from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic
from handler.notification import Notification

TNotification = TypeVar('TNotification', bound=Notification)

class NotificationHandler(ABC, Generic[TNotification]):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, notification: Type[TNotification]) -> None:
        pass