import requests
import json


def get_response(url, language, page=None):
    url = "https://api.hh.ru/vacancies"
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
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    vacancies_data = response.json()
    return vacancies_data



def predict_rub_salary(languages):
    url = "https://api.hh.ru/vacancies"
    headers = {
        'HH-User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    vacancies_info = {}
    for language in languages:
        try:
            for pages in range(get_response(url, language)['pages'] + 1):
                page = 0
                get_response(url, language)
                params = {
                    'text': f'Программист {language}',
                    'area': "1",
                    'page': {page},
                    'per_page': '100',
                    'resume_search_experience_period': 'all_time',
                    'currency': "RUR",
                    'only_with_salary': 'true'
                }
                page += 1
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                vacancies_data = response.json()
                final_vacancies = []
                vacancies = []
                for vacancy in vacancies_data['items']:
                    if vacancy['salary'].get('from') and vacancy['salary'].get('to'):
                        vacancies.append(int((vacancy['salary'].get('from') + vacancy['salary'].get('to')) / 2))
                        final_vacancies.extend(vacancies)
                    if vacancy['salary'].get('from') and not vacancy['salary'].get('to'):
                        vacancies.append(int(vacancy['salary'].get('from') * 1.2))
                        final_vacancies.extend(vacancies)
                    if vacancy['salary'].get('to') and not vacancy['salary'].get('from'):
                        vacancies.append(int(vacancy['salary'].get('to') * 0.8))
                        final_vacancies.extend(vacancies)
                lang = {
                    "vacancies_found": vacancies_data['found'],
                    "vacancies_processed": len(final_vacancies),
                    "average_salary": int((sum(final_vacancies)) / len(final_vacancies))}
                vacancies_info[language] = lang
                print(len(final_vacancies))
                print(len(vacancies))
            with open(f'vacancies_info.json', 'w', encoding='utf-8') as file:
                json.dump(vacancies_info, file, ensure_ascii=False, indent=4)
        except:
            print("Error")
        # with open(f'vacancies_info.json', 'w', encoding='utf-8') as file:
        #     json.dump(vacancies_info, file, ensure_ascii=False, indent=4)


# def counts_pages(language):
#     url = "https://api.hh.ru/vacancies"
#     headers = {
#         'HH-User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
#                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
#     }
#     params = {
#         'text': f'Программист {language}',
#         'area': "1",
#         'page': '0',
#         'per_page': '100',
#         'resume_search_experience_period': 'all_time',
#         'currency': "RUR",
#         'only_with_salary': 'true'
#     }
#     response = requests.get(url, headers=headers, params=params)
#     response.raise_for_status()
#     vacancies_data = response.json()
#     print(f"{language} : {vacancies_data['pages']}")
#     return vacancies_data['pages']


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
    predict_rub_salary(languages)


if __name__ == '__main__':
    main()
