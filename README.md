# Сравниваем вакансии программистов

Скрипт собирает все вакансии программистов по Москве за месяц, через [HeadHunter API](https://dev.hh.ru/) и [SuperJob API](https://api.superjob.ru/). Обрабатываются вакансии с указанной заработной платой в рублях. Если указаны оба поля “от” и “до”, считается ожидаемый оклад как среднее арифметическое. Если только “от”, умножается на 1.2, а если только “до”, умножается на 0.8. Зарплаты округляются до целого числа и после сбора данных скрипт выводит статистику в терминале. 
![img.png](https://i.imgur.com/sOeyxo8.jpeg)

## Установка

1. Для запуска должен быть установлен [Python 3](https://www.python.org/downloads/release/python-3124/)
2. Клонируйте репозиторий с github
3. Установите зависимости 
```bash
pip install -r requirements.txt
```
5. Создайте файл `.env` указав имя и значение этой переменной как на примере ниже, замените `0123456789abcdefgh` на свой сервисный ключ – “токен” SuperJob API.
```bash
SUPER_JOB_KEY=0123456789abcdefgh
```
### Как его получить: 
- SuperJob API — [Зарегистрируйтесь](https://api.superjob.ru/).
- Получите токен `Secret key` [отсюда](https://api.superjob.ru/info/).
---
### Запуск:

```bash
python main.py
```
---
### Создано с помощью 
![!Static Badge](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
