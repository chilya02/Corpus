from __future__ import annotations
from .utils import extract_vowels_with_accents
import pandas as pd
import re
from ..utils import delete_empty_rows, shift_right

class Ikt:
    def __init__(self, count: int, total_rows_count: int) -> None:
        self.__count: int = count
        self.__total_rows_count: int = total_rows_count
    
    @property
    def relative(self) -> float:
        return round(self.__count / self.__total_rows_count, 5)
    
    @property
    def count(self) -> int:
        return self.__count

class StressnessProfile:

    def __init__(self, ikts: list[Ikt], total_rows_count: int) -> None:
        self.__ikts: list[Ikt] = ikts
        self.__total_rows_count: int = total_rows_count

    @property
    def total_rows_count(self) -> int:
        return self.__total_rows_count

    def __getitem__(self, key: int) -> Ikt:
        return self.__ikts[key-1]

    def __str__(self) -> str:
        return 'Профиль ударности:\n\n' + shift_right('\n'.join(f'{index}\t{ikt.count}\t{ikt.relative}' for index, ikt in enumerate(self, 1)))
    
    def __iter__(self):
        for ikt in self.__ikts:
            yield ikt
    
    def as_df(self) -> pd.DataFrame:
        df = pd.DataFrame(
            [index, ikt.count, ikt.relative] for index, ikt in enumerate(self, 1)
        )
        df.columns = ['Икт', 'Количество', 'Доля']
        df.set_index('Икт', inplace=True)
        return df


class StressnessProfileAnalyzer:
    def __init__(self, type: str, arg: list[StressnessProfile] | str, steps: int) -> None:
        self.__type: str = type
        self.__arg: list[StressnessProfile] | str = arg
        self.__steps: int = steps
    
    @staticmethod
    def text(text: str, steps: int) -> StressnessProfileAnalyzer:
        return StressnessProfileAnalyzer(type='text', arg=text, steps=steps)

    @staticmethod
    def average(stats: list[StressnessProfile], steps: int) -> StressnessProfileAnalyzer:
        return StressnessProfileAnalyzer(type='average', arg=stats, steps=steps)
    
    def analyze(self) -> StressnessProfile:
        if self.__type == 'text':
            stat = self.__text_analyze()
        else:
            stat = self.__average_analyze()
        stressness_profile, total_rows_count = stat
        result: list[Ikt] = []
        for ikt in stressness_profile:
            result.append(Ikt(count=ikt, total_rows_count=total_rows_count))
        return StressnessProfile(ikts=result, total_rows_count=total_rows_count)

    def __text_analyze(self) -> tuple[list[int], int]:
        text = delete_empty_rows(re.sub(r'\(.*\)', '', self.__arg))
        text_rows = text.split('\n')
        rows_count = len(text_rows)
        stat = [0] * self.__steps
        for row in text_rows:
            index = 0
            for vowel in extract_vowels_with_accents(string=row):
                if '<' in vowel:
                    if not (index + 1) % 2: 
                        stat[index // 2] += 1
                index += 1
                if index // 2 >= len(stat):
                    break
        return (stat, rows_count)

    def __average_analyze(self) -> tuple[list[int], int]:
        result = [0] * self.__steps
        rows_count = 0
        for stat in self.__arg:
            rows_count += stat.total_rows_count
            for index in range(self.__steps):
                result[index] += stat[index + 1].count
        return (result, rows_count)
