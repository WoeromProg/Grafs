import csv


class Vacancy:
    """Класс для представления вакансии
    Attributes:
        currency_to_rub (dict): Курс валют по отношению к рублю
        name (str): название вакансии
        year (int): год
        sal_To(int): Верхняя граница вилки оклада
        sal_From(int): Нижняя граница вилки оклада
        sal_Currency(str): Валюта оклада
        sal_Average(float): Средний оклад
    """

    currency_to_rub = {
         "UAH": 1.64, "BYR": 23.91, "KZT": 0.13, "EUR": 59.90, "GEL": 21.74, "AZN": 35.68, "KGS": 0.76,
         "RUR": 1,  "USD": 60.66, "UZS": 0.0055,
    }

    def __init__(self, vacancy):
        """Инициализирует объект vacancy, выполняет конвертацию для целочисленных полей"""
        self.name = vacancy['name']
        self.year = int(vacancy['published_at'][:4])
        self.sal_To = int(float(vacancy['salary_to']))
        self.sal_From = int(float(vacancy['salary_from']))
        self.area_name = vacancy['area_name']
        self.sal_Currency = vacancy['salary_currency']
        self.sal_Average = self.currency_to_rub[self.sal_Currency] * (self.sal_From + self.sal_To) / 2




class DataSet:
    """Класс для чтения файла, работы с ним"""
    def __init__(self, file_name, vacancy):
        """Инициализирует файл и вакансию"""
        self.file = file_name
        self.vacancy = vacancy

    def csv_reader(self):
        """Attributes:
                salary(dict): Зарплата, словарь
                salaryVacName(dict): количество вакансий по годам
                numbVacancies(dict): кол-во вакансий
                vacNum_name(dict): Количество вакансий по годам для выбранной профессии
                salary_city(dict): оклад в зависимости от города
                head(list): Столбцы из файла
                salary_number = {}(dict): Количество зарплат"""



        salary = {}
        salaryVacName = {}
        numbVacancies = {}
        vacNum_name = {}
        salary_city = {}
        head = []
        salary_number = {}
        count_of_vacancies = 0

        """Чтение файла, принимает файл"""
        with open(self.file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            """Запись столбцов и их количества, принимает файл"""
            for index, row in enumerate(reader):
                if index == 0:
                    head = row
                    head_len = len(row)
                    """Записываем вакансию если она полностью заполнена"""
                elif '' not in row and len(row) == head_len:
                    vacancy = Vacancy(dict(zip(head, row)))
                    """Записываем к вакансии среднее значение оклада"""
                    self.vacYear_salary(salary, vacancy)

                    """Динамика количества вакансий по годам"""
                    if vacancy.year not in numbVacancies:
                        numbVacancies[vacancy.year] = 1
                    else:
                        numbVacancies[vacancy.year] += 1

                    """Динамика количества вакансий по годам для выбранной профессии"""
                    if vacancy.name.find(self.vacancy) != -1:
                        self.vacYear_salary(salaryVacName, vacancy)

                        if vacancy.year not in vacNum_name:
                            vacNum_name[vacancy.year] = 1
                        else:
                            vacNum_name[vacancy.year] += 1

                    self.vacAreaName_cityAndNumber(salary_city, salary_number, vacancy)

                    count_of_vacancies += 1

        salaryVacName, vacNum_name = self.notSalaryVacName(numbVacancies, salary, salaryVacName)

        """Динамика уровня зарплат по годам"""
        dict1 = {}
        for year, list_of_salaries in salary.items():
            dict1[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        """Динамика уровня зарплат по годам для выбранной профессии"""
        dict2 = {}
        for year, list_of_salaries in salaryVacName.items():
            if len(list_of_salaries) == 0:
                dict2[year] = 0
            else:
                dict2[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        """Уровень зарплат по городам (в порядке убывания)"""
        dict3 = {}
        for year, list_of_salaries in salary_city.items():
            dict3[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        dict4 = {}
        for year, list_of_salaries in salary_number.items():
            dict4[year] = round(list_of_salaries / count_of_vacancies, 4)
        dict4 = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in dict4.items()]))
        dict4.sort(key=lambda a: a[-1], reverse=True)
        """Доля вакансий по городам (в порядке убывания)"""
        dict5 = dict4.copy()

        dict4 = dict1(dict4)
        dict3 = list(filter(lambda a: a[0] in list(dict4.keys()), [(key, value) for key, value in dict3.items()]))
        dict3.sort(key=lambda a: a[-1], reverse=True)
        dict3 = dict1(dict3[:10])

        print('Динамика уровня зарплат по годам: ' + str(dict1))
        print('Динамика количества вакансий по годам: ' + str(numbVacancies))
        print('Динамика уровня зарплат по годам для выбранной профессии: ' + str(dict2))
        print('Динамика количества вакансий по годам для выбранной профессии: ' + str(vacNum_name))
        print('Уровень зарплат по городам (в порядке убывания): ' + str(dict3))
        print('Доля вакансий по городам (в порядке убывания): ' + str(dict1(dict5[:10])))

    """Считает уровень зарплат по городам. Принимает значения: оклад по городам, количество окладов, вакансию"""
    def vacAreaName_cityAndNumber(self, salary_city, salary_number, vacancy):
        if vacancy.area_name not in salary_city:
            salary_city[vacancy.area_name] = [vacancy.sal_Average]
        else:
            salary_city[vacancy.area_name].append(vacancy.sal_Average)
        if vacancy.area_name not in salary_number:
            salary_number[vacancy.area_name] = 1
        else:
            salary_number[vacancy.area_name] += 1

    """Считает средний оклад по вакансии. Принимает оклад и вакансию"""
    def vacYear_salary(self, salary, vacancy):
        if vacancy.year not in salary:
            salary[vacancy.year] = [vacancy.sal_Average]
        else:
            salary[vacancy.year].append(vacancy.sal_Average)

    """Динамика количества вакансий по годам для выбранной профессии. Принимает количество вакансии, оклад, оклад по професии
        Выводит словарь окладов для вакансии и словарь количества вакансий"""
    def notSalaryVacName(self, numbVacancies, salary, salaryVacName):
        if not salaryVacName:
            salaryVacName = salary.copy()
            salaryVacName = dict([(key, []) for key, value in salaryVacName.items()])
            vacNum_name = numbVacancies.copy()
            vacNum_name = dict([(key, 0) for key, value in vacNum_name.items()])
        return salaryVacName, vacNum_name


class InputConnect:
    """Класс для определения формы вывода в зависимости от потребностей пользователя"""

    """Инициализация пути для файла и требуемой вакансии"""
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')

        data_set = DataSet(self.file_name, self.vacancy_name)
        data_set.csv_reader()


if __name__ == '__main__':
    InputConnect()