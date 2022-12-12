import csv


class Vacancy:
    currency_to_rub = {
         "UAH": 1.64, "BYR": 23.91, "KZT": 0.13, "EUR": 59.90, "GEL": 21.74, "AZN": 35.68, "KGS": 0.76,
         "RUR": 1,  "USD": 60.66, "UZS": 0.0055,
    }

    def __init__(self, vacancy):
        self.name = vacancy['name']
        self.year = int(vacancy['published_at'][:4])
        self.sal_To = int(float(vacancy['salary_to']))
        self.sal_From = int(float(vacancy['salary_from']))
        self.area_name = vacancy['area_name']
        self.sal_Currency = vacancy['salary_currency']
        self.sal_Average = self.currency_to_rub[self.sal_Currency] * (self.sal_From + self.sal_To) / 2




class DataSet:
    def __init__(self, file_name, vacancy):
        self.file = file_name
        self.vacancy = vacancy

    def csv_reader(self):

        salary = {}
        salaryVacName = {}
        numbVacancies = {}
        vacNum_name = {}
        salary_city = {}
        head = []
        salary_number = {}
        count_of_vacancies = 0
        with open(self.file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    head = row
                    head_len = len(row)
                elif '' not in row and len(row) == head_len:
                    vacancy = Vacancy(dict(zip(head, row)))

                    self.vacYear_salary(salary, vacancy)

                    if vacancy.year not in numbVacancies:
                        numbVacancies[vacancy.year] = 1
                    else:
                        numbVacancies[vacancy.year] += 1

                    if vacancy.name.find(self.vacancy) != -1:
                        self.vacYear_salary(salaryVacName, vacancy)

                        if vacancy.year not in vacNum_name:
                            vacNum_name[vacancy.year] = 1
                        else:
                            vacNum_name[vacancy.year] += 1

                    self.vacAreaName_cityAndNumber(salary_city, salary_number, vacancy)

                    count_of_vacancies += 1

        salaryVacName, vacNum_name = self.notSalaryVacName(numbVacancies, salary, salaryVacName)

        dict = {}
        for year, list_of_salaries in salary.items():
            dict[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        dict2 = {}
        for year, list_of_salaries in salaryVacName.items():
            if len(list_of_salaries) == 0:
                dict2[year] = 0
            else:
                dict2[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        dict3 = {}
        for year, list_of_salaries in salary_city.items():
            dict3[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        dict4 = {}
        for year, list_of_salaries in salary_number.items():
            dict4[year] = round(list_of_salaries / count_of_vacancies, 4)
        dict4 = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in dict4.items()]))
        dict4.sort(key=lambda a: a[-1], reverse=True)
        dict5 = dict4.copy()
        dict4 = dict(dict4)
        dict3 = list(filter(lambda a: a[0] in list(dict4.keys()), [(key, value) for key, value in dict3.items()]))
        dict3.sort(key=lambda a: a[-1], reverse=True)
        dict3 = dict(dict3[:10])

        print('Динамика уровня зарплат по годам: ' + str(dict))
        print('Динамика количества вакансий по годам: ' + str(numbVacancies))
        print('Динамика уровня зарплат по годам для выбранной профессии: ' + str(dict2))
        print('Динамика количества вакансий по годам для выбранной профессии: ' + str(vacNum_name))
        print('Уровень зарплат по городам (в порядке убывания): ' + str(dict3))
        print('Доля вакансий по городам (в порядке убывания): ' + str(dict(dict5[:10])))

    def vacAreaName_cityAndNumber(self, salary_city, salary_number, vacancy):
        if vacancy.area_name not in salary_city:
            salary_city[vacancy.area_name] = [vacancy.sal_Average]
        else:
            salary_city[vacancy.area_name].append(vacancy.sal_Average)
        if vacancy.area_name not in salary_number:
            salary_number[vacancy.area_name] = 1
        else:
            salary_number[vacancy.area_name] += 1

    def vacYear_salary(self, salary, vacancy):
        if vacancy.year not in salary:
            salary[vacancy.year] = [vacancy.sal_Average]
        else:
            salary[vacancy.year].append(vacancy.sal_Average)

    def notSalaryVacName(self, numbVacancies, salary, salaryVacName):
        if not salaryVacName:
            salaryVacName = salary.copy()
            salaryVacName = dict([(key, []) for key, value in salaryVacName.items()])
            vacNum_name = numbVacancies.copy()
            vacNum_name = dict([(key, 0) for key, value in vacNum_name.items()])
        return salaryVacName, vacNum_name


class InputConnect:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')

        data_set = DataSet(self.file_name, self.vacancy_name)
        data_set.csv_reader()


if __name__ == '__main__':
    InputConnect()