# src/tests/test_cli.py

import pytest
import sys
from src.cli import parse_args

def test_parse_args_valid():
    """ Проверяет, что parse_args корректно обрабатывает валидные аргументы. """
    
    test_args = [
        "main.py", "--sender", "123",
        "--receiver", "456", 
        "--message", "Сообщение"
    ]
    sys.argv = test_args  
    
    args = parse_args()

    assert args.sender == "123"
    assert args.receiver == "456"
    assert args.message == "Сообщение"

def test_parse_args_missing_argument():
    """ Проверяет, что parse_args вызывает ошибку, если не хватает аргументов. """
    test_args = ["main.py", "--sender", "123", "--message", "Сообщение"]
    sys.argv = test_args 
    
    with pytest.raises(SystemExit): 
        parse_args()
