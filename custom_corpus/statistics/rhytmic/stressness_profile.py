from .utils import extract_vowels_with_accents
import pandas as pd

class StressnessProfile:

    def __init__(self, steps: int) -> None:
        self._ikts = [0] * steps

    def __getitem__(self, key: int) -> float:
        return self._ikts[key-1]

    def __str__(self) -> str:
        return 'Профиль ударности:\n' + '\n'.join(f'{index + 1}\t{self._ikts[index]}' for index in range(len(self._ikts)))
    
    def __iter__(self) -> float:
        for ikt in self._ikts:
            yield ikt
    
    def as_df(self) -> pd.DataFrame:
        df = pd.DataFrame(
            [index, self[index]] for index in range(1, len(self._ikts) + 1 )
        )
        df.columns = ['Икт','Доля ударных слов']
        df.set_index('Икт', inplace=True)
        return df

class TextStressnessProfile(StressnessProfile):

    def __init__(self, steps: int, text: str) -> None:
        super().__init__(steps)

        text_rows = text.split('\n')
        rows_count = len(text_rows)
        stat = [0] * steps
        for row in text_rows:
            index = 0
            for vowel in extract_vowels_with_accents(string=row):
                if '<' in vowel:
                    if not (index + 1) % 2: 
                        stat[index // 2] += 1
                index += 1
                if index // 2 >= len(stat):
                    break
        for index in range(steps):
            self._ikts[index] = round(stat[index] / rows_count, 5)     
        

class CorpusStressnessProfile(StressnessProfile):

    def __init__(self, steps: int, stats: list[TextStressnessProfile]) -> None:
        super().__init__(steps)
        result = [0] * steps
        for stat in stats:
            for index in range(steps):
                result[index] += stat[index + 1]
        for index in range(steps):
            self._ikts[index] = round(result[index] / len(stats), 5)
        