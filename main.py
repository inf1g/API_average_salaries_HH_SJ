import requests
import os
from time import sleep
from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable


def load_key(token):
    load_dotenv()
    key = os.getenv(token)
    return key


def get_response(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def create_table(statistics, website):
    table_data = [
        ['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата']
    ]
    for language, stats in statistics.items():
        table_data.append([language, stats['vacancies_found'], stats['vacancies_processed'], stats['average_salary']])
    title = f" {website}  Moscow"
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[4] = 'right'
    return table_instance.table


def calculate_salary(vacancy, salary_from, salary_to, toggle=None):
    salary = []
    if toggle:
        vacancy = vacancy['salary']
    if vacancy:
        if vacancy.get(salary_from) and vacancy.get(salary_to):
            salary.append(int((vacancy.get(salary_from) + vacancy.get(salary_to)) / 2))
        elif vacancy.get(salary_from) and not vacancy.get(salary_to):
            salary.append(int(vacancy.get(salary_from) * 1.2))
        elif vacancy.get(salary_to) and not vacancy.get(salary_from):
            salary.append(int(vacancy.get(salary_to) * 0.8))
    return salary


def predict_rub_salary_for_hh(languages):
    url = "https://api.hh.ru/vacancies"
    vacancy_statistics = {}
    salaries_vacancies = []
    vacancies_response = None
    area_moscow = 1
    period_days = 30
    per_page_vacancies = 100
    currency = 'RUR'
    for language in languages:
        vacancies_processed_total = 0
        sleep(10)
        for page in count(0):
            params = {
                'text': f'Программист {language}',
                'area': area_moscow,
                'page': page,
                'per_page': per_page_vacancies,
                'period': period_days,
                'currency': currency
            }
            vacancies_response = get_response(url, params=params)
            for vacancy in vacancies_response['items']:
                vacancy_salary = calculate_salary(vacancy, 'from', 'to', 1)
                salaries_vacancies.extend(vacancy_salary)
                vacancies_processed_total += len(vacancy_salary)
            if page >= vacancies_response['pages'] - 1:
                break
        if len(salaries_vacancies) == 0:
            average_salary = 0
        else:
            average_salary = int(sum(salaries_vacancies) / len(salaries_vacancies))
        vacancy_statistics[language] = {
            "vacancies_found": vacancies_response['found'],
            "vacancies_processed": vacancies_processed_total,
            "average_salary": int(average_salary)
        }
    return vacancy_statistics


def predict_rub_salary_for_sj(languages, api_key):
    url = "https://api.superjob.ru/2.0/vacancies/"
    vacancy_statistics = {}
    area_moscow = 4
    per_page_vacancies = 100
    currency = 'rub'
    for language in languages:
        salaries_vacancies = []
        vacancies_response = 0
        vacancies_processed_total = 0
        for page in count(0):
            headers = {'X-Api-App-Id': api_key}
            params = {
                "keyword": f'Программист {language}',
                'town': area_moscow,
                'page': page,
                'count': per_page_vacancies,
                'currency': currency
            }
            vacancies_response = get_response(url, headers, params)
            for vacancy in vacancies_response['objects']:
                vacancy_salary = calculate_salary(vacancy, 'payment_from', 'payment_to')
                salaries_vacancies.extend(vacancy_salary)
                vacancies_processed_total += len(vacancy_salary)
            if not vacancies_response['more']:
                break
        if len(salaries_vacancies) == 0:
            average_salary = 0
        else:
            average_salary = int(sum(salaries_vacancies) / len(salaries_vacancies))
        vacancy_statistics[language] = {
            "vacancies_found": vacancies_response['total'],
            "vacancies_processed": vacancies_processed_total,
            "average_salary": int(average_salary)
        }
    return vacancy_statistics


def main():
    key = load_key('SUPER_JOB_KEY')
    languages = {
        "JavaScript",
        "Python",
        "Java",
        "C#",
        "PHP",
        "C++",
        "TypeScript",
        "Go",
        "C",
        "KOTLIN",
        "1C"
    }
    statistic_sj = predict_rub_salary_for_sj(languages, key)
    statistic_hh = predict_rub_salary_for_hh(languages)
    print(create_table(statistic_sj, 'superjob.ru'))
    print(create_table(statistic_hh, 'hh.ru'))


if __name__ == '__main__':
    main()
