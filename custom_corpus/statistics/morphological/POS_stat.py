import spacy
import re
import pandas as pd
from .refactor_words import REFACTOR_WORDS, REFACTOR_VERBS_TENSE, INFINITIVE_VERBS


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
        self.tense: str = tense
        self.form = form
    

class POS:
    '''Часть речи'''
    
    def __init__(self, name: str, total_words_count: int) -> None:
        self.name: str = name
        self.tokens: list[Token] = []
        self.total_words_count: int = total_words_count

    def add_word(self, word: Token) -> None:
        self.tokens.append(word)
    
    def __iter__(self) -> Token:
        for token in self.tokens:
            yield token

    @property
    def count(self) -> int:
        return len(self.tokens)
    
    @property
    def relative(self) -> float:
        return round(self.count / self.total_words_count, 5)


class PosStat:
    '''Статистика по части речи'''

    def __init__(self):
        self.POSes: list[POS] = []
    
    def __iter__(self):
        for pos in self.POSes:
            yield pos
    
    def __getitem__(self, key: str) -> POS:
        for pos in self.POSes:
            if pos.name == key:
                return pos
        raise KeyError
    
    def add_pos(self, pos: POS) -> None:
        self.POSes.append(pos)
    
    def add_token(self, pos: str, word: Token) -> None:
        try:
            self[pos].add_word(word)
        except KeyError:
            new_pos = POS(pos, 0)
            new_pos.add_word(word)
            self.add_pos(new_pos)

    def __str__(self) -> str:
        return 'Статистика по частям речи:\n' + '\n'.join(f'{pos.name}\t{pos.count}\t{pos.relative}' for pos in self.POSes)

    def as_df(self) -> pd.DataFrame:
        df = pd.DataFrame([pos.name, pos.count, pos.relative] for pos in self)
        df.index = range(1, len(self.POSes) + 1)
        df.index.name = 'Ранг'
        df.columns = ['Часть речи', 'Количество', 'Доля']
        return df


class TextPosStat(PosStat):
    '''Статистика по частям речи в тексте'''

    __initialized: bool = False

    @classmethod
    def __initialize_spacy(cls):
        '''Инициализирует spacy'''

        if not cls.__initialized:
            print('Initialize spacy')
            cls.__nlp = spacy.load('ru_core_news_lg')
            cls.__initialized = True
            print('\033[A                 \033[A')
    
    def __init__(self, text: str):
        super().__init__()
        self.__initialize_spacy()
        total_words_count = 0
 
        text = re.sub(r'''[<\|]''', '', text)
 
        doc = self.__nlp(text)
        
        for token in doc:

            #Пропускаем пробелы и пунктуацию
            if (not token.pos_ == 'PUNCT') and (not token.pos_ == 'SPACE'):
                    total_words_count += 1
            else:
                continue
            
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

            #Созаём слово
            if pos_ == 'VERB':
                new_word = Verb(token=token.text, tense=tense, form=form)
            else:
                new_word = Token(token=token.text)

            #Добаляем в статистику
            self.add_token(pos=pos_, word=new_word)

        #Для всех частей речи задаем общее количество слов для расчетов относительной статистики
        for pos in self:
            pos.total_words_count = total_words_count


class CorpusPosStat(PosStat):
    '''Статистика по частям речи в корпусе'''

    def __init__(self, stats: list[TextPosStat]):
        super().__init__()
        total_words_count = 0
        for text_stat in stats:
            for pos in text_stat:
                for token in pos.tokens:
                    if (not pos.name == 'PUNCT') and (not pos.name == 'SPACE'):
                        total_words_count += 1
                    
                    #Создаём новое слово
                    if pos.name == 'VERB':
                        new_word = Verb(token=token.token, tense=token.tense, form=token.form)
                    else:
                        new_word = Token(token=token.token)
                    
                    #добавляем в статистику
                    self.add_token(pos=pos.name, word=new_word)

        #Для всех частей речи задаем общее количество слов для расчетов относительной статистики
        for pos in self:
            pos.total_words_count = total_words_count
