import firebase_admin
from firebase_admin import credentials, db
from src.interfaces.base_strategy import BaseStrategy
import hashlib
import os
import math

class FirebaseStrategy(BaseStrategy):
    def __init__(self):
        self.active = False
        self.first_run = True
        
        key_path = '------'
        database_url = '-------'

        if os.path.exists(key_path):
            try:
                if not firebase_admin._apps:
                    cred = credentials.Certificate(key_path)
                    firebase_admin.initialize_app(cred, {
                        'databaseURL': database_url
                    })
                self.ref = db.reference('nyc_deaths')
                self.active = True
            except Exception as e:
                self.active = False
        else:
            self.active = False

    def send(self, data: dict):
        year = str(data.get('Year', '????'))
        cause = str(data.get('Leading Cause', 'Unknown'))

        if self.active:
            try:
                clean_data = {}
                for key, value in data.items():
                    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                        clean_data[key] = None 
                    else:
                        clean_data[key] = value

                unique_str = f"{year}{cause}{data.get('Sex', '')}"
                unique_id = hashlib.md5(unique_str.encode()).hexdigest()[:8]
                
                self.ref.child(unique_id).set(clean_data)
                print(f"[FIREBASE-RT] | {year} | OK | Записано в Realtime DB")
                
            except Exception as e:
                self.active = False
                print(f"❌ ПОМИЛКА: {e}")
                self._print_imitation(year, cause)
        else:
            self._print_imitation(year, cause)

    def _print_status(self):
        if self.active:
            print("✅ СТАТУС: FIREBASE REALTIME DB ONLINE")
        else:
            print("⚠️ СТАТУС: FIREBASE OFFLINE (Режим імітації)")

    def _print_imitation(self, year, cause):
        print(f"[FIREBASE-IMITATION] | {year} | {cause[:40]}...")