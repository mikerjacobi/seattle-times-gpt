from dataclasses import dataclass


@dataclass
class Response:
    message: str


def handle_hello_world() -> Response:
    return Response("world")
