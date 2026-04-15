import json
from src.interfaces.base_strategy import BaseStrategy
try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False


class KafkaStrategy(BaseStrategy):
    def __init__(self, bootstrap_servers='localhost:9092', topic='nyc_deaths'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.active = False
        self.first_run = True
        self.retry_counter = 0  
        self._connect()

    def _connect(self):
        """Внутрішній метод для спроби підключення"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(7, 5, 0),
                request_timeout_ms=1000,
                metadata_max_age_ms=1000
            )
            self.active = True
            return True
        except:
            self.active = False
            return False

    def send(self, data: dict):
        year = str(data.get('Year', '????'))
        cause = str(data.get('Leading Cause', 'Unknown'))

        if self.first_run:
            self._print_status()
            self.first_run = False

        if not self.active:
            self.retry_counter += 1
            if self.retry_counter >= 5:
                print(f"🔄 [KAFKA] Спроба відновити зв'язок...")
                if self._connect():
                    print("✅ [Kafka] Зв'язок відновлено!")
                self.retry_counter = 0

        if self.active:
            try:
                self.producer.send(self.topic, data).get(timeout=1)
                print(f"[KAFKA] | {year} | OK | Доставлено у брокер")
            except:
                self.active = False
                print(f"⚠️ [Kafka -> Lost] Зв'язок розірвано!")
                self._print_imitation(year, cause)
        else:
            self._print_imitation(year, cause)

    def _print_status(self):
        if self.active:
            print("✅ СТАТУС: KAFKA ONLINE")
        else:
            print("⚠️ СТАТУС: KAFKA OFFLINE (Режим імітації)")

    def _print_imitation(self, year, cause):
        print(f"[KAFKA-IMITATION] | {year} | {cause[:45]}...")
