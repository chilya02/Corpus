from __future__ import annotations
import re
import pandas as pd
from ..utils import delete_empty_rows, shift_right


class WordStat:
    """Статистика по слову"""

    def __init__(self, word: str, count: int, total_words_count: int) -> None:
        self.__word: str = word
        self.__count: int = count
        self.__total_words_count: int = total_words_count

    @property
    def word(self) -> str:
        '''Слово'''
        return self.__word

    @property
    def relative(self) -> float:
        '''Доля слов от общего количества'''
        return round(self.__count / self.__total_words_count, 5)

    @property
    def count(self) -> int:
        '''Количество слов'''
        return self.__count

    def __str__(self) -> str:
        return str(self.relative)


class FrequencyStatistic:
    '''Частотная статистика слов'''

    def __init__(self, words: list[WordStat]) -> None:
        self.__words: list[WordStat] = words
        self.__sorted: bool = False

    def __str__(self) -> str:
        return 'Частотная статистика слов:\n\n' + shift_right('\n'.join(f'{index + 1}\t{word.count}\t{word.relative}\t{word.word}' for index, word in enumerate(sorted(self, key=lambda word_: word_.count, reverse=True))))

    def __len__(self):
        return len(self.__words)

    def __getitem__(self, key: str) -> WordStat:
        if not self.__sorted:
            self.__words.sort(key=lambda word: word.word)
            self.__sorted = True
        first = 0
        last = len(self.__words) - 1
        word = key.lower()
        while (first <= last):
            mid = (first + last) // 2
            if self.__words[mid].word > word:
                last = mid - 1
            elif self.__words[mid].word < word:
                first = mid + 1
            elif self.__words[mid].word == word:   
                return self.__words[mid]
        raise KeyError

    def __iter__(self):
        for word in sorted(self.__words, key=lambda word_: word_.count, reverse=True):
            yield word

    def as_df(self) -> pd.DataFrame:
        df = pd.DataFrame(
            [word.word, word.count, word.relative] for word in sorted(self.__words, key=lambda word_: word_.count, reverse=True)
        )
        df.columns = ['Слово', 'Количество', 'доля']
        df.index = [x for x in range(1, len(self.__words) + 1)]
        return df

class WordsFreqAnalyzer:
    def __init__(self, type: str, arg: str | list[FrequencyStatistic]) -> None:
        self.__arg: str | list[FrequencyStatistic] = arg
        self.__type : str = type
    
    @staticmethod
    def text(text: str) -> WordsFreqAnalyzer:
        return WordsFreqAnalyzer(type='text', arg=text)
    
    @staticmethod
    def average(stats: list[FrequencyStatistic]) -> WordsFreqAnalyzer:
        return WordsFreqAnalyzer(type='average', arg=stats)

    def analyze(self) -> FrequencyStatistic:
        if self.__type == 'text':
            stat = self.__text_analyze()
        else:
            stat = self.__average_analyze()
        
        words_stat, total_words_count = stat
        result: list[WordStat] = []
        for word in words_stat:
            result.append(WordStat(word=word, count=words_stat[word], total_words_count=total_words_count))
        return FrequencyStatistic(words=result)

    def __text_analyze(self) -> tuple[dict[str, int], int]:
        text = delete_empty_rows(
            re.sub(
                r'[<-]',
                '',
                re.sub(
                    r'''[\(\)\.,!"'\[\]«»—–:;…?\|]''',
                    ' ', 
                    self.__arg
                )
            )
        )
        total_words_count = 0
        words: dict[str, int] = {}
        for row in text.split('\n'):
            for word in re.split(r'\s+', row.strip(' ')):
                total_words_count += 1
                clean_word = re.sub('ё', 'е',word.lower())
                try:
                    words[clean_word] += 1
                except KeyError:
                    words[clean_word] = 1
        return (words, total_words_count)
        
    
    def  __average_analyze(self) -> tuple[dict[str, int], int]:
        total_words_count = 0

        words: dict[str, int] = {}

        for stat in self.__arg:
            for word in stat:
                total_words_count += word.count
                try:
                    words[word.word] += word.count
                except KeyError:
                    words[word.word] = word.count
        return (words, total_words_count)