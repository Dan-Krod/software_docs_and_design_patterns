import csv
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.models import Message, User
from src.data_access.interfaces import IMessageRepository, IUserRepository

class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter_by(email=email).first()

    def add(self, user: User) -> None:
        self.session.add(user)

class MessageRepository(IMessageRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_to_db(self, m: Message) -> bool:
        try:
            self.session.add(m)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Save error: {e}")
            self.session.rollback()
            return False

    def delete_from_db(self, message_id: int) -> bool:
        try:
            msg = self.session.query(Message).get(message_id)
            if msg:
                self.session.delete(msg)
                self.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Delete error: {e}")
            self.session.rollback()
            return False

    def load_from_db(self, channel_id: int, limit: int) -> List[Message]:
        return self.session.query(Message).filter_by(channel_id=channel_id).limit(limit).all()

    def load_from_csv(self, file_path: str) -> List[dict]:
        """Reads all columns for 1000+ rows as required by Lab 2"""
        data = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                dict_reader = csv.DictReader(f)
                for row in dict_reader:
                    data.append(row)
            return data
        except FileNotFoundError:
            print(f"File {file_path} not found!")
            return []