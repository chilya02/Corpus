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
##### Создание
Синтаксис
`some_text = Text('<путь>', <количество стоп>, '<название>', <год>)`

```python 
from custom_corpus import Text

#Загрузка текста

#Примеры
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
Создание
```python
from custom_corpus import Corpus

#Загрузка корпуса текстов
some_corpus = Corpus(<количество стоп>)
some_corpus.load_texts_from_directory(<путь>)


```
Получение данных
```python
>>> some_corpus.statistic
>>> some_corpus.texts
>>> some_corpus.steps
```
### Статистики объектов
```python
#Получение статистики
some_text_or_corpus.statistic
```
