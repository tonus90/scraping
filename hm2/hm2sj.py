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
from urllib.parse import urljoin

class JobParse:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    base_url = 'https://www.superjob.ru'

    def __init__(self, start_url: str, save_path: Path, max_pages):
        self.start_url = start_url
        self.save_path = save_path
        self.max_pages = max_pages
    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response

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
        url = self.start_url #первый урл стартовый дальше будем менять по кнопке дальше
        cnt = 0
        cnt_pages = 0
        while url:  #пока урл сущетсвует делаем
            if cnt_pages < int(self.max_pages):
                soup = self._get_soup(url) #суп
                button = soup.find('a', attrs={'class': 'icMQ_ bs_sM _3ze9n f-test-button-dalshe f-test-link-Dalshe'}) #вытащим кнопку дальше
                try:
                    url = urljoin(self.base_url, button.attrs.get('href', ''))
                except AttributeError as err:
                    print(err)
                    url = False
                for vac in soup.find_all('div', attrs={'class': "iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL"}):
                    vacancies_data = self._parse(vac)
                    cnt+=1
                    vac_path = self.save_path.joinpath(f'vacancy{str(cnt)}.json')
                    self._save(vacancies_data, vac_path)
                cnt_pages += 1
                print(cnt)
                print(cnt_pages)
            else: break

    def _get_template(self): #получим шаблон для словаря

        return {
            'name': lambda vac: vac.find('div', attrs={'class': "_3mfro PlM3e _2JVkc _3LJqf"}).text,
            'url': lambda vac: urljoin(self.base_url, vac.find('div', attrs={'class': "_3mfro PlM3e _2JVkc _3LJqf"}).find('a', attrs={'target': "_blank"}).attrs.get('href', '')),
            'min_sal': self._get_min_salary,
            'max_sal': self._get_max_salary,
            'valuta': self._get_valuta,
        }


    def _get_min_salary(self, vac): #получим мин зп
        work = vac.find('span', attrs={'class': "_1OuF_ _1qw9T f-test-text-company-item-salary"})
        sal = work.find('span', attrs={'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text
        if sal.lower()=='по договоренности':
            return None
        my_list = sal.split()
        if my_list[0].isdigit():
            min_s = f'{my_list[0]}{my_list[1]}'
        elif my_list[0] == 'от':
            min_s = f'{my_list[1]}{my_list[2]}'
        elif my_list[0] == 'до':
            min_s = None
        else:
            min_s = None
        return min_s

    def _get_max_salary(self, vac): #получим макс зп
        work = vac.find('span', attrs={'class': "_1OuF_ _1qw9T f-test-text-company-item-salary"})
        sal = work.find('span', attrs={'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text
        if sal.lower()=='по договоренности':
            return None
        my_list = sal.split()
        try:
            if my_list[0].isdigit():
                max_s = (f'{my_list[3]}{my_list[4]}')
            elif my_list[0] == 'от':
                max_s = None
            elif my_list[0] == 'до':
                max_s = (f'{my_list[1]}{my_list[2]}')
            else:
                max_s = None
        except IndexError as err: #если зп ровно 120 000 в мес, то запишется в мин, а тут отловим ошибку
            print(err)
            max_s = None
        return max_s

    def _get_valuta(self, vac): #получим валюту
        work = vac.find('span', attrs={'class': "_1OuF_ _1qw9T f-test-text-company-item-salary"})
        sal = work.find('span', attrs={'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text
        if sal.lower() == 'по договоренности':
            return None
        my_list = sal.split()

        if my_list[0].isdigit() and len(my_list) > 3:
            val = my_list[5]
        elif my_list[0].lower() == 'от' or my_list[0].lower() == 'до':
            val = my_list[3]
        elif my_list[0].lower() == 'по':
            val = None
        else:
            val = 'руб'
        return val


if __name__ == '__main__':
    name = input('Введите должность: ')
    max_pages = input('Сколько страниц сканрировать?: ')
    url = f'https://www.superjob.ru/vacancy/search/?keywords={name}'
    save_path = Path('vacancies_sj')

    if not save_path.exists():
        save_path.mkdir()

    parser = JobParse(url, save_path, max_pages)
    try:
        parser.run()
    except ValueError as err:
        print(err)
        pass