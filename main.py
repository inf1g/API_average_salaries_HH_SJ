from requests import Session
import os
from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable


def load_keys(token):
    load_dotenv()
    key = os.getenv(token)
    return key


def get_response(session, url, headers=None, params=None):
    response = session.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def creating_table(statistics_json, website):
    table_data = [
        ['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата']
    ]
    for language, stats in statistics_json.items():
        table_data.append([language, stats['vacancies_found'], stats['vacancies_processed'], stats['average_salary']])
    title = f"{website}  Moscow"
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[4] = 'right'
    return table_instance.table


def calculate_average_salary(salaries):
    return int(sum(salaries) / len(salaries))


def creating_statistics(vacancy_json, salary_from, salary_to, toggle=None):
    salary = []
    for vacancy in vacancy_json:
        if toggle:
            vacancy = vacancy['salary']
        if vacancy.get(salary_from) and vacancy.get(salary_to):
            if vacancy.get(salary_from) != 0 and vacancy.get(salary_to) != 0:
                salary.append(int((vacancy.get(salary_from) + vacancy.get(salary_to)) / 2))
        elif vacancy.get(salary_from) and not vacancy.get(salary_to):
            if vacancy.get(salary_from) != 0 and vacancy.get(salary_to) == 0:
                salary.append(int(vacancy.get(salary_from) * 1.2))
        elif vacancy.get(salary_to) and not vacancy.get(salary_from):
            if vacancy.get(salary_to) != 0 and vacancy.get(salary_from) == 0:
                salary.append(int(vacancy.get(salary_to) * 0.8))
    return salary


def predict_rub_salary_for_hh(languages):
    url = "https://api.hh.ru/vacancies"
    vacancies_info = {}
    vacancies_salary = []
    vacancies_data = None
    with Session() as session:
        for language in languages:
            vacancies_processed_total = 0
            for page in count(0):
                headers = {
                    'HH-User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                     ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                }
                params = {
                    'text': f'Программист {language}',
                    'area': "1",
                    'page': page,
                    'per_page': '100',
                    'period': '30',
                    'currency': "RUR",
                    'only_with_salary': 'true'
                }
                vacancies_data = get_response(session, url, headers, params)
                if page >= vacancies_data['pages']:
                    break
                vacancy_page_list = creating_statistics(
                    vacancies_data['items'], 'from', 'to', 1)
                vacancies_salary.extend(vacancy_page_list)
                vacancies_processed_total += len(vacancy_page_list)
            if len(vacancies_salary) == 0:
                average_salary = 0
            else:
                average_salary = calculate_average_salary(vacancies_salary)
            lang = {
                "vacancies_found": vacancies_data['found'],
                "vacancies_processed": vacancies_processed_total,
                "average_salary": int(average_salary)}
            vacancies_info[language] = lang
    return vacancies_info


def predict_rub_salary_for_sj(languages):
    url = "https://api.superjob.ru/2.0/vacancies/"
    vacancies_info = {}
    with Session() as session:
        for language in languages:
            vacancies_salary = []
            vacancies_processed_total = 0
            for page in count(0):
                headers = {'X-Api-App-Id': load_keys('SUPER_JOB_KEY')}
                params = {
                    "keyword": f'Программист {language}',
                    'town': 4,
                    'page': page,
                    'count': 100,
                    'payment': 'RUR',
                    'currency': 'rur'
                }
                vacancies_data = get_response(session, url, headers, params)
                vacancy_page_list = creating_statistics(
                    vacancies_data['objects'], 'payment_from', 'payment_to')
                vacancies_salary.extend(vacancy_page_list)
                vacancies_processed_total += len(vacancy_page_list)
                if not vacancies_data['more']:
                    break
            if len(vacancies_salary) == 0:
                average_salary = 0
            else:
                average_salary = calculate_average_salary(vacancies_salary)
            lang = {
                "vacancies_found": vacancies_data['total'],
                "vacancies_processed": vacancies_processed_total,
                "average_salary": int(average_salary)
            }
            vacancies_info[language] = lang
    return vacancies_info


def main():
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
        'Ruby',
        "1C"
    }
    statistic_sj = predict_rub_salary_for_sj(languages)
    statistic_hh = predict_rub_salary_for_hh(languages)
    print(creating_table(statistic_sj, 'superjob.ru'))
    print(creating_table(statistic_hh, 'hh.ru'))


if __name__ == '__main__':
    main()
