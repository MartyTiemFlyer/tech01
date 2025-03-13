# http/http_message.py


class HttpRequest:
    def __init__(self, method: str, path: str, headers: dict, body: str = ""):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        """Формирует HTTP-запрос в виде байтов."""
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        return (request_line + headers + "\r\n" + self.body).encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        """Создает объект запроса из байтов."""
        lines = binary_data.decode("utf-8").split("\r\n")
        method, path, _ = lines[0].split(" ")
        headers = {}
        body = ""

        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ", 1)
            headers[key] = value

        if "" in lines:
            body = "\r\n".join(lines[lines.index("") + 1:])

        return cls(method, path, headers, body)


class HttpResponse:
    def __init__(self, status_code: int, headers: dict, body: str):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        """Разбирает HTTP-ответ из байтов."""
        lines = binary_data.decode("utf-8").split("\r\n")
        status_line = lines[0]
        _, status_code, _ = status_line.split(" ", 2)
        headers = {}
        body = ""

        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ", 1)
            headers[key] = value

        if "" in lines:
            body = "\r\n".join(lines[lines.index("") + 1:])

        return cls(int(status_code), headers, body)
