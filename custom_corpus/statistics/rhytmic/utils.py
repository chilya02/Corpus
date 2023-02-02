import re
def extract_vowels_with_accents(string: str) -> list:
    '''
        Принимает на вход строку размеченного текста.
        Возвращает список гласных входной строки + символ '<', если гласная в сильной позиции
    '''

    matches = re.findall(r'[аоуыэяёюиеАОУЫЭЯЁЮИЕ]<?', string=string)
    result = []
    for match in matches:
        result.append(match)
    return result
