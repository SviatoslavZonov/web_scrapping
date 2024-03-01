import requests
from bs4 import BeautifulSoup
import json

# ссылка с ключевыми словами
url = 'https://spb.hh.ru/search/vacancy?text=Python+django+flask&salary=&ored_clusters=true&enable_snippets=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110 '}

def get_page(url):
    return requests.get(url, headers=headers)

# ищем по тегам инфо
def parser_vacansies(tag_vacancy):
    link = tag_vacancy.find('a', class_='bloko-link')['href']
    salary = tag_vacancy.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    if salary:
        salary = salary.text.strip()
    else:
        salary = 'Не указана'
    company = tag_vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text.strip()
    city = tag_vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
    return {
        'link': link,
        'salary': salary.replace('\u202f', ' '),
        'company': company.replace('\xa0', ' ').strip(),
        'city': city.replace('\xa01\xa0', '...')
    }

# записываем в json
def write_json (data, file_name):
    data = json.dumps(data)
    data = json.loads(data)
    with open(file_name, 'a', encoding='utf-8') as file:
        json.dump(data, file)
        file.write('\n')

# парсим
def main():
    main_html = get_page(url).text
    soup = BeautifulSoup(main_html, features='html5lib')
    vacansies = soup.find_all('div', class_="serp-item")
    for vacancy in vacansies:
        parsed = parser_vacansies(vacancy)
        print(parsed)
        write_json(parsed, 'vacancies_hh.json')


if __name__ == '__main__':
    main()