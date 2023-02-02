from .utils import extract_vowels_with_accents
import pandas as pd


class AccentPosition:
    """Результат анализа ударений на определенном слоге"""

    def __init__(self, accent: int, part: float) -> None:
        self.accent = accent
        self.part = part

    def __str__(self) -> str:
        return str(self.part)


class RhythmicWord:
    """Результат анализа ритмических слов определенной длины."""

    def __init__(self, length: int):
        self.__accents: list[AccentPosition] = []
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

    def __init__(self):
        self._words :list[RhythmicWord] = []

    def __str__(self) -> str:
        return 'Ритмические слова:\n' + '\n'.join(str(rhytmic_word) for rhytmic_word in sorted(self._words, key=lambda x: x.length))
    
    def __getitem__(self, key: int) -> RhythmicWord:
        """Слово определенной длины"""

        for word in self._words:
            if word.length == key:
                return word
        raise KeyError

    def _add_word(self, word: RhythmicWord) -> None:
        """Добавляет ритмическое слово"""

        self._words.append(word)

    def __iter__(self):
        for word in sorted(self._words, key=lambda x: x.length):
            yield word

    def as_df(self) -> pd.DataFrame:
        """Pandas.DataFrame с данными"""
        data = []
        for rhythmic_word in sorted(self._words,key=lambda x: x.length):
            for accent in rhythmic_word:
                data.append([f'{rhythmic_word.length}.{accent.accent}', accent.part])
        df = pd.DataFrame(data)
        df.columns = ['Тип слова', 'Доля']
        df.set_index('Тип слова', inplace=True)
        return df


class TextRhythmicWords(RhythmicWords):
    """Результат анализа ритмических слов"""
    
    def __init__(self, text: str):
        super().__init__()
 
        rhythmic_words = text.strip('|').split('|')
        stat : dict[int, dict[int, int]] = {}
        count = len(rhythmic_words)

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

        for length in stat.keys():
            self._add_word(RhythmicWord(length=length))
            for accent_position in stat[length].keys():
                accent = AccentPosition(accent_position, round(stat[length][accent_position] / count, 5))
                self._words[-1]._add_accent(accent=accent)


class CorpusRhythmicWords(RhythmicWords):
    """Результат анализа ритмических слов"""

    def __init__(self, stats: list[TextRhythmicWords]):
        super().__init__()
        stat = {}
        count = len(stats)
        for text_stat in stats:
            for rhythmic_word in text_stat:
                for accent in rhythmic_word:
                    if rhythmic_word.length in stat:
                        if accent.accent in stat[rhythmic_word.length]:
                            stat[rhythmic_word.length][accent.accent] += accent.part
                        else:
                            stat[rhythmic_word.length][accent.accent] = accent.part
                    else:
                        stat[rhythmic_word.length] = {accent.accent: accent.part}

        for length in stat.keys():
            self._add_word(RhythmicWord(length=length))
            for accent_position in stat[length].keys():
                accent = AccentPosition(accent_position, round(stat[length][accent_position] / count, 5))
                self._words[-1]._add_accent(accent=accent)
