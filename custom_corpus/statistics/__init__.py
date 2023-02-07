"""
Пакет для работы со статистикой

Классы:
------
`Statistic`
    Статистика (родительский класс)
`TextStatistic(Statistic)`
    Статистика текста
`CorpusStatistic(Statistic)`
    Статистика корпуса

Модули:
-------
`utils`
    Утилиты для работы с текстом

Пакеты:
------
`statistic.rhythmic`
    Пакет для работы с ритмикой
`statistic.lexical`
    Пакет для работы с лексикой
`statistic.morphological`
    Пакет для работы с морфлогией
`statistic.graphical`
    Пакет для работы с графической информацией
"""

from .rhytmic import RhythmicStatistic, RhythmicAnalyzer
from .morphological import MorphologicalStatistic, MorphologicalAnalyzer
from .lexical import LexicalStatistic, LexicalAnalyzer
from .graphical import GraphicalStatistic, GraphicalAnalyzer
from .utils import shift_right

class Statistic:
    """Статистика
    
    Атрибуты
    --------

    rhythmic : `RhythmicStatistic`
        Анализ ритмики
    lexical : `LexicalStatistic`
        Анализ лексики
    morpholgical : `MorphologicalStatistic`
        Анализ морфологии
    graphical : `GraphicalStatistic`
        Графический анализ
    
    Примеры
    -------

    Вывод объектов статистики:
    
        >>> print(text_or_corpus.statistic)
        #Выведет всю статистику текста или корпуса
        >>> print(text_or_corpus.statistic.rhythmic)
        #Выведет только ритмическую статистику

    Обращение к объектам статистики:

        >>> text_or_corpus.statistic
        <custom_corpus.statistics.Statistic at 0x7f4e98690c50>
        >>> text_or_corpus.statistic.lexical
        <custom_corpus.statistics.lexical.LexicalStatistic at 0x7f4e98969410> 
    """

    def __init__(
            self, 
            rhythmic: RhythmicStatistic,
            lexical: LexicalStatistic, 
            morphological: MorphologicalStatistic, 
            graphical: GraphicalStatistic
        ) -> None:
        
        self.__rhythmic: RhythmicStatistic = rhythmic
        self.__morphological: MorphologicalStatistic = morphological
        self.__lexical: LexicalStatistic = lexical
        self.__graphical: GraphicalStatistic = graphical

    def __str__(self) -> str:
        return 'Статистика:\n\n' + shift_right('\n\n'.join(map(str, (self.rhythmic, self.lexical, self.morphological, self.graphical))))
    
    @property
    def rhythmic(self) -> RhythmicStatistic:
        """Ритмический анализ"""

        return self.__rhythmic

    @property
    def morphological(self) -> MorphologicalStatistic:
        """Морфологический анализ"""

        return self.__morphological
    
    @property
    def lexical(self) -> LexicalStatistic:
        """Лексический анализ"""

        return self.__lexical
    
    @property
    def graphical(self) -> GraphicalStatistic:
        """Графический анализ"""

        return self.__graphical


class Analyzer:
    
    @staticmethod
    def text(text: str, steps: int) -> Statistic:
        return Statistic(
            RhythmicAnalyzer.text(text, steps=steps),
            LexicalAnalyzer.text(text=text),
            MorphologicalAnalyzer.text(text=text),
            GraphicalAnalyzer.text(text)
        )

    @staticmethod
    def average(stats: list[Statistic], steps: int) -> Statistic:
        rhythmic_stats: list[RhythmicStatistic] = []
        morphological_stats: list[MorphologicalStatistic] = []
        lexical_stats: list[LexicalStatistic] = []
        graphical_stats: list[GraphicalStatistic] = []
        for stat in stats:
            rhythmic_stats.append(stat.rhythmic)
            morphological_stats.append(stat.morphological)
            lexical_stats.append(stat.lexical)
            graphical_stats.append(stat.graphical)
        return Statistic(
            RhythmicAnalyzer.average(rhythmic_stats, steps=steps),
            LexicalAnalyzer.average(lexical_stats),
            MorphologicalAnalyzer.average(morphological_stats),
            GraphicalAnalyzer.average(graphical_stats)
        )