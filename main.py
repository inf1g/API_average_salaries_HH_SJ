import requests
import json
import os
from itertools import count
from dotenv import load_dotenv


def load_keys(token):
    load_dotenv()
    key = os.getenv(token)
    return key


def get_response(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_for_hh(languages):
    url = "https://api.hh.ru/vacancies"
    vacancies_info = {}
    vacancies_salary = []
    for language in languages:
        print(language)
        for page in count(0):
            salary = []
            print(page)
            headers = {
                'HH-User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                 ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            }
            params = {
                'text': f'Программист {language}',
                'area': "1",
                'page': page,
                'per_page': '100',
                'resume_search_experience_period': 'all_time',
                'currency': "RUR",
                'only_with_salary': 'true'
            }
            vacancies_data = get_response(url, headers, params)
            if page >= vacancies_data['pages']:
                break
            for vacancy in vacancies_data:
                if vacancy['salary'].get('from') and vacancy['salary'].get('to'):
                    salary .append(int((vacancy['salary'].get('from') + vacancy['salary'].get('to')) / 2))
                    vacancies_salary.extend(salary)
                elif vacancy['salary'].get('from') and not vacancy['salary'].get('to'):
                    salary .append(int(vacancy['salary'].get('from') * 1.2))
                    vacancies_salary.extend(salary)
                elif vacancy['salary'].get('to') and not vacancy['salary'].get('from'):
                    salary .append(int(vacancy['salary'].get('to') * 0.8))
                    vacancies_salary.extend(salary)
                else:
                    pass


            vacancies_salary_for_page.append(predict_salary(vacancies_data['items'], 'from', 'to'))
            vacancies_salary.extend(vacancies_salary_for_page)
        lang = {
            "vacancies_found": vacancies_data['found'],
            "vacancies_processed": vacancies_data['found'],
            "average_salary": int((sum(vacancies_salary)) / len(vacancies_salary))}
        vacancies_info[language] = lang
        with open(f'vacancies_info.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_info, file, ensure_ascii=False, indent=4)


def creating_salary_list(vacancy_json, salary_from, salary_to, toggle=None):
    salary = []
    for vacancy in vacancy_json:
        print(vacancy)
        if toggle:
            vacancy = vacancy['salary']
        if vacancy.get(salary_from) and vacancy.get(salary_to):
            salary.append(int((vacancy.get(salary_from) + vacancy.get(salary_to)) / 2))
        elif vacancy.get(salary_from) and not vacancy.get(salary_to):
            salary.append(int(vacancy.get(salary_from) * 1.2))
        elif vacancy.get(salary_to) and not vacancy.get(salary_from):
            salary.append(int(vacancy.get(salary_to) * 0.8))
        else:
            pass
    return int((sum(salary)) / len(salary))


def predict_rub_salary_for_sj(languages):
    url = "https://api.superjob.ru/2.0/vacancies/"
    ids = 'Программист'
    vacancies_info = {}
    vacancies_salary = []
    for language in languages:
        print(language)
        for page in count(0):
            vacancies_salary_for_page = []
            headers = {'X-Api-App-Id': load_keys('SUPER_JOB_KEY')}
            params = {
                "keyword": language,
                'town': 4,
                'page': page,
                'count': 100,
                'payment': 'RUB',
                'currency': 'rub'
            }
            vacancies_data = get_response(url, headers, params)
            if page >= 6:
                break
            vacancies_salary_for_page.append(predict_salary(vacancies_data['objects'], 'payment_from', 'payment_to'))
            vacancies_salary.extend(vacancies_salary_for_page)
        lang = {
            "vacancies_found": vacancies_data['found'],
            "vacancies_processed": vacancies_data['found'],
            "average_salary": int((sum(vacancies_salary)) / len(vacancies_salary))}
        vacancies_info[language] = lang
        with open(f'vacancies_info_hh.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_info, file, ensure_ascii=False, indent=4)




    # with open(f'vacancies_SJ.json', 'w', encoding='utf-8') as file:
    #     json.dump(vacancies_data, file, ensure_ascii=False, indent=4)
    # with open(f'vacancies_SJ.json', 'r', encoding='utf-8') as file2:
    #     vacancies = json.load(file2)
    #     predict_salary(vacancies, 'payment_from', 'payment_to')
    # for vacancy in vacancies['objects']:
    #     print(f"Название вакансии: {vacancy['profession']}")
    #     print(f"Зарплата: от {vacancy['payment_from']} до {vacancy['payment_to']} руб.")
    #     print(f"Город: {vacancy['town']['title']}")
    #     print('-' * 40)


def main():
    languages = {
        "JavaScript",
        "Python",
        "Java",
        "C#",
        "PHP",
        "C++",
        "TypeScript",
        "Swift",
        "Go",
        "Shell",
        "C",
        "KOTLIN",
        "1C"
    }
    predict_rub_salary_for_sj(languages)
    # predict_rub_salary_for_hh(languages)


if __name__ == '__main__':
    main()
