import re
import pandas as pd

class WordStat:
    """Статистика по слову"""

    def __init__(self, word: str, count: int = 1) -> None:
        self.__word: str = word
        self.__count: int = count
        self.total_words_count: int = 0

    def add_word(self, count: int = 1):
        self.__count += count

    @property
    def word(self) -> str:
        '''Слово'''
        return self.__word

    @property
    def relative(self) -> float:
        '''Доля слов от общего количества'''
        return round(self.__count / self.total_words_count, 5)

    @property
    def count(self) -> int:
        '''Количество слов'''
        return self.__count

    def __str__(self) -> str:
        return str(self.relative)


class FrequencyStatistic:
    '''Частотная статистика слов'''

    def __init__(self) -> None:
        self._words: list[WordStat] = []
        self._sorted: bool = False

    def __str__(self) -> str:
        return 'Частотная статистика слов:\n' + '\n'.join(f'{index + 1}\t{word.count}\t{word.relative}\t{word.word}' for index, word in enumerate(sorted(self._words, key=lambda word_: word_.count, reverse=True)))

    def __len__(self):
        return len(self._words)

    def __getitem__(self, key: str) -> WordStat:
        if not self._sorted:
            self._words.sort(key=lambda word: word.word)
            self._sorted = True
        # for word in self._words:
        #     if word.word == key.lower():
        #         return word  
        first = 0
        last = len(self._words) - 1
        while (first <= last):
            mid = (first + last) // 2
            if self._words[mid].word > key.lower():
                last = mid - 1
            elif self._words[mid].word < key.lower():
                first = mid + 1
            elif self._words[mid].word == key.lower():   
                return self._words[mid]
        raise KeyError

    def __iter__(self):
        for word in sorted(self._words, key=lambda word_: word_.count, reverse=True):
            yield word

    def as_df(self) -> pd.DataFrame:
        df = pd.DataFrame(
            [word.word, word.count, word.relative] for word in sorted(self._words, key=lambda word_: word_.count, reverse=True)
        )
        df.columns = ['Слово', 'Количество', 'доля']
        df.index = [x for x in range(1, len(self._words) + 1)]
        return df
    
    def add_word_stat(self, word_stat: WordStat):
        self._words.append(word_stat)
        self._sorted = False


class TextFrequencyStatistic(FrequencyStatistic):
    '''Часотная статистика по тексту'''

    def __init__(self, text: str) -> None:
        super().__init__()
        total_words_count = 0
        for row in text.split('\n'):
            for word in re.split(r'\s+', row.strip(' ')):
                total_words_count += 1
                lower_case_word = re.sub('ё','е',word.lower())
                try:
                    self[lower_case_word].add_word()
                except KeyError:
                    self.add_word_stat(WordStat(lower_case_word))
        
        for word in self:
            word.total_words_count = total_words_count
    

class CorpusFrequencyStatistic(FrequencyStatistic):
    '''Частотная статистика слов по корпусу текстов'''

    def __init__(self, stats: list[TextFrequencyStatistic]) -> None:
        super().__init__()
        total_words_count = 0
        for stat in stats:
            for word in stat:
                total_words_count += word.count
                try:
                    self[word.word].add_word(word.count)
                except KeyError:
                    self.add_word_stat(WordStat(word=word.word, count=word.count))
        for word in self:
            word.total_words_count = total_words_count