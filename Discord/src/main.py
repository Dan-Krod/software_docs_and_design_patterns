import os
import traceback
import time
from src.data_access.database import db_system
from src.data_access.repositories import SqlAlchemyUserRepository, MessageRepository
from src.business_logic.services import DataImportService

def bootstrap():
    """
    App Bootstrapper: Initializes infrastructure, injects dependencies, 
    and executes business logic (Lab 2 requirements).
    """
    print("="*50)
    print("INITIALIZATION")
    print("="*50)
    
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print("[1/3] Setting up database schema...")
    db_system.create_tables()
    
    if not db_system.test_connection():
        print("CRITICAL ERROR: Database connection failed.")
        return
    print("SUCCESS: Database connection established.")

    session = db_system.get_session()

    try:
        user_repo = SqlAlchemyUserRepository(session)
        message_repo = MessageRepository(session)

        import_service = DataImportService(
            message_repo=message_repo, 
            user_repo=user_repo,
            session=session
        )

        csv_path = "data/seed_data.csv"
        
        if os.path.exists(csv_path):
            print(f"[2/3] Reading source file: {csv_path}")
            start_time = time.time()
            
            print("[3/3] Processing business logic and ORM mapping...")
            import_service.import_discord_data(csv_path)
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            print("-" * 50)
            print("FINAL STATUS: SUCCESS")
            print(f"Execution time: {duration} seconds")
            print("="*50)
        else:
            print(f"ERROR: {csv_path} missing. Please run generator.py first.")

    except Exception as e:
        print(f"\nCRITICAL SYSTEM FAILURE: {e}")
        traceback.print_exc() 
    finally:
        session.close()

if __name__ == "__main__":
    bootstrap()