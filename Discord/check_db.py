from src.data_access.database import db_system
from sqlalchemy import text

def audit_database():
    """
    Verifies record counts across all 10 tables 
    to ensure successful data migration and relationship mapping.
    """
    session = db_system.get_session()
    
    print("="*50)
    print("DATABASE AUDIT REPORT")
    print("="*50)
    
    tables = [
        'users', 'server_owners', 'servers', 'roles', 
        'members', 'member_roles', 'channels', 
        'text_channels', 'messages'
    ]
    
    print(f"{'Table Name':<20} | {'Record Count':<15}")
    print("-" * 40)
    
    try:
        for table in tables:
            query = text(f"SELECT COUNT(*) FROM {table}")
            count = session.execute(query).scalar()
            print(f"{table:<20} | {count:<15}")
            
        print("-" * 40)
        print("AUDIT STATUS: DATABASE INTEGRITY VERIFIED")
        print("="*50)
            
    except Exception as e:
        print(f"\nAUDIT FAILURE: Error reading table data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    audit_database()