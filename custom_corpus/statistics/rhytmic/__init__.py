"""
Пакет для работы с ритмической статистикой

Классы:
-------
`RhythmicAnalyzer`
    Ритмический анализатор с возможностью усреднения статистик нескольких текстов
`RhythmicStatistic`
    Ритмическая статистика (результат анализа)

Модули:
`rhythmic_words`
    Модуль для работы с ритмическими словами
`stressness_profile`
    Модуль для работы с профилем ударности
"""


from .stressness_profile import StressnessProfile, StressnessProfileAnalyzer
from .rhytmic_words import RhythmicWords, RhythmicWordsAnalyzer
from ..utils import shift_right
class RhythmicStatistic:
    '''Ритмический анализ'''
    
    def __init__(self, stressness_profile_analyzer: StressnessProfileAnalyzer, rhythmic_words_analyzer: RhythmicWordsAnalyzer) -> None:
        self.__stressness_profile: StressnessProfile | None = None
        self.__rhytmic_words: RhythmicWords | None = None
        self.__stressness_profile_analyzer: StressnessProfileAnalyzer = stressness_profile_analyzer
        self.__rhytmic_words_analyzer: RhythmicWordsAnalyzer = rhythmic_words_analyzer

    @property 
    def rhytmic_words(self) -> RhythmicWords:
        if not self.__rhytmic_words:
            self.__rhytmic_words = self.__rhytmic_words_analyzer.analyze()
        return self.__rhytmic_words

    @property
    def stressness_profile(self) -> StressnessProfile:
        if not self.__stressness_profile:
            self.__stressness_profile = self.__stressness_profile_analyzer.analyze()
        return self.__stressness_profile

    def __str__(self) -> str:
        return 'Ритмический анализ:\n\n' + shift_right('\n\n'.join(map(str, (self.rhytmic_words, self.stressness_profile))))

class RhythmicAnalyzer:

    def __init__(self) -> None:
        pass

    @staticmethod
    def text(text: str, steps: int) -> RhythmicStatistic:
        return RhythmicStatistic(
            stressness_profile_analyzer=StressnessProfileAnalyzer.text(
                text=text, 
                steps=steps
            ),
            rhythmic_words_analyzer=RhythmicWordsAnalyzer.text(
                text=text
            )
        )

    @staticmethod
    def average(stats: list[RhythmicStatistic], steps: int) -> RhythmicStatistic:
        rhytmic_words_stats: list[RhythmicWords] = []
        stressness_profile_stats: list[StressnessProfile] = []
        for stat in stats:
            rhytmic_words_stats.append(stat.rhytmic_words)
            stressness_profile_stats.append(stat.stressness_profile)
        return RhythmicStatistic(
            stressness_profile_analyzer=StressnessProfileAnalyzer.average(
                stats=stressness_profile_stats, 
                steps=steps
            ),
            rhythmic_words_analyzer=RhythmicWordsAnalyzer.average(
                stats=rhytmic_words_stats
            )
        )
