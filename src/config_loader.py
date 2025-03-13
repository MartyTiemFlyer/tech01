# src/config_loader.py

import toml
from pathlib import Path

def load_config():
    """
    Загружает конфигурацию из файла config.toml.

    Возвращает:
        dict: Словарь с конфигурационными данными.
    """
    
    config_path = Path(__file__).parent.parent / "config" / "config.toml"

    with open(config_path, "r", encoding="utf-8") as config_file:
        config = toml.load(config_file)

    return config