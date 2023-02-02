from .stressness_profile import StressnessProfile, TextStressnessProfile, CorpusStressnessProfile
from .rhytmic_words import RhythmicWords, TextRhythmicWords, CorpusRhythmicWords
from ..utils import delete_empty_rows
import re

class RhytmicStatistic:
    '''Ритмический анализ'''
    
    def __init__(self) -> None:
        self.__stressness_profile: StressnessProfile | None
        self.__rhytmic_words: RhythmicWords | None
    
    @property 
    def rhytmic_words(self) -> RhythmicWords:
        pass

    @property
    def stressness_profile(self) -> StressnessProfile:
        pass

    def __str__(self) -> str:
        return 'Ритмический анализ:\n\n' + '\n\n'.join(map(str, (self.rhytmic_words, self.stressness_profile)))

class TextRhytmicStatistic(RhytmicStatistic):
    '''Ритмическая статистика текста'''

    def __init__(self, text: str, steps: int) -> None:
        super().__init__()
        self.__stressness_profile: TextStressnessProfile | None = None
        self.__rhytmic_words: TextRhythmicWords | None = None
        self.__text: str = delete_empty_rows(re.sub(r'\(.*\)', '', text))
        self.__steps: int = steps
    
    @property 
    def rhytmic_words(self) -> TextRhythmicWords:
        """Ритмические слова"""

        if not self.__rhytmic_words:
            self.__rhytmic_words = TextRhythmicWords(text=self.__text)
        return self.__rhytmic_words
    
    @property 
    def stressness_profile(self) -> TextStressnessProfile:
        """Профиль ударности"""

        if not self.__stressness_profile:
            self.__stressness_profile = TextStressnessProfile(steps=self.__steps, text=self.__text)
        return self.__stressness_profile

class CorpusRhytmicStatistic(RhytmicStatistic):
    """Ритмическая статистика корпуса"""

    def __init__(self, stats: list[TextRhytmicStatistic], steps: int) -> None:
        super().__init__()
        self.__stressness_profile: CorpusStressnessProfile | None = None
        self.__rhytmic_words: CorpusRhythmicWords | None = None
        self.__texts_stats: list[TextRhytmicStatistic] = stats
        self.__steps: int = steps

    @property
    def stressness_profile(self) -> CorpusStressnessProfile:
        """Профиль ударности"""

        if not self.__stressness_profile:
            stressness_profiles: list[TextStressnessProfile] = []
            for text_stat in self.__texts_stats:
                stressness_profiles.append(text_stat.stressness_profile)
            self.__stressness_profile = CorpusStressnessProfile(steps=self.__steps, stats=stressness_profiles)
        return self.__stressness_profile
    
    @property
    def rhytmic_words(self) -> CorpusRhythmicWords:
        """Ритмический анализ"""

        if not self.__rhytmic_words:
            rhytmic_words_list: list[TextRhythmicWords] = []
            for stat in self.__texts_stats:
                rhytmic_words_list.append(stat.rhytmic_words)
            self.__rhytmic_words = CorpusRhythmicWords(stats=rhytmic_words_list)
        return self.__rhytmic_words        
