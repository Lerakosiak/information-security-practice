from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Логін: 3-30 символів, лише латиниця, цифри та _"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError("Логін може містити лише латинські літери, цифри та _")
        return value

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        if re.search(r"[<>&\"']", value):
            raise ValueError("Ім’я не може містити HTML-символи")
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль має містити хоча б одну велику літеру")
        if not re.search(r"[a-z]", value):
            raise ValueError("Пароль має містити хоча б одну малу літеру")
        if not re.search(r"\d", value):
            raise ValueError("Пароль має містити хоча б одну цифру")
        return value


class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=300)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        if re.search(r"[<>&\"']", value):
            raise ValueError("HTML-теги та спеціальні символи заборонені")
        return value.strip()

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str