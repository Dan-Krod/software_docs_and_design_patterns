from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Message, User

class IUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> None:
        pass

class IMessageRepository(ABC):
    @abstractmethod
    def save_to_db(self, m: Message) -> bool:
        pass

    @abstractmethod
    def load_from_db(self, channel_id: int, limit: int) -> List[Message]:
        pass

    @abstractmethod
    def delete_from_db(self, message_id: int) -> bool:
        """Implementation of deleteFromDB() from UML"""
        pass

    @abstractmethod
    def load_from_csv(self, file_path: str) -> List[dict]:
        """Required by Lab 2 to read 1000+ rows"""
        pass