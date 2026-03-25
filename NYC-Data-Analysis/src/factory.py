import json
from src.strategies.console_strategy import ConsoleStrategy
from src.strategies.console_strategy import ConsoleStrategy
from src.strategies.file_strategy import FileStrategy


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

        print(f"⚠️ Стратегію {target} не знайдено. Використовую Console.")
        return ConsoleStrategy()
