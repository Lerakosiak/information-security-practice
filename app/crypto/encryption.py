from cryptography.fernet import Fernet, InvalidToken
from app.crypto.key_manager import get_encryption_key

def get_fernet() -> Fernet:
    """Створює об'єкт Fernet з поточним ключем."""
    return Fernet(get_encryption_key())

def encrypt_field(value: str) -> str:
    """Шифрує рядкове значення."""
    if not value:
        return value
    f = get_fernet()
    return f.encrypt(value.encode("utf-8")).decode("utf-8")

def decrypt_field(encrypted_value: str) -> str:
    """Розшифровує значення."""
    if not encrypted_value:
        return encrypted_value
    try:
        f = get_fernet()
        return f.decrypt(encrypted_value.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        return "[ПОМИЛКА РОЗШИФРУВАННЯ: невірний ключ]"