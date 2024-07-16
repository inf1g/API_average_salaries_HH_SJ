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
    table_data = [[
        'Язык программирования',
        'Найдено вакансий',
        'Обработано вакансий',
        'Средняя зарплата'
    ]]
    for language, stats in statistics.items():
        table_data.append([
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary']]
        )
    title = f" {website}  Moscow"
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[4] = 'right'
    return table_instance.table


def calculate_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    elif salary_from:
        return int(salary_from * 1.2)
    elif salary_to:
        return int(salary_to * 0.8)


def predict_rub_salary_for_hh(languages):
    url = "https://api.hh.ru/vacancies"
    vacancy_statistics = {}
    area_moscow = 1
    period_days = 30
    per_page_vacancies = 100
    currency = 'RUR'
    for language in languages:
        vacancies_salaries = []
        sleep(5)
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
                if vacancy['salary']:
                    vacancy_salary = calculate_salary(vacancy['salary']['from'], vacancy['salary']['to'])
                    vacancies_salaries.append(vacancy_salary)
            if page >= vacancies_response['pages'] - 1:
                break
        if not len(vacancies_salaries):
            average_salary = 0
        else:
            average_salary = int(sum(vacancies_salaries) / len(vacancies_salaries))
        vacancy_statistics[language] = {
            "vacancies_found": vacancies_response['found'],
            "vacancies_processed": len(vacancies_salaries),
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
        vacancies_salaries = []
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
                if vacancy['payment_from'] or vacancy['payment_to']:
                    vacancy_salary = calculate_salary(vacancy['payment_from'], vacancy['payment_to'])
                    vacancies_salaries.append(vacancy_salary)
            if not vacancies_response['more']:
                break
        if not len(vacancies_salaries):
            average_salary = 0
        else:
            average_salary = int(sum(vacancies_salaries) / len(vacancies_salaries))
        vacancy_statistics[language] = {
            "vacancies_found": vacancies_response['total'],
            "vacancies_processed": len(vacancies_salaries),
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
