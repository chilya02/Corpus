import re


def delete_empty_rows(text: str) -> str:
    """Удаляет пустые строки из текста"""

    return re.sub(r'\n\s*\n', '\n', text).strip('\n')
