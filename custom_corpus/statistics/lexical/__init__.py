from .words_frequency import FrequencyStatistic, TextFrequencyStatistic, CorpusFrequencyStatistic
from ..utils import delete_empty_rows
import re

class LexicalStatistic:

    def __init__(self) -> None:
        self.__frequency_stat: FrequencyStatistic | None = None

    @property
    def words_freq(self) -> FrequencyStatistic:
        pass

    def __str__(self) -> str:
        return 'Лексический анализ:\n\n' + '\n\n'.join(map(str, (self.words_freq,)))


class TextLexicalStatistic(LexicalStatistic):

    def __init__(self, text: str) -> None:
        super().__init__()
        self.__text: str = delete_empty_rows(
            re.sub(
                r'[<-]',
                '',
                re.sub(
                    r'''[\(\)\.,!"'\[\]«»—–:;…?\|]''',
                    ' ', 
                    text
                )
            )
        )
        self.__frequency_stat: TextFrequencyStatistic | None = None
    
    @property
    def words_freq(self) -> TextFrequencyStatistic:
        if not self.__frequency_stat:
            self.__frequency_stat = TextFrequencyStatistic(self.__text)
        return self.__frequency_stat

    
class CorpusLexicalStatistic(LexicalStatistic):

    def __init__(self, stats: list[TextLexicalStatistic]) -> None:
        super().__init__()
        self.__frequency_stat: CorpusFrequencyStatistic | None = None
        self.__texts_stats: list[TextLexicalStatistic] = stats
    
    @property
    def words_freq(self) -> CorpusFrequencyStatistic:
        if not self.__frequency_stat:
            freq_stats_list: list[TextFrequencyStatistic] = []
            for stat in self.__texts_stats:
                freq_stats_list.append(stat.words_freq)
            self.__frequency_stat = CorpusFrequencyStatistic(freq_stats_list)
        return self.__frequency_stat
    
    