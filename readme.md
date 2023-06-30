# Corpus
## Описание проекта
Corpus - небольшая библиотека, написанная на Python, предназначенная для анализа стихотворений.
## Содержание
* [Установка](#Установка)
    * [Загрузка исходного кода](#Загрузка-исходного-кода)
    * [Установка зависимостей](#Установка-зависимостей)
* [Использование](#Использование)
    * [Анализируемые объекты](#Анализируемые-объекты)
      * [Текст](#Текст)
      * [Корпус](#Корпус)
    * [Статистика](#Статистики-объектов)
        * [Ритмическая статистика](#Ритмичечская-статистика)
            * [Ритмические слова](#Ритмические-слова)
            * [Профиль ударности](#Профиль-ударности)
        * [Лексическая статистика](#Лексическая-статистика)
            * [Частотный словарь](#Частотный-словарь)
        * [Графическая статистика](#Графическая-статистика)
            * [Средняя длина слов](#Средняя-длина-слов)
        * [Морфологическая статистика](#Морфологическая-статистика)
            * [Статистика по частям речи](#Статистика-по-частям-речи)



## Установка
### Загрузка исходного кода
Linux:
```linux
git clone https://github.com/chilya02/Corpus.git
```
Windows:
> Загрузите архивом и распакуйте в папке проекта
### Установка зависимостей
Linux/Windows:
```terminal
pip install -r pip_requirements.txt
python -m spacy download ru_core_news_lg
```
## Использование 
### Анализируемые объекты
#### Текст
Синтаксис: 
``` 
some_text = Text('<путь>', <количество стоп>, '<название>', <год>)
```
Примеры:
```python 
from custom_corpus import Text

text_1 = Text('Dubia.txt', 4, 'Дубия', 1817)
text_2 = Text(path='Dubia.txt', steps=4, name='Дубия', year=1817)
text_3 = Text('F_1857_16_Прибой.txt', 4)
text_4 = Text(path='F_1857_16_Прибой.txt', steps=4)
```
Получение данных
```python
>>> some_text.statistic #Статистика текста
>>> some_text.text      #Непосредственно текст
>>> some_text.steps     #Количество стоп в тексте
>>> some_text.year      #Год написания текста
>>> some_text.name      #Название текста
```
#### Корпус
Синтаксис: 
```
some_corpus = Corpus(<количество стоп>)
some_corpus.load_texts_from_directory(<путь>)
```

Примеры:
```python
from custom_corpus import Corpus, YearFilter

#Загрузка из папки
corpus_1 = Corpus(5)
corpus_1.load_texts_from_directory('Фет')

#Загрузка из папки с фильтром 
corpus_2 = Corpus(5)
year_filter = YearFilter(1845, 1859)
corpus_2.load_texts_from_directory('Фет', year_filter)

#Объединение нескольких текстов
corpus_3 = text_1 + text_2
```
Получение данных
```python
>>> some_corpus.statistic   #Статистика всех текстов куорпуса
>>> some_corpus.texts       #Список текстов
>>> some_corpus.steps       #Количество стоп в текстах корпуса
```
---
### Статистики объектов
```python
#Вернёт объект типа custom_corpus.statistic.Statistic
>>> some_text_or_corpus.statistic

#Выведет всю статистику в текстовом формате
>>> print(some_text_or_corpus.statistic)
```
#### Ритмическая статистика
```python
#Вернёт объект типа custom_corpus.statistic.rhythmic.RhythmicStatistic
>>> some_text_or_corpus.statistic.rhythmic

#Выведет ритмическую статистику в текстовом формате
>>> print(some_text_or_corpus.statistic.rhythmic)
```
#### Ритмические слова
```python 

#Вернёт объект типа custom_corpus.statistic.rhythmic.RhythmicWords
>>> some_text_or_corpus.statistic.rhythmic.rhythmic_words

#Вернёт объект типа Pandas.DataFrame с результатами анализа
>>> some_text_or_corpus.statistic.rhythmic.rhythmic_words.as_df()

#Вернёт объект типа custom_corpus.statistic.rhythmic.RhythmicWord - статистика по слову из 2 слогов
>>> some_text_or_corpus.statistic.rhythmic.rhythmic_words[2]

#Выведет статистику ритмических слов в текстовом формате
>>> print(some_text_or_corpus.statistic.rhythmic.rhythmic_words)

#Выведет статистику ритмического слова из двух слогов в текстовом формате
>>> print(some_text_or_corpus.statistic.rhythmic.rhythmic_words[2])
```
#### Профиль ударности 
```python 

#Вернёт объект типа custom_corpus.statistic.rhythmic.StressnessProfile
>>> some_text_or_corpus.statistic.rhythmic.stressness_profile

#Вернёт объект типа Pandas.DataFrame с результатами анализа
>>> some_text_or_corpus.statistic.rhythmic.stressness_profile.as_df()

#Вернёт объект типа custom_corpus.statistic.rhythmic.Ikt - статистика по ударению на 2 икт
>>> some_text_or_corpus.statistic.rhythmic.stressness_profile[2]

#Выведет статистику профиля ударности в текстовом формате
>>> print(some_text_or_corpus.statistic.rhythmic.stressness_profile)

#Выведет долю строк с ударением на 2 икт относительно общего количества
>>> print(some_text_or_corpus.statistic.rhythmic.stressness_profile[2])

```
---
#### Лексическая статистика
---
#### Графическая статистика
---
#### Морфологическая статистика

