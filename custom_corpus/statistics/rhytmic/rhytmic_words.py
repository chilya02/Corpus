from __future__ import annotations
from .utils import extract_vowels_with_accents
import pandas as pd
import re
from ..utils import delete_empty_rows, shift_right

class AccentPosition:
    """Результат анализа ударений на определенном слоге"""

    def __init__(self, accent: int, count: int, total_words_count: int) -> None:
        self.__accent: int = accent
        self.__count: int = count
        self.__total_words_count = total_words_count

    @property
    def accent(self) -> int:
        return self.__accent
    
    def __str__(self) -> str:
        return str(self.relative)

    @property
    def count(self) -> int:
        return self.__count
    
    @property
    def relative(self) -> float:
        return round(self.__count / self.__total_words_count, 5)


class RhythmicWord:
    """Результат анализа ритмических слов определенной длины."""

    def __init__(self, length: int, accents: list[AccentPosition]):
        self.__accents: list[AccentPosition] = accents
        self.length = length

    def _add_accent(self, accent: AccentPosition) -> None:
        """Добавляет новый вариант ударения"""

        self.__accents.append(accent)

    def __str__(self) -> str:
        return '\n'.join(f'{self.length}.{accent.accent}\t{accent}' for accent in sorted(self.__accents, key=lambda x: x.accent))

    def __getitem__(self, key: int) -> float:
        """Определённое ударение"""

        for variant in self.__accents:
            if variant.accent == key:
                return variant.part
        raise KeyError

    def __iter__(self):
        for accent in sorted(self.__accents, key=lambda x: x.accent):
            yield accent


class RhythmicWords:
    """Результат анализа ритмических слов"""

    def __init__(self, rhythmic_words: list[RhythmicWord]):
        self.__words :list[RhythmicWord] = rhythmic_words

    def __str__(self) -> str:
        return 'Ритмические слова:\n\n' + shift_right('\n'.join(str(rhytmic_word) for rhytmic_word in self))
    
    def __iter__(self):
        for word in sorted(self.__words, key=lambda x: x.length):
            yield word

    def __getitem__(self, key: int) -> RhythmicWord:
        """Слово определенной длины"""

        for word in self:
            if word.length == key:
                return word
        raise KeyError    

    def as_df(self) -> pd.DataFrame:
        """Pandas.DataFrame с данными"""
        data = []
        for rhythmic_word in self:
            for accent in rhythmic_word:
                data.append([f'{rhythmic_word.length}.{accent.accent}', accent.relative])
        df = pd.DataFrame(data)
        df.columns = ['Тип слова', 'Доля']
        df.set_index('Тип слова', inplace=True)
        return df


class RhythmicWordsAnalyzer:
    def __init__(self, type: str, arg: list[RhythmicWords] | str) -> None:
        self.__type: str = type
        self.__arg: list[RhythmicWords] | str = arg
    
    @staticmethod
    def text(text: str) -> RhythmicWordsAnalyzer:
        return RhythmicWordsAnalyzer('text', arg=text)

    @staticmethod
    def average(stats: list[RhythmicWords]) -> RhythmicWordsAnalyzer:
        return RhythmicWordsAnalyzer('average', stats)
    
    def analyze(self) -> RhythmicWords:
        if self.__type == 'text':
            stat = self.__text_analyze()
        else:
            stat = self.__average_analyze()
        
        rhythmic_words, total_words_count = stat
        result: list[RhythmicWord] = []
        for length in rhythmic_words:
            accents: list[AccentPosition] = []
            for accent_position in rhythmic_words[length]:
                accents.append(AccentPosition(
                    accent=accent_position, 
                    count=rhythmic_words[length][accent_position], 
                    total_words_count=total_words_count)
                )
            result.append(RhythmicWord(length=length, accents=accents))
        return RhythmicWords(rhythmic_words=result)
        

    def __text_analyze(self) -> tuple[dict[int, dict[int, int]], int]:
        text = delete_empty_rows(re.sub(r'\(.*\)', '', self.__arg))
        rhythmic_words = text.strip('|').split('|')
        stat : dict[int, dict[int, int]] = {}
        total_words_count = len(rhythmic_words)

        for rhythmic_word in rhythmic_words:
            vowels = extract_vowels_with_accents(rhythmic_word)

            # Количество слогов:
            syllables_count = len(vowels)

            # Поиск ударной позиции
            for index in range(len(vowels)):
                if '<' in vowels[index]:
                    accent_position = index + 1
                    break

            if syllables_count in stat:
                if accent_position in stat[syllables_count]:
                    stat[syllables_count][accent_position] += 1
                else:
                    stat[syllables_count][accent_position] = 1
            else:
                stat[syllables_count] = {accent_position: 1}
        return (stat, total_words_count)

    def __average_analyze(self) -> tuple[dict[int, dict[int, int]], int]:
        total_words_count = 0
        stat = {}
        for text_stat in self.__arg:
            for rhythmic_word in text_stat:
                for accent in rhythmic_word:
                    total_words_count += accent.count
                    if rhythmic_word.length in stat:
                        if accent.accent in stat[rhythmic_word.length]:
                            stat[rhythmic_word.length][accent.accent] += accent.count
                        else:
                            stat[rhythmic_word.length][accent.accent] = accent.count
                    else:
                        stat[rhythmic_word.length] = {accent.accent: accent.count}
        return (stat, total_words_count)
    
