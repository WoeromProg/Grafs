import csv


class Vacancy:
    """Класс для представления вакансии
        Attributes:
            currency_to_rub (dict): Курс валют по отношению к рублю
            name (str): название вакансии
            year (int): год
            salary_to(int): Верхняя граница вилки оклада
            salary_from(int): Нижняя граница вилки оклада
            salary_currency(str): Валюта оклада
            salary_average(float): Средний оклад
        """
    currency_to_rub = {
        "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
        "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055,
    }

    def __init__(self, vacancy):
        """Инициализирует объект vacancy, выполняет конвертацию для целочисленных полей
        >>> Vacancy({"name": 'Руководитель', "description": '<strong>Обязанности:</strong>', "key_skills": 'Организаторские', "experience_id": 'between3And6',"premium": 'FALSE', "employer_name": 'ПМЦ Авангард',"salary_from": '90000',"salary_to": '100000', "salary_gross": 'FALSE',"salary_currency": 'RUR', "area_name": 'Санкт-Петербург',"published_at": '2022-07-17T18:23:06+0300'}).salary_average
        95000.0
        >>> Vacancy({"name": 'Руководитель', "description": '<strong>Обязанности:</strong>', "key_skills": 'Организаторские', "experience_id": 'between3And6',"premium": 'FALSE', "employer_name": 'ПМЦ Авангард',"salary_from": '90000',"salary_to": '100000', "salary_gross": 'FALSE',"salary_currency": 'RUR', "area_name": 'Санкт-Петербург',"published_at": '2022-07-17T18:23:06+0300'}).salary_currency
        'RUR'
        >>> Vacancy({"name": 'Руководитель', "description": '<strong>Обязанности:</strong>', "key_skills": 'Организаторские', "experience_id": 'between3And6',"premium": 'FALSE', "employer_name": 'ПМЦ Авангард',"salary_from": '90000',"salary_to": '100000', "salary_gross": 'FALSE',"salary_currency": 'RUR', "area_name": 'Санкт-Петербург',"published_at": '2022-07-17T18:23:06+0300'}).year
        2022


"""
        self.name = vacancy['name']
        self.salary_from = int(float(vacancy['salary_from']))
        self.salary_to = int(float(vacancy['salary_to']))
        self.salary_currency = vacancy['salary_currency']
        self.salary_average = self.currency_to_rub[self.salary_currency] * (self.salary_from + self.salary_to) / 2
        self.area_name = vacancy['area_name']
        self.year = int(vacancy['published_at'][:4])


class DataSet:
    """Класс для чтения файла, работы с ним"""

    def __init__(self, file_name, vacancy_name):
        """Инициализирует файл и вакансию"""
        self.file_name = file_name
        self.vacancy_name = vacancy_name

    def csv_reader(self):
        """Attributes:
                       salary(dict): Зарплата, словарь
                       salary_of_vacancy_name(dict): количество вакансий по годам
                       vacancies_number(dict): кол-во вакансий
                       vacancies_number_of_vacancy_name(dict): Количество вакансий по годам для выбранной профессии
                       salary_city(dict): оклад в зависимости от города
                       head(list): Столбцы из файла
                       salary_number = {}(dict): Количество зарплат"""

        salary = {}
        salary_of_vacancy_name = {}
        vacancies_number = {}
        vacancies_number_of_vacancy_name = {}
        salary_city = {}
        header = []
        salary_number = {}
        count_of_vacancies = 0

        with open(self.file_name, mode='r', encoding='utf-8-sig') as file:
            """Чтение файла, принимает файл"""
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                """Запись столбцов и их количества, принимает файл"""
                if index == 0:
                    header = row
                    csv_header_length = len(row)
                    """Записываем вакансию если она полностью заполнена"""
                elif '' not in row and len(row) == csv_header_length:
                    """Записываем к вакансии среднее значение оклада"""
                    vacancy = Vacancy(dict(zip(header, row)))

                    if vacancy.year not in salary:
                        """Динамика количества вакансий по годам"""
                        salary[vacancy.year] = [vacancy.salary_average]
                    else:
                        salary[vacancy.year].append(vacancy.salary_average)

                    if vacancy.year not in vacancies_number:
                        vacancies_number[vacancy.year] = 1
                    else:
                        vacancies_number[vacancy.year] += 1


                    if vacancy.name.find(self.vacancy_name) != -1:
                        """Динамика количества вакансий по годам для выбранной профессии"""
                        if vacancy.year not in salary_of_vacancy_name:
                            salary_of_vacancy_name[vacancy.year] = [vacancy.salary_average]
                        else:
                            salary_of_vacancy_name[vacancy.year].append(vacancy.salary_average)

                        if vacancy.year not in vacancies_number_of_vacancy_name:
                            vacancies_number_of_vacancy_name[vacancy.year] = 1
                        else:
                            vacancies_number_of_vacancy_name[vacancy.year] += 1

                    if vacancy.area_name not in salary_city:
                        salary_city[vacancy.area_name] = [vacancy.salary_average]
                    else:
                        salary_city[vacancy.area_name].append(vacancy.salary_average)

                    if vacancy.area_name not in salary_number:
                        """Доля вакансий по городам (в порядке убывания)"""
                        salary_number[vacancy.area_name] = 1
                    else:
                        salary_number[vacancy.area_name] += 1

                    count_of_vacancies += 1

        if not salary_of_vacancy_name:
            """Уровень зарплат по городам (в порядке убывания)"""
            salary_of_vacancy_name = salary.copy()
            salary_of_vacancy_name = dict([(key, []) for key, value in salary_of_vacancy_name.items()])
            vacancies_number_of_vacancy_name = vacancies_number.copy()
            vacancies_number_of_vacancy_name = dict(
                [(key, 0) for key, value in vacancies_number_of_vacancy_name.items()])

        """Динамика уровня зарплат по годам"""
        stats = {}
        for year, list_of_salaries in salary.items():
            stats[year] = int(sum(list_of_salaries) / len(list_of_salaries))
            """Динамика уровня зарплат по годам для выбранной профессии"""
        stats2 = {}
        """Уровень зарплат по городам (в порядке убывания)"""
        for year, list_of_salaries in salary_of_vacancy_name.items():
            if len(list_of_salaries) == 0:
                stats2[year] = 0
            else:
                stats2[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        stats3 = {}
        for year, list_of_salaries in salary_city.items():
            stats3[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        stats4 = {}
        for year, list_of_salaries in salary_number.items():
            stats4[year] = round(list_of_salaries / count_of_vacancies, 4)
        stats4 = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in stats4.items()]))
        stats4.sort(key=lambda a: a[-1], reverse=True)
        stats5 = stats4.copy()
        """Доля вакансий по городам (в порядке убывания)"""
        stats4 = dict(stats4)
        stats3 = list(filter(lambda a: a[0] in list(stats4.keys()), [(key, value) for key, value in stats3.items()]))
        stats3.sort(key=lambda a: a[-1], reverse=True)
        stats3 = dict(stats3[:10])

        print('Динамика уровня зарплат по годам: ' + str(stats))
        print('Динамика количества вакансий по годам: ' + str(vacancies_number))
        print('Динамика уровня зарплат по годам для выбранной профессии: ' + str(stats2))
        print('Динамика количества вакансий по годам для выбранной профессии: ' + str(vacancies_number_of_vacancy_name))
        print('Уровень зарплат по городам (в порядке убывания): ' + str(stats3))
        print('Доля вакансий по городам (в порядке убывания): ' + str(dict(stats5[:10])))


class InputConnect:
    """Отвечает за ввод местоположения файла и фильтра по профессии"""
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')

        data_set = DataSet(self.file_name, self.vacancy_name)
        data_set.csv_reader()


if __name__ == '__main__':
    InputConnect()