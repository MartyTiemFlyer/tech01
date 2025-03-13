# tests/test_http_message.py
import pytest
from src.http.http_message import HttpRequest, HttpResponse

def test_http_request_to_bytes():
    """ Тест to_bytes(): превращает HTTP-запрос в байтовую строку перед отправкой по сети. """
    
    request = HttpRequest(
        method="POST",
        path="/send_sms",
        headers={"Content-Type": "application/json"},
        body='{"message": "Hello"}'
    )

    request_bytes = request.to_bytes()
    assert b"POST /send_sms" in request_bytes
    assert b"Content-Type: application/json" in request_bytes
    assert b'{"message": "Hello"}' in request_bytes

def test_http_response_from_bytes():
    """Тест from_bytes(): парсит полученный HTTP-ответ в объект Python."""
    
    response_bytes = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"success\"}"
    response = HttpResponse.from_bytes(response_bytes)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.body == '{"status": "success"}'
