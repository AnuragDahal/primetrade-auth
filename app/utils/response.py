from typing import Optional, Any


def send_response(message: str, data: Optional[Any] = None) -> dict:
    return {
        "status": "success",
        "message": message,
        "data": data
    }
