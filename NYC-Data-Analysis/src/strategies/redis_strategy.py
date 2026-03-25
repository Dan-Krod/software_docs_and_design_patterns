from src.interfaces.base_strategy import BaseStrategy
import hashlib
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RedisStrategy(BaseStrategy):
    def __init__(self, host='localhost', port=6379):
        self.active = True  
        self.first_run = True
        try:
            self.client = redis.Redis(
                host=host, port=port, socket_connect_timeout=1)
        except:
            self.active = False

    def send(self, data: dict):
        year = str(data.get('Year', '????'))
        cause = str(data.get('Leading Cause', 'Unknown'))

        if self.first_run:
            self._check_connection()
            self.first_run = False

        if self.active:
            try:
                unique_str = f"{data.get('Year')}{data.get('Leading Cause')}{data.get('Sex')}{data.get('Race Ethnicity')}"

                unique_id = hashlib.md5(unique_str.encode()).hexdigest()[:8]
                key = f"death:{year}:{unique_id}"
                self.client.set(key, str(data))
                print(f"[REDIS] | {year} | OK | Записано ключ {key}")
            except Exception as e:
                self.active = False
                print(f"❌ Помилка Redis: {e}")
                self._print_imitation(year, cause)
        else:
            self._print_imitation(year, cause)

    def _check_connection(self):
        try:
            self.client.ping()
            print("✅ СТАТУС: REDIS ONLINE")
        except:
            self.active = False
            print("⚠️ СТАТУС: REDIS OFFLINE (Режим імітації)")
            print("👉 Для реальної роботи: docker-compose up -d")

    def _print_imitation(self, year, cause):
        print(f"[REDIS-IMITATION] | {year} | {cause[:45]}...")
