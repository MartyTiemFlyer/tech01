# src/cli.py

import argparse

def parse_args():
    """
    Парсит аргументы командной строки.

    Возвращает:
        argparse.Namespace: Объект с аргументами.
    """

    parser = argparse.ArgumentParser(description="Отправка SMS через API.")

    parser.add_argument(
        "--sender", "-s",
        type=str,
        required=True,
        help="Номер отправителя SMS."
    )
    parser.add_argument(
        "--receiver", "-r",
        type=str,
        required=True,
        help="Номер получателя SMS."
    )
    parser.add_argument(
        "--message", "-m",
        type=str,
        required=True,
        help="Текст SMS сообщения."
    )

    args = parser.parse_args()
    return args