from typing import Optional
from ninja import Schema


class CustomResponse(Schema):
    success: Optional[str] = None
    error: Optional[str] = None
