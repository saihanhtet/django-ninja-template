from ninja import Schema
from pydantic import BaseModel, EmailStr


class SignInSchema(BaseModel):
    email: EmailStr
    password: str


class UserDetailSchema(Schema):
    id: int
    email: EmailStr
