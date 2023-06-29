"""
Пакет для работы с лексической статистикой.

Классы:
------
`LexicalAnalyzer`
    Лексический анализатор с возможностью усреднения статистик нескольких текстов. 
`LexicalStatistic`
    Лексическая статистика (результат анализа)

Модули:
-------
`words_frequency`
    Модуль для работы с частотной статистикой слов.
"""



from __future__ import annotations
from .words_frequency import FrequencyStatistic, WordsFreqAnalyzer
from ..utils import shift_right

class LexicalAnalyzer:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def text(text: str) -> LexicalStatistic:
        return LexicalStatistic(WordsFreqAnalyzer.text(text))
    
    @staticmethod
    def average(stats: list[LexicalStatistic]) -> LexicalStatistic:
        freq_stats_list : list[FrequencyStatistic] = []
        for stat in stats:
            freq_stats_list.append(stat.words_freq)
        return LexicalStatistic(WordsFreqAnalyzer.average(stats=freq_stats_list))

class LexicalStatistic:

    def __init__(self, analyzer: WordsFreqAnalyzer) -> None:
        self.__frequency_stat: FrequencyStatistic | None = None
        self.__freq_analyzer : WordsFreqAnalyzer = analyzer

    @property
    def words_freq(self) -> FrequencyStatistic:
        if not self.__frequency_stat:
            self.__frequency_stat = self.__freq_analyzer.analyze()
        return self.__frequency_stat

    def __str__(self) -> str:
        return 'Лексический анализ:\n\n' + shift_right('\n\n'.join(map(str, (self.words_freq,))))