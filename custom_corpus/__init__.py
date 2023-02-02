"""Модуль работы с текстами"""

from __future__ import annotations
import os
import re
from .exceptions import *
from .statistics import TextStatistic, CorpusStatistic
from progress.bar import IncrementalBar


class YearFilter:
    """
    Фильтр по годам

    Атрибуты
    --------
    min_year : int
        Год начала отрезка
    max_year : int
        Год конца отрезка
    
    Примеры
    -------
    Создать фильтр с 1812 по 1813 год::

        YearFilter(1812, 1813)
    
    ::

        YearFilter(min_year=1812, max_year=1813)
    
    """

    def __init__(self, min_year: int, max_year: int) -> None:
        """
        Создаёт фильтр по годам, начиная с min_year включитльно по max_year включительно

        Параметры
        ---------
        min_year : int
            Год начала отрезка
        max_year : int 
            Год конца отрезка
        
        Возвращаемое значение
        ---------------------
        None
        """

        if not isinstance(min_year, int) or not isinstance(max_year, int):
            raise TypeError("Год должен быть целым числом")

        self.min_year: int = min_year
        self.max_year: int = max_year


class Text:
    """
    Текст
    
    Атрибуты
    --------
    name : str
        Название текста
    steps : int 
        Количество стоп в тексте
    statistic : TextStatistic
        Статистика текста
    year : int
        Год текста
    text : str
        Текст
    
    Примеры
    -------
    Создать 4-х стопный текст 1817 года с имненем "Дубия"::

        text_1 = Text('Dubia.txt', 4, 'Дубия', 1817)
    
    ::

        text_2 = Text(path='Dubia.txt', steps=4, name='Дубия', year=1817)
    
    Создать 4-х стопный текст 1857 года с именем "Прибой"::
    
        text_1 = Text('F_1857_16_Прибой.txt', 4)
    
    ::
        
        text_2 = Text(path='F_1857_16_Прибой.txt', steps=4)
    
    Получить статистику текста::

        text_1.statistic

    Получить исходный текст::

        text_1.text

    Получить количество стоп текста::

        text_1.steps

    Получить год текста::

        text_1.year

    """

    def __init__(self, path: str, steps: int, name: str | None = None, year: int | None =  None) -> None:
        """
        Создает новый текст

        Параметры
        ---------
        path : str
            Путь к файлу с текстом
        steps : int
            Количество стоп в тексте
        name : str, optional
            Название текста. Если оно не передано, название берётся из имени файла.
        year : int, optional
            Год текста. Если он не передан, год берётся из названия файла.
        
        !!!!!Важно!!!!!
        ---------------
        Когда год и имя текста не передаются в аргументы, они берутся из имени файла, которое должно соответствовать формату::

        "<Префикс: строка>_<Год: целое число>_<Количество строк: целое число>_<Название текста: строка>.txt"
        
        Примеры
        -------
        Создать 4-х стопный текст 1817 года с имненем "Дубия"::

            Text('Dubia.txt', 4, 'Дубия', 1817)

        ::

            Text(path='Dubia.txt', steps=4, name='Дубия', year=1817)

        Создать 4-х стопный текст 1857 года с именем "Прибой"::
        
            Text('F_1857_16_Прибой.txt', 4)

        ::

            Text(path='F_1857_16_Прибой.txt', steps=4)

        """
        
        file_name = os.path.split(path)[-1]
        self.__steps = steps

        #Запоминается имя текста
        if name:
            self.__name = name
        else:
            self.__name = re.search(
                pattern=r'.*_\d+_\d+_(?P<name>.+)\.txt',
                string=file_name
            ).group('name')

        #Запоминается год текста
        if year:
            self.__year = year
        else:
            self.__year = int(
                re.search(
                    pattern=r'.*_(?P<year>\d+)_\d+_.+\.txt', 
                    string=file_name
                ).group('year')
            )
        
        #Читается текст из файла
        with open(path, 'r', encoding='utf-8') as file:
            self.__text: str = file.read().strip('\n').strip(' ')

        #Создается статистика текста
        self.__statistic = TextStatistic(text=self.text, steps=steps)

    @property
    def name(self) -> str:
        """Название текста"""
        return self.__name

    @property
    def year(self) -> int:
        """Год текста"""
        return self.__year

    @property
    def statistic(self) -> TextStatistic:
        """Статистика текста"""
        return self.__statistic

    @property
    def steps(self) -> int:
        """Количество стоп в тексте"""
        return self.__steps
    
    @property
    def text(self) -> str:
        """Текст"""
        return self.__text

    def __add__(self, other: Text | Corpus) -> Corpus:
        """Объединяет с текстом или корпусом"""

        if not isinstance(other, (Text, Corpus)):
            raise TypeError(
                f'Невозможно объединить текст с объектом типа {type(other)}'
            )
        if not self.steps == other.steps:
            raise StepsException(
                f'Невозможно объединить {self.steps}-стпоный \
                    текст и {other.steps}-стопный \
                        {"корпус" if isinstance(other, Corpus) else "текст"}'
            )
        corpus = Corpus(self.steps)
        corpus.add_text(self)
        if isinstance(other, Text):
            corpus.add_text(other)
        elif isinstance(other, Corpus):
            for text in other.texts:
                corpus.add_text(text)
        else:
            raise TypeError()
        return corpus

    def __str__(self) -> str:
        return self.text


class Corpus:
    """
    Корпус текстов
    
    Атрибуты
    --------
    steps : int 
        Количество стоп в текстах корпуса
    statistic : CorpusStatistic
        Статистика корпуса текстов
    texts : list[Text]
        Список текстов в корпусе

    Методы
    ------
    add_text(text: Text):
        Добавляет текст в корпус
    load_texts_from_directory(directory_path, year_filter):
        Добавляет либо все тексты из папки, либо тексты с фильтром по годам
    add_texts_from_other_corpus_with_filter(corpus, year_filter)
        Добавяет тексты из другого корпуса с фильтром по годам
    create_new_with_filter(corpus, year_filter)
        Создаёт корупус из текстов другого корпуса с фильтром по годам
    
    Примеры
    -------
    Создать корпус объединением нескольких текстов::

        some_corpus = text_1 + text_2

    Создать корпус 
    
    Добавить текст в существующий корпус

    * some_corpus.add_text(text)
    """

    def __init__(self, steps: int) -> None:
        self.texts: list[Text] = []
        self.__steps: int = steps
        self.__changed: bool = True
        self.__statistic: CorpusStatistic | None = None

    @property
    def statistic(self) -> CorpusStatistic:
        """Средняя статистика по корпусу"""

        if self.__changed:
            stats = []
            for text in self.texts:
                stats.append(text.statistic)
            self.__statistic = CorpusStatistic(stats, self.steps)
            self.__changed = False
        return self.__statistic

    @property
    def steps(self) -> int:
        """Количество стоп в текстах корпуса"""

        return self.__steps

    def add_text(self, text: Text) -> None:
        """Добавляет текст в корпус"""

        self.__changed = True
        if text.steps == self.steps:
            self.texts.append(text)
        else:
            raise StepsException(
                f'Нельзя добавить {text.steps}-стопный текст {text.name} в {self.steps}-стопный корпус')

    def load_texts_from_directory(self, directory_path: str, year_filter: YearFilter | None = None) -> None:
        """Загружает тексты из указанной директории в корпус"""

        self.__changed = True
        for root, dirs, files in os.walk(f"{directory_path}"):

            for filename in files:
                path = os.path.join(directory_path, filename)
                text = Text(path=path, steps=self.__steps)
                if year_filter:
                    if year_filter.min_year <= text.year <= year_filter.max_year:
                        self.add_text(text)
                else:
                    self.add_text(text)

    def __iter__(self):
        for text in self.texts:
            yield text

    def add_texts_from_other_corpus_with_filter(self, corpus: Corpus, year_filter: YearFilter) -> None:
        """Добавляет тексты из другого корпуса по фильтру"""

        self.__changed = True
        for text in corpus.texts:
            if year_filter.min_year <= text.year <= year_filter.max_year:
                self.add_text(text=text)

    def __add__(self, other: Text | Corpus) -> Corpus:
        """Объединяет с текстом или корпусом"""

        if not isinstance(other, (Text, Corpus)):
            raise TypeError(
                f'Невозможно объединить корпус с объектом типа {type(other)}'
            )
        if not self.steps == other.steps:
            raise StepsException(
                f'Невозможно объединить {self.steps}-стпоный \
                    корпус и {other.steps}-стопный \
                        {"корпус" if isinstance(other, Corpus) else "текст"}'
            )
        corpus = Corpus(self.steps)
        for text in self.texts:
            corpus.add_text(text=text)
        if isinstance(other, Text):
            corpus.add_text(other)
        elif isinstance(other, Corpus):
            for text in other.texts:
                corpus.add_text(text)
        else:
            raise TypeError()
        return corpus

    @classmethod
    def create_new_with_filter(cls, corpus: Corpus, year_filter: YearFilter) -> Corpus:
        """Создаёт корупус из текстов другого корпуса по фильтру"""

        new_corpus = cls(steps=corpus.steps)
        for text in corpus.texts:
            if year_filter.min_year <= text.year <= year_filter.max_year:
                new_corpus.add_text(text=text)
        return new_corpus


def delta(item_1: Text | Corpus, item_2: Text | Corpus) -> float:
    """Дельта-расстояние между объектами типа Corpus или Text"""

    if not isinstance(item_1, (Text, Corpus)) or not isinstance(item_2, (Text, Corpus)):
        raise TypeError(
            'Дельта-расстояние можно вычислить только между объектами типов Text или Corpus'
        )
    new_corpus = item_1 + item_2
    analyzed_words_count = 0
    z_sum = 0
    with IncrementalBar(max=len(new_corpus.statistic.lexical.words_freq), message='Calc Delta') as bar:
        for word_stat in new_corpus.statistic.lexical.words_freq:
            bar.next()
            analyzed_words_count += 1
            try:
                freq_1 = item_1.statistic.lexical.words_freq[word_stat.word].relative
                freq_2 = item_2.statistic.lexical.words_freq[word_stat.word].relative
            except KeyError:
                continue

            sigma = (((freq_1 - word_stat.relative) ** 2) + ((freq_2 - word_stat.relative) ** 2) / 2) ** 0.5
            if sigma:
                z_sum += abs(freq_1 - freq_2) / sigma
        bar.finish()
        print("\033[A                                                         \033[A\033[A")
    return z_sum / analyzed_words_count
