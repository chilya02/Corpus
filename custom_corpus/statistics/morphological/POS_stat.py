from __future__ import annotations
import spacy
import re
import pandas as pd
from .refactor_words import REFACTOR_WORDS, REFACTOR_VERBS_TENSE, INFINITIVE_VERBS
from ..utils import shift_right

class Token:
    '''Слово'''

    def __init__(self, token: str):
        self.token: str = token
    
    @property
    def length(self) -> int:
        return len(self.token)
    

class Verb(Token):
    '''Глагол'''

    def __init__(self, token: str, tense: str | None, form: str | None):
        super().__init__(token=token)
        self.__tense: str | None = tense
        self.__form: str | None = form
    
    @property
    def tense(self) -> str | None:
        """Время глагола"""
        return self.__tense
    
    @property
    def form(self) -> str | None:
        """Форма глагола"""
        return self.__form
    

class POS:
    '''Часть речи'''
    
    def __init__(self, name: str, total_words_count: int, tokens: list[Token]) -> None:
        self.__name: str = name
        self.__tokens: list[Token] = tokens
        self.__total_words_count: int = total_words_count
    
    def __iter__(self):
        for token in self.__tokens:
            yield token

    @property
    def count(self) -> int:
        return len(self.__tokens)
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def relative(self) -> float:
        return round(self.count / self.__total_words_count, 5)


class PosStat:
    '''Статистика по части речи'''

    def __init__(self, poses: list[POS]):
        self.__POSes: list[POS] = poses
    
    def __iter__(self):
        for pos in self.__POSes:
            yield pos
    
    def __getitem__(self, key: str) -> POS:
        for pos in self:
            if pos.name == key:
                return pos
        raise KeyError

    def __str__(self) -> str:
        return 'Статистика по частям речи:\n\n' + shift_right('\n'.join(f'{pos.name}\t{pos.count}\t{pos.relative}' for pos in self))

    def as_df(self) -> pd.DataFrame:
        df = pd.DataFrame([pos.name, pos.count, pos.relative] for pos in self)
        df.index = range(1, len(self.__POSes) + 1)
        df.index.name = 'Ранг'
        df.columns = ['Часть речи', 'Количество', 'Доля']
        return df

class PosAnalyzer:

    __initialized: bool = False

    def __init__(self, type: str, arg: list[PosStat] | str) -> None:
        self.__type: str = type
        self.__arg: list[PosStat] | str = arg

    @classmethod
    def __initialize_spacy(cls):
        '''Инициализирует spacy'''

        if not cls.__initialized:
            print('Initialize spacy')
            cls.__nlp = spacy.load('ru_core_news_lg')
            cls.__initialized = True
            print('\033[A                 \033[A')

    @staticmethod
    def text(text: str) -> PosAnalyzer:
        return PosAnalyzer(type='text', arg=text)

    @staticmethod
    def average(stats: list[PosStat]) -> PosAnalyzer:
        return PosAnalyzer(type='average', arg=stats)

    def analyze(self) -> PosStat:
        if self.__type == 'text':
            stat = self.__text_analyze()
        else:
            stat = self.__average_analyze()
        poses_stat, total_words_count = stat
        poses: list[POS] = []
        for pos in poses_stat:
            poses.append(POS(
                name=pos, 
                total_words_count=total_words_count,
                tokens=poses_stat[pos]))
        return PosStat(poses=poses)

    def __average_analyze(self) -> tuple[dict[str, list[Token]], int]:
        total_words_count = 0
        stat: dict[str, list[Token]] = {}
        for stat_ in self.__arg:
            for pos in stat_:
                for token in pos:
                    if pos.name == 'PUNCT' or pos.name == 'SPACE':
                        continue
                    total_words_count += 1
                    if pos.name == 'VERB':
                        new_word = Verb(token=token.token, tense=token.tense, form=token.form)
                    else:
                        new_word = Token(token=token.token)
                    try:
                        stat[pos.name].append(new_word)
                    except KeyError:
                        stat[pos.name] = [new_word]
        return (stat, total_words_count)

    def __text_analyze(self) -> tuple[dict[str, list[Token]], int]:

        self.__initialize_spacy()

        total_words_count = 0
        stat: dict[str, list[Token]] = {}
        text = re.sub(r'''[<\|]''', '', self.__arg)
 
        doc = self.__nlp(text)
        for token in doc:

            #Пропускаем пробелы и пунктуацию
            if token.pos_ == 'PUNCT' or token.pos_ == 'SPACE':
                continue
            
            total_words_count += 1

            #Поиск слова в собстенном словаре
            try:
                pos_ = REFACTOR_WORDS[re.sub('ё', 'е', token.text.lower())]
            except KeyError:
                pos_ = token.pos_

            #Перемещение согласно договоренностям
            if pos_ == 'AUX':
                pos_ = 'VERB'
            elif pos_ == 'DET':
                pos_ = 'PRON'
            
            #Обработка глголов
            if pos_ == 'VERB':
                form = None
                #Inf или нет
                try:
                    form = token.morph.to_dict()['VerbForm']
                except KeyError:
                    if re.sub('ё', 'е', token.text.lower()) in INFINITIVE_VERBS:
                        form = 'Inf'
                    else:
                        form = 'Fin'

                #Время
                tense = None
                try:
                    tense = REFACTOR_VERBS_TENSE[re.sub('ё', 'е', token.text.lower())]
                except KeyError:
                    try:
                        tense = token.morph.to_dict()['Tense']
                    except KeyError:
                        tense = None
            
                new_word = Verb(token=token.text, tense=tense, form=form)
            else:
                new_word = Token(token=token.text)

            #Добаляем в статистику
            try:
                stat[pos_].append(new_word)
            except KeyError:
                stat[pos_] = [new_word]

        return (stat, total_words_count)
