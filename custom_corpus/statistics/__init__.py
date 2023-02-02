'''Сущности результатов анализа разных видов'''

from .rhytmic import RhytmicStatistic, TextRhytmicStatistic, CorpusRhytmicStatistic
from .morphological import MorphologicalStatistic, TextMorphologicalStatistic, CorpusMorphologicalStatistic
from .lexical import LexicalStatistic, TextLexicalStatistic, CorpusLexicalStatistic
from .graphical import GraphicalStatistic, TextGraphcalStatistic, CorpusGraphicalStatistic


class Statistic:
    """Результат анализа"""

    def __init__(self) -> None:
        self._rhythmic: RhytmicStatistic
        self._morphological: MorphologicalStatistic
        self._lexical: LexicalStatistic
        self._graphical: GraphicalStatistic

    def __str__(self) -> str:
        return 'Статистика:\n\n' + '\n\n'.join(map(str, (self.graphical, self.morphological, self.rhythmic, self.lexical)))
    
    @property
    def rhythmic(self) -> RhytmicStatistic:
        """Ритмический анализ"""

        return self._rhythmic

    @property
    def morphological(self) -> MorphologicalStatistic:
        """Морфологический анализ"""

        return self._morphological
    
    @property
    def lexical(self) -> LexicalStatistic:
        """Лексический анализ"""

        return self._lexical
    
    @property
    def graphical(self) -> GraphicalStatistic:
        """Графический анализ"""

        return self._graphical


class TextStatistic(Statistic):
    """Результат анализа"""
    
    def __init__(self, text: str, steps: int) -> None:
        super().__init__()
        self._rhythmic = TextRhytmicStatistic(text=text, steps=steps)
        self._morphological = TextMorphologicalStatistic(text=text)
        self._lexical = TextLexicalStatistic(text=text)
        self._graphical = TextGraphcalStatistic(text=text)


class CorpusStatistic(Statistic):
    """Результат анализа"""

    def __init__(self, text_statistic_list: list[TextStatistic], steps: int) -> None:
        super().__init__()
        rhythmic_stats: list[TextRhytmicStatistic] = []
        morphological_stats: list[TextMorphologicalStatistic] = []
        lexical_stats: list[TextLexicalStatistic] = []
        graphical_stats: list[TextGraphcalStatistic] = []
        for stat in text_statistic_list:
            rhythmic_stats.append(stat.rhythmic)
            morphological_stats.append(stat.morphological)
            lexical_stats.append(stat.lexical)
            graphical_stats.append(stat.graphical)
        self._rhythmic = CorpusRhytmicStatistic(stats=rhythmic_stats, steps=steps)
        self._morphological = CorpusMorphologicalStatistic(stats=morphological_stats)
        self._lexical = CorpusLexicalStatistic(stats=lexical_stats)
        self._graphical = CorpusGraphicalStatistic(stats=graphical_stats)
