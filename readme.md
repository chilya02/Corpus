# Corpus
## Описание проекта
Corpus - небольшая библиотека, написанная на Python, предназначенная для анализа стихотворений.
## Содержание 
* [Анализируемые объекты](#Анализируемые-объекты)
    * [Текст]
    * [Корпус]
* [Статистика]
    * [Ритмическая статистика]
        * [Ритмические слова]
        * [Профиль ударности]
    * [Лексическая статистика]
        * [Частотный словарь]
    * [Графическая статистика]
        * [Статистика по частям речи] 
    * [Морфологическая статистика]


## Установка

## Использование 

### Анализируемые объекты
```python 
from custom_corpus import Text, Corpus

#Загрузка текста
some_text = Text('<путь>', <колиечество стоп>, '<название>', <год>)

#Загрузка корпуса текстов
some_corpus = Corpus(<количество стоп>)
some_corpus.load_texts_from_directory(<путь>)

```
### Статистики объектов
```python
#Получение статистики
some_text_or_corpus.statistic
```
