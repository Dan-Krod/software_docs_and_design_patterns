import json
from src.strategies.console_strategy import ConsoleStrategy
from src.strategies.kafka_strategy import KafkaStrategy
from src.strategies.redis_strategy import RedisStrategy
from src.strategies.file_strategy import FileStrategy
from src.strategies.firebase_strategy import FirebaseStrategy

class StrategyFactory:
    @staticmethod
    def get_strategy(target=None):
        if target is None:
            with open('config/settings.json', 'r') as f:
                config = json.load(f)
            target = config.get("strategy", "console").lower()
        else:
            target = target.lower()
            
        if target == "console":
            return ConsoleStrategy()
        elif target == "file":
            return FileStrategy()
        elif target == "kafka":
            return KafkaStrategy()
        elif target == "redis":
            return RedisStrategy()
        elif target == "firebase":
            return FirebaseStrategy()
        
        print(f"⚠️ Стратегію {target} не знайдено. Використовую Console.")
        return ConsoleStrategy()