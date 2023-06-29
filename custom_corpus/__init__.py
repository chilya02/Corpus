# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                           #
#              i25555552                                                                    #           
#           S25555555555                                                                    #            
#        ,25552522255555                                                                    #            
#       522          X52                                                                    #            
#      52             5       5252552    5555.255 ;5552 5525X   55552  2555    225555552    #            
#     25                    iS5   2555   55525525  55555 5555S  5552   5552   555X          #            
#    25.                   5555    5555  5555      5555   5555  5552   5555   5555555555i   #            
#    55                    5555    255.  5555      5555   5555  5555:  5555   i5555555255   #            
#   i525                   SS2552  255   555555    25555555Si   55552 55255   ,.     r52X   #
#   2555r                    2555522,    .55552    2555S225i    .2552i 2552   5555552225    #            
#    555555S                                       5555                                     #            
#    X55555555222r                                 5555                                     #            
#      255555555555555555S;                        5555                                     #            
#        :X5225555555522S                          552                                      #                                                                                                                          
#                                                                                           #      
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""
Пакет для работы с текстами.

Классы:
------

`YearFilter`
    Фильтр по годам
`Text` 
    Текст
`Corpus` 
    Корпус

Функции:
-------
`delta()`

Модули:
-------
`exceptions`
    Мокуль исключений

Пакеты:
------
`statistic`
    Пакет работы со статистикой
"""

from __future__ import annotations
import os
import re
from .exceptions import *
from .statistics import Statistic, Analyzer#, TextStatistic, CorpusStatistic
from progress.bar import IncrementalBar


class YearFilter:
    """
    Фильтр по годам

    Атрибуты
    ========
    min_year : `int`
        Год начала отрезка
    max_year : `int`
        Год конца отрезка
    
    Примеры
    =======
    ::

        some_filter = YearFilter(1812, 1813)
        some_filter = YearFilter(min_year=1812, max_year=1813)
    """

    def __init__(self, min_year: int, max_year: int) -> None:
        """
        Создаёт фильтр по годам с min_year включитльно по max_year включительно

        Параметры
        ---------
        min_year : `int`
            Год начала отрезка
        max_year : `int`
            Год конца отрезка
        
        Примеры
        -------
        ::

            YearFilter(1812, 1813)
            YearFilter(min_year=1812, max_year=1813)
        """

        if not isinstance(min_year, int) or not isinstance(max_year, int):
            raise TypeError("Год должен быть целым числом")

        self.min_year: int = min_year
        self.max_year: int = max_year


class Text:
    """
    Текст

    Атрибуты
    ========
    name : `str`
        Название текста
    steps : `int` 
        Количество стоп в тексте
    statistic : `TextStatistic`
        Статистика текста
    year : `int`
        Год текста
    text : `str`
        Текст

    Примеры
    =======
    Создание:
    --------
    ::

        some_text = Text('Dubia.txt', 4, 'Дубия', 1817)
        some_text = Text('F_1857_16_Прибой.txt', 4)

    Доступ к атрибутам:
    -------------------
    >>> some_text.statistic
    >>> some_text.text
    >>> some_text.steps
    >>> some_text.year
    >>> sone_text.name
    """

    def __init__(self, path: str, steps: int, name: str | None = None, year: int | None =  None) -> None:
        """
        Создает новый текст из файла по пути path.

        Параметры
        ---------
        path : `str`
            Путь к файлу с текстом
        steps : `int`
            Количество стоп в тексте
        name : `str` ``(Опционально)``
            Название текста. Если оно не передано, название берётся из имени файла.
        year : `int` ``(Опционально)``
            Год текста. Если он не передан, год берётся из названия файла.
        
        !!!!!Важно!!!!!
        ---------------
        Когда год и имя текста не передаются в аргументы, они берутся из имени файла, которое должно соответствовать формату::

        "<Префикс: строка>_<Год: целое число>_<Количество строк: целое число>_<Название текста: строка>.txt"
        
        Примеры
        -------
        ::

            Text('Dubia.txt', 4, 'Дубия', 1817)
            Text(path='Dubia.txt', steps=4, name='Дубия', year=1817)
            Text('F_1857_16_Прибой.txt', 4)
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
        self.__statistic = Analyzer.text(text=self.text, steps=steps)

    @property
    def name(self) -> str:
        """Название текста"""
        return self.__name

    @property
    def year(self) -> int:
        """Год текста"""
        return self.__year

    @property
    def statistic(self) -> Statistic:
        """
        Статистика текста"""
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
    ========
    steps : `int`
        Количество стоп в текстах корпуса
    statistic : `CorpusStatistic`
        Статистика корпуса текстов
    texts : `list of Text`
        Тексты корпуса

    Методы
    ======
    Добавляет текст в корпус::

        add_text(text)

    Добавляет тексты из папки с возможностью фильтрации по годам::

        load_texts_from_directory(directory_path, year_filter)

    Добавяет тексты из другого корпуса с фильтром по годам::

        add_texts_with_filter(corpus, year_filter)

    Создаёт корупус из текстов другого корпуса с фильтром по годам::

        #Метод класса
        create_new_with_filter(corpus, year_filter)
    
    !!!!!Важно!!!!!
    ===============
    При использовании текста в нескольких местах кода, используйте следующие методы для повышения эффективности::
    
        add_text(text)
        add_texts_with_filter(corpus, year_filter)
        create_with_filter(corpus, year_filter)
        text_1 + text_2 + ...
    
    Примеры
    =======
    Создание:
    ---------
    ::

        some_corpus = text_1 + text_2
        some_corpus = Corpus(4)
        some_corpus = Corpus.create_with_filter(some_corpus_2, year_filter)
    
    Доступ к атрибутам:
    --------------------
    >>> some_corpus.statistic
    >>> some_corpus.texts
    >>> some_corpus.steps
    
    Итерирование по текстам:
    -------------------------
    ::

        for text in some_corpus:
            #Действия с текстами
    
    Добавление текстов в корпус:
    ---------------------------
    Один текст::
        
        some_corpus += text
        #Или:
        some_corpus.add_text(text)
        
    Тексты из другого корпуса::

        some_corpus += other_corpus
        #С фильтром:
        year_filter = YearFilter(1845, 1859)
        some_corpus.add_texts_with_filter(other_corpus, year_filter)

    Загрузить из папки::
    
        some_corpus.load_texts_from_directory('Фет')
        #С фильтром:
        year_filter = YearFilter(1845, 1859)
        some_corpus.load_texts_from_directory('Фет', year_filter)
    """

    def __init__(self, steps: int) -> None:
        """
        Создает корпус с количеством стоп steps.
        
        Параметры
        --------
        steps : `int`
            Количество стоп для текстов корпуса.
        
        Примеры:
        --------
        ::

            Corpus(4)
            Corpus(steps=4)
        """
        self.texts: list[Text] = []
        self.__steps: int = steps
        self.__changed: bool = True
        self.__statistic: Statistic | None = None

    @property
    def statistic(self) -> Statistic:
        """Средняя статистика по корпусу"""

        if self.__changed:
            stats = []
            for text in self.texts:
                stats.append(text.statistic)
            self.__statistic = Analyzer.average(stats, self.steps)
            self.__changed = False
        return self.__statistic

    @property
    def steps(self) -> int:
        """Количество стоп в текстах корпуса"""

        return self.__steps

    def add_text(self, text: Text) -> None:
        """
        Добавляет текст в корпус.
        
        Параметры
        ---------
        text : `Text`
            Текст для добавления
        
        Примеры
        ------
        ::

            some_corpus.add_text(some_text)
            some_corpus.add_text(text=some_text)
        """

        self.__changed = True
        if text.steps == self.steps:
            self.texts.append(text)
        else:
            raise StepsException(
                f'Нельзя добавить {text.steps}-стопный текст {text.name} в {self.steps}-стопный корпус')

    def load_texts_from_directory(self, directory_path: str, year_filter: YearFilter | None = None) -> None:
        """
        Загружает тексты из указанной директории в корпус.
        Если передан фильтр, то тексты отбираются по нему, при этом важно, чтобы имена файлов содержали год.
        
        Параметры
        ---------
        directory_path : `str`
            Путь к директории
        year_filter : `YearFilter` ``(Опционально)``
            Фильтр для отбора текстов
        
        Примеры
        -------
        ::

            load_texts_from_directory('Фет')
            load_texts_from_directory('Фет', year_filter)

        """

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

    def add_texts_with_filter(self, corpus: Corpus, year_filter: YearFilter) -> None:
        """
        Добавляет тексты из другого корпуса по фильтру.
        
        Параметры
        ---------
        corpus : `Corpus`
            Корпус, из которого отбираются тексты
        year_filter : `YearFilter`
            Фильтр, по которому осуществляется отбор
        
        Примеры
        -------
        ::

            add_texts_with_filter(other_corpus, some_year_filter)
            add_texts_with_filter(corpus=other_corpus, year_filter=some_year_filter)
        """

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

    @staticmethod
    def create_with_filter(corpus: Corpus, year_filter: YearFilter) -> Corpus:
        """
        Создаёт корупус из текстов другого корпуса по фильтру.
        
        Параметры
        ---------
        corpus : `Corpus`
            Корпус, из которого отбираются тексты
        year_filter : `YearFilter`
            Фильтр, по которому отбираются тексты
        
        Примеры
        -------
        ::

            Corpus.create_with_filter(some_corpus, some_year_filter)
            Corpus.create_with_filter(corpus=some_corpus, year_filter=some_year_filter)

        """

        new_corpus = Corpus(steps=corpus.steps)
        for text in corpus.texts:
            if year_filter.min_year <= text.year <= year_filter.max_year:
                new_corpus.add_text(text=text)
        return new_corpus


def delta(item_1: Text | Corpus, item_2: Text | Corpus) -> float:
    """
    Дельта-расстояние между объектами типа Corpus или Text
    
    Параметры
    ---------
    item_1 : `Text` или `Corpus`
        Первый объект
    item_2 : `Text` или `Corpus`
        Второй объект

    Возвращаемое значение
    ---------------------

    `float`
        Дробное число, равное дельта-расстоянию между объектами.

    Примеры
    -------
    ::

        delta(text_1, text_2)
        delta(text_1, corpus_1)
        delta(corpus_1, corpus_2)
    """

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
