from .POS_stat import PosStat, Verb
import pandas as pd

class VerbsTenseStat:
    def __init__(self) -> None:
        self.__verbs: list[Verb] = []
        self.total_words_count: int = 0

    def add_word(self, word: Verb) -> None:
        self.__verbs.append(word)

    @property
    def count(self) -> int:
        return len(self.__verbs)
    
    @property
    def relative(self):
        if self.total_words_count:
            return round(self.count / self.total_words_count, 5)
        else:
            return 0


class VerbsTensesStat:
    def __init__(self, stat: PosStat) -> None:
        
        self.__inf = VerbsTenseStat()
        self.__past = VerbsTenseStat()
        self.__pres = VerbsTenseStat()
        self.__fut = VerbsTenseStat()
        self.__imper = VerbsTenseStat()

        self.__data ={
            'Инфинитив': self.inf,
            'Императив': self.imper,
            'Прошедшее': self.past,
            'Настоящее': self.pres,
            'Будущее ': self.fut,
        }

        total_words_count = 0

        try:
            verbs: list[Verb] = stat['VERB'].tokens
            for verb in verbs:
                if verb.form == 'Inf':
                    self.__inf.add_word(verb)
                elif verb.tense == 'Fut':
                    self.__fut.add_word(verb)
                elif verb.tense == 'Past':
                    self.__past.add_word(verb)
                elif verb.tense == 'Pres':
                    self.__pres.add_word(verb)
                else:
                    self.__imper.add_word(verb)

                total_words_count += 1
        except KeyError:
            pass
        for tense in self.__data:
            self.__data[tense].total_words_count = total_words_count       
    
    def __str__(self) -> str:
        return 'Статистика по временам глагольных частей речи:\n' + '\n'.join(f'{name}\t{stat.count}\t{stat.relative}' for name, stat in self.__data.items())
        
    def as_df(self) -> pd.DataFrame:
        df = pd.DataFrame([name, stat.count, stat.relative] for name, stat in self.__data.items())
        df.columns = ['Тип','Количество', 'Доля']
        df.set_index('Тип', inplace=True)
        return df

    @property
    def inf(self) -> VerbsTenseStat:
        return self.__inf
    
    @property
    def past(self) -> VerbsTenseStat:
        return self.__past
    
    @property
    def pres(self) -> VerbsTenseStat:
        return self.__pres
    
    @property
    def fut(self) -> VerbsTenseStat:
        return self.__fut

    @property
    def imper(self) -> VerbsTenseStat:
        return self.__imper