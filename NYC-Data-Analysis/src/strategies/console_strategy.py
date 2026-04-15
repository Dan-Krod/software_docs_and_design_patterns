from src.interfaces.base_strategy import BaseStrategy


class ConsoleStrategy(BaseStrategy):
    def send(self, data: dict):
        year = data.get('Year', '????')
        cause = data.get('Leading Cause', 'Unknown Cause')
        deaths = data.get('Deaths', '0')
        print(
            f"[CONSOLE] {year} | Смертей: {deaths.ljust(6)}| Причина: {cause[:40]}... ")
