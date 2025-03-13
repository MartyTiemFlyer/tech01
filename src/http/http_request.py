# http/http_request.py

import asyncio
import base64
import json
import logging
from src.http.http_message import HttpRequest, HttpResponse

class HttpRequester:
    """
    Отвечает за отправку HTTP-запросов вручную. 
    Работает через asyncio.open_connection.
    """
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username 
        self.password = password  
    
    async def send_request(self, path: str, data: dict) -> HttpResponse:
        """
        Устанавливает соединение с сервером.
        Формирует правильный HTTP-запрос с учетом аутентификации.
        Отправляет запрос, получает и разбирает ответ.
        
        Аргументы:
            path (str): Путь к API (например, "/send_sms").
            data (dict): Тело запроса в формате JSON.
        
        Возвращает:
            HttpResponse: Разобранный HTTP-ответ.
        """
        # Подключение к серверу
        reader, writer = await asyncio.open_connection(self.host, self.port)

        body = json.dumps(data)

        # Кодируем аутентификацию в Base64
        auth_header = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

        # Объект HTTP-запроса
        request = HttpRequest(
            method="POST",
            path=path,
            headers={
                "Host": self.host,
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json",
                "Content-Length": str(len(body))
            },
            body=body
        )

        logging.info(f"Отправка запроса: {request.method} {path}, заголовки={request.headers}, тело={body}")
        
        writer.write(request.to_bytes())
        await writer.drain()

        response_data = await reader.read()
        writer.close()
        await writer.wait_closed()
        
        response = HttpResponse.from_bytes(response_data)
        logging.info(f"Получен ответ: код={response.status_code}, заголовки={response.headers}, тело={response.body}")

        return response


