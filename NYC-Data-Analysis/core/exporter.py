class DataExporter:
    def __init__(self, reader, strategy):
        self.reader = reader
        self.strategy = strategy

    def run(self):
        print("\n" + "="*40)
        print(
            f"📤 ЕКСПОРТ ДАНИХ (Стратегія: {self.strategy.__class__.__name__})")
        print("="*55)

        for row in self.reader.read_rows(limit=10):
            self.strategy.send(row)

        print("-"*55)
        print(f"[SUCCESS] Готово! Опрацьовано записів: 10")
        print("="*55)
        print(f"✅ Експорт завершено успішно")
        print("="*55 + "\n")
