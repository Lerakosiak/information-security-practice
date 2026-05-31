import os
import sys

def get_encryption_key() -> bytes:
    """Отримує ключ шифрування зі змінної оточення."""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        print("КРИТИЧНА ПОМИЛКА: ENCRYPTION_KEY не встановлено!")
        sys.exit(1)
    return key.encode()