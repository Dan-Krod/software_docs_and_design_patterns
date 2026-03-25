import pandas as pd


class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_rows(self, limit=10):
        try:
            df = pd.read_csv(self.file_path)
            df_subset = df.head(limit)
            for _, row in df_subset.iterrows():
                yield row.to_dict()
        except FileNotFoundError:
            print(f"❌ Помилка: Файл {self.file_path} не знайдено!")
            return []
