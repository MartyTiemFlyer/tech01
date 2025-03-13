# src/main.py
# Запуск: python -m src.main --sender {sender_name} --receiver {receiver_name} --message "{message}"
# Пример: python -m src.main --sender 123456789 --receiver 987654321 --message "Привет, мир!"

import asyncio
from urllib.parse import urlparse
from src.http.http_request import HttpRequester
from src.config_loader import load_config
from src.cli import parse_args
import logging

# Настройка логирования
logging.basicConfig(
    filename="sms_sender.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def main():
    """Основная логика программы: загрузка конфигурации, парсинг аргументов и отправка запроса."""
    
    config = load_config()
    
    args = parse_args()
    logging.info(f"Запуск программы: sender={args.sender}, receiver={args.receiver}, message={args.message}")

    parsed_url = urlparse(config["sms_service"]["url"])
    host = parsed_url.hostname
    port = parsed_url.port or 4010

    username = config["sms_service"]["username"]
    password = config["sms_service"]["password"]

    data = {
        "sender": args.sender,
        "recipient": args.receiver,
        "message": args.message
    }

    async def send_sms():
        """Асинхронная отправка SMS с обработкой ошибок."""
        requester = HttpRequester(host, port, username, password)
        try:
            response = await requester.send_request("/send_sms", data)
            
            print(f"Код ответа: {response.status_code}")
            print("Тело ответа:", response.body)

            logging.info(f"Успешно отправлено SMS: {data}")
            logging.info(f"Ответ сервера: {response.status_code}, {response.body}")

        except Exception as e:
            logging.error(f"Ошибка при отправке SMS: {e}")
            print("Ошибка при отправке SMS. Проверьте лог.")

    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(send_sms())
    finally:
        loop.close()

if __name__ == "__main__":
    main()
