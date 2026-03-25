import os
from src.interfaces.base_strategy import BaseStrategy


class FileStrategy(BaseStrategy):
    def __init__(self, filename="data/output.txt"):
        self.filename = filename
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write("--- NYC Death Data Export Start ---\n")

    def send(self, data: dict):
        year = data.get('Year', '????')
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f"{data}\n")
        print(f"[FILE] Записано рік {year} у {self.filename}")
