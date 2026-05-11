import bleach
import re


def sanitize_text(text: str) -> str:
    """
    Видаляє HTML-теги з тексту.
    Потрібно для захисту від XSS.
    """
    cleaned = bleach.clean(text, tags=[], strip=True)
    return cleaned.strip()


def contains_sql_patterns(text: str) -> bool:
    """
    Перевіряє підозрілі SQL-патерни.
    """
    sql_patterns = [
        r"(\b(UNION|SELECT|INSERT|DELETE|DROP)\b)",
        r"(--|;|\/\*|\*\/)",
        r"(\bOR\b\s+\b1\s*=\s*1\b)",
    ]

    for pattern in sql_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False