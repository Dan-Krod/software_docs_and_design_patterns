import argparse
import json
from src.core.reader import CSVReader
from src.core.exporter import DataExporter
from src.factory import StrategyFactory

def main():
    parser = argparse.ArgumentParser(description="NYC Death Data Exporter")
    parser.add_argument('-s', '--strategy', type=str, 
                        help="Вибір стратегії: console, kafka, redis, file")
    args = parser.parse_args()

    with open('config/settings.json', 'r') as f:
        config = json.load(f)

    selected_strategy = args.strategy or config.get("strategy", "console")

    strategy = StrategyFactory.get_strategy(selected_strategy)

    reader = CSVReader(config['data_path'])
    exporter = DataExporter(reader, strategy)
    exporter.run()

if __name__ == "__main__":
    main()