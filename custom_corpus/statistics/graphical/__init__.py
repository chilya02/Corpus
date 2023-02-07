import re
from ..utils import shift_right

class GraphicalStatistic:
    def __init__(self, alphabetical_symbols_count: int, total_words_count: int) -> None:
        self.__total_words_count: int = total_words_count
        self.__alphabetical_symbols_count: int = alphabetical_symbols_count
    
    def __str__(self) -> str:
        return 'Графический анализ:\n\n' + shift_right('Средняя длина слов:\n\n' + shift_right(str(self.average_words_length)))

    @property
    def average_words_length(self) -> float:
        return round(self.alphabetical_symbols_count / self.total_words_count, 5)
    
    @property
    def total_words_count(self) -> int:
        return self.__total_words_count

    @property
    def alphabetical_symbols_count(self) -> int:
        return self.__alphabetical_symbols_count


class GraphicalAnalyzer:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def text(text: str) -> GraphicalStatistic:
        clean_text = re.sub(r'<', '', text)
        clean_text = re.sub(r'''[\(\)\.,!"'\[\]«»—:;…?\|\n]''', ' ', clean_text)
        total_words_count = len(re.split(r'\s+', clean_text.strip(' ')))
        alphabetical_symbols_count = len(re.sub(r'\s+', '', clean_text))
        return GraphicalStatistic(alphabetical_symbols_count=alphabetical_symbols_count, total_words_count=total_words_count)
    
    @staticmethod
    def average(stats: list[GraphicalStatistic]) -> GraphicalStatistic:
        total_words_count = 0
        alphabetical_symbols_count = 0
        for stat in stats:
            total_words_count += stat.total_words_count
            alphabetical_symbols_count += stat.alphabetical_symbols_count
        return GraphicalStatistic(alphabetical_symbols_count=alphabetical_symbols_count, total_words_count=total_words_count)
