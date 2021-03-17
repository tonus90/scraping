"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
* Наименование вакансии.
* Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
* Ссылку на саму вакансию.
* Сайт, откуда собрана вакансия.
"""

from bs4 import BeautifulSoup
import requests
from pathlib import Path
import json
from time import sleep
from urllib.parse import urljoin

class JobParse:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    base_url = 'https://hh.ru'

    def __init__(self, start_url: str, params:dict, save_path: Path, max_pages):
        self.start_url = start_url
        self.save_path = save_path
        self.params = params
        self.max_pages = max_pages

    def _get_response(self, url):
        while True:
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return response
            sleep(0.5)

    def _get_soup(self, url):
        response = self._get_response(url)
        return BeautifulSoup(response.text, 'html.parser')

    def _parse(self, vacancy):
        data = {}
        for key, funk in self._get_template().items():
            try:
                data[key] = funk(vacancy)
            except AttributeError:
                pass
        return data

    def _save(self, data:dict, file_path:Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))

    def run(self):
        url = self.start_url
        cnt = 0
        cnt_pages = 0
        while url:
            if cnt_pages < int(self.max_pages):
                soup = self._get_soup(url)
                get = soup.find('a', attrs={'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
                try:
                    url = urljoin(self.base_url, get.attrs.get('href', ''))
                except AttributeError as err:
                    print(err)
                    url = False
                catalog_vac = soup.find('div', attrs={'class': "vacancy-serp"})
                for vac in catalog_vac.find_all('div', attrs={'class': "vacancy-serp-item"}):
                    vacancies_data = self._parse(vac)
                    cnt += 1
                    vac_path = self.save_path.joinpath(f'vacancy{str(cnt)}.json')
                    self._save(vacancies_data, vac_path)
                cnt_pages += 1
                print(cnt_pages)
                print(cnt)
            else: break

    def _get_template(self):
        return {
            'name': lambda vac: vac.find('a', attrs={'class': "bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy"}).text,
            'url': lambda vac: vac.find('a', attrs={'class': "bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy"}).attrs.get('href', ''),
            'min_sal': self._get_min_salary,
            'max_sal': self._get_max_salary,
            'valuta': self._get_valuta,
        }


    def _get_min_salary(self, vac):
        work = vac.find('div', attrs={'class': 'vacancy-serp-item__sidebar'})
        try:
            sal = work.find('span', attrs={'class': 'bloko-section-header-3 bloko-section-header-3_lite'}).text
        except Exception as err:
            print(err)
            return None
        my_list = sal.split()
        if my_list[0].isdigit():
            min_s = f'{my_list[0]}{my_list[1].split("-")[0]}'
        elif my_list[0] == 'от':
            min_s = f'{my_list[1]}{my_list[2]}'
        elif my_list[0] == 'до':
            min_s = None
        elif len(my_list[0]) == 5:
            get = my_list[0].split('-')
            min_s = f'{get[0]}'
        else:
            min_s = None
        return min_s

    def _get_max_salary(self, vac):
        work = vac.find('div', attrs = {'class': 'vacancy-serp-item__sidebar'})
        try:
            sal = work.find('span', attrs={'class': 'bloko-section-header-3 bloko-section-header-3_lite'}).text
        except Exception as err:
            print(err)
            return None
        my_list = sal.split()
        if my_list[0].isdigit():
            max_s = (f'{my_list[1].split("-")[1]}{my_list[2]}')
        elif my_list[0] == 'от':
            max_s = None
        elif my_list[0] == 'до':
            max_s = (f'{my_list[1]}{my_list[2]}')
        elif len(my_list[0]) == 5:
            get = my_list[0].split('-')
            max_s = f'{get[1]}{my_list[1]}'
        else:
            max_s = None
        return max_s

    def _get_valuta(self, vac):
        work = vac.find('div', attrs = {'class': 'vacancy-serp-item__sidebar'})
        try:
            sal = work.find('span', attrs={'class': 'bloko-section-header-3 bloko-section-header-3_lite'}).text
        except Exception as err:
            print(err)
            return None
        my_list = sal.split()
        if len(my_list[0]) == 5:
            val = my_list[2]
        else: val = my_list[3]
        return val


if __name__ == '__main__':
    name = input('Введите должность: ')
    max_pages = input('Сколько страниц сканрировать?: ')
    url = 'https://hh.ru/search/vacancy'
    params = {'area': 1,
              'fromSearchLine': True,
              'st': 'searchVacancy',
              'text': name,
              }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    save_path = Path('vacancies_hh')
    if not save_path.exists():
        save_path.mkdir()
    parser = JobParse(url, params, save_path, max_pages)
    try:
        parser.run()
    except ValueError as err:
        print(err)
        pass
