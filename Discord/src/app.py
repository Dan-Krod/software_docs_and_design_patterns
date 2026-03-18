import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_access.database import db_system
from src.data_access.repositories import MessageRepository, SqlAlchemyUserRepository
from src.business_logic.services import DataImportService
from src.presentation import web_controller

def start_web_app():
    session = db_system.get_session()
    
    msg_repo = MessageRepository(session)
    user_repo = SqlAlchemyUserRepository(session)
    
    service = DataImportService(msg_repo, user_repo, session)
    
    web_controller.service = service
    
    web_controller.app.run(debug=True, port=5000)

if __name__ == "__main__":
    start_web_app()