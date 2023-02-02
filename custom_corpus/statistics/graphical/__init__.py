import re

class GraphicalStatistic:
    def __init__(self) -> None:
        self._total_words_count: int = 0
        self._alphabetical_symbols_count: int = 0
    
    def __str__(self) -> str:
        return 'Графический анализ:\n\n' + 'Средняя длина слов:\n' + str(self.average_words_length)

    @property
    def average_words_length(self) -> float:
        return round(self.alphabetical_symbols_count / self.total_words_count, 5)
    
    @property
    def total_words_count(self) -> int:
        return self._total_words_count

    @property
    def alphabetical_symbols_count(self) -> int:
        return self._alphabetical_symbols_count

class TextGraphcalStatistic(GraphicalStatistic):
    def __init__(self, text: str) -> None:
        clean_text = re.sub(r'<', '', text)
        clean_text = re.sub(r'''[\(\)\.,!"'\[\]«»—:;…?\|\n]''', ' ', clean_text)
        self._total_words_count = len(re.split(r'\s+', clean_text.strip(' ')))
        self._alphabetical_symbols_count = len(re.sub(r'\s+', '', clean_text))
        

class CorpusGraphicalStatistic(GraphicalStatistic):
    def __init__(self, stats: list[TextGraphcalStatistic]) -> None:
        super().__init__()
        for stat in stats:
            self._total_words_count += stat._total_words_count
            self._alphabetical_symbols_count += stat._alphabetical_symbols_count