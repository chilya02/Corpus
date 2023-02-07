"""
Модуль утилит для работы с текстом

Содержит функции:
    * delete_empty_rows(text: str)
"""

import re


def delete_empty_rows(text: str) -> str:
    """Удаляет пустые строки из текста"""

    return re.sub(r'\n\s*\n', '\n', text).strip('\n')

def shift_right(text: str) -> str:
    rows = text.split('\n')
    result: list[str] = []
    for row in rows:
        result.append(' ' + row)
    return '\n'.join(result)