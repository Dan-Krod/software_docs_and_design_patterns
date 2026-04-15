from src.data_access.database import db_system
from src.domain.models import User

session = db_system.get_session()
users = session.query(User).all()

for u in users:
    if not u.password_hash:
        u.set_password('admin123') 

session.commit()
print("Готово! Всі юзери отримали пароль admin123")