from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic

TDomain = TypeVar('TDomain')
TApi = TypeVar('TApi')

class ApiConverter(ABC, Generic[TDomain, TApi]):
    """
    ApiConverter is an abstract base class that defines methods for converting between domain objects and API representations.
    """
    
    @classmethod
    @abstractmethod
    def to_domain(cls, input: Type[TApi]) -> Type[TDomain]:
        raise NotImplementedError(f"{cls.__name__} does not implement {cls.to_domain.__name__} method")

    @classmethod
    @abstractmethod
    def to_api(cls, input: Type[TDomain]) -> Type[TApi]:
        raise NotImplementedError(f"{cls.__name__} does not implement {cls.to_api.__name__} method")