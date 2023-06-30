# Corpus
## Описание проекта
Corpus - небольшая библиотека, написанная на Python, предназначенная для анализа стихотворений.
## Установка

## Использование 
```python 
from custom_corpus import Text, Corpus
#Загрузка текста
some_text = Text('<путь>', <колиечество стоп>, '<название>', <год>)
#Загрузка корпуса текстов
some_corpus = Corpus(<количество стоп>)
some_corpus.load_texts_from_directory(<путь>)
#или

```
