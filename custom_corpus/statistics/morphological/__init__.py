from .POS_stat import PosStat, PosAnalyzer
from progress.bar import IncrementalBar
from .verbs_tense import VerbsTensesStat
from ..utils import shift_right

class MorphologicalStatistic:
    def __init__(self, pos_analyzer: PosAnalyzer) -> None:
        self.__pos_statistic: PosStat | None = None
        self.__pos_analyzer = pos_analyzer
        self.__verbs_tenses: VerbsTensesStat | None = None

    @property
    def POS(self) -> PosStat: 
        if not self.__pos_statistic:
            self.__pos_statistic = self.__pos_analyzer.analyze()
        return self.__pos_statistic
    
    @property
    def verbs_tenses(self) -> VerbsTensesStat:
        if not self.__verbs_tenses:
            self.__verbs_tenses = VerbsTensesStat(self.POS)
        return self.__verbs_tenses

    def __str__(self) -> str:
        return 'Морфологический анализ:\n\n' + shift_right('\n\n'.join(map(str, (self.POS, self.verbs_tenses))))

class MorphologicalAnalyzer:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def text(text: str) -> MorphologicalStatistic:
        return MorphologicalStatistic(pos_analyzer=PosAnalyzer.text(text=text))
    
    @staticmethod
    def average(stats: list[MorphologicalStatistic]) -> MorphologicalStatistic:
        pos_stats: list[PosStat] = []
        for stat in stats:
            pos_stats.append(stat.POS)
        return MorphologicalStatistic(pos_analyzer=PosAnalyzer.average(stats=pos_stats))
 