from .POS_stat import PosStat, TextPosStat, CorpusPosStat
from progress.bar import IncrementalBar
from .verbs_tense import VerbsTensesStat


class MorphologicalStatistic:
    def __init__(self) -> None:
        self.__pos_statistic: PosStat | None = None
        self.__verbs_tenses: VerbsTensesStat | None = None

    @property
    def POS(self) -> PosStat: 
        pass
    
    @property
    def verbs_tenses(self) -> VerbsTensesStat:
        if not self.__verbs_tenses:
            self.__verbs_tenses = VerbsTensesStat(self.POS)
        return self.__verbs_tenses

    def __str__(self) -> str:
        return 'Морфологический анализ:\n\n' + '\n\n'.join(map(str, (self.POS, self.verbs_tenses)))

    
        
class TextMorphologicalStatistic(MorphologicalStatistic):
    
    def __init__(self, text: str) -> None:
        super().__init__()
        self.__pos_statistic: TextPosStat | None = None
        self.__text = text
    
    @property
    def POS(self) -> TextPosStat:
        if not self.__pos_statistic:
            self.__pos_statistic = TextPosStat(self.__text)
        return self.__pos_statistic
    
    
class CorpusMorphologicalStatistic(MorphologicalStatistic):
    
    def __init__(self, stats: list[TextMorphologicalStatistic]) -> None:
        super().__init__()
        self.__pos_statistic: CorpusPosStat | None = None
        self.__texts_stats: list[TextMorphologicalStatistic] = stats
    
    @property
    def POS(self) -> CorpusPosStat:
        if not self.__pos_statistic:
            POS_stats: list[TextPosStat] = []
            with IncrementalBar(max=len(self.__texts_stats), message='POS Analyze') as bar:
                for POS_stat in self.__texts_stats:
                    POS_stats.append(POS_stat.POS)
                    bar.next()
                bar.finish()
                print("\033[A                                                         \033[A\033[A")
                self.__pos_statistic = CorpusPosStat(POS_stats)
        return self.__pos_statistic