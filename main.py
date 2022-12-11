import csv
import re
import os
import sys

from prettytable import PrettyTable
from prettytable import ALL

mytable = PrettyTable()
mytable.field_names = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                       "Название региона", "Дата публикации вакансии"]
dict_numbers_field = {"№": 0, "Название": 1, "Описание": 2, "Навыки": 3, "Опыт работы": 4, "Премиум-вакансия": 5,
                      "Компания": 6, "Оклад": 7, "Идентификатор валюты оклада": 7,
                      "Название региона": 8, "Дата публикации вакансии": 9}
dict_vacancies = {"name": "Название", "description": "Описание", "key_skills": "Навыки", "experience_id": "Опыт работы",
                  "premium": "Премиум-вакансия", "employer_name": "Компания",
                  "salary_from": "Нижняя граница вилки оклада",
                  "salary_to": "Верхняя граница вилки оклада", "salary_gross": "Оклад",
                  "salary_currency": "Идентификатор валюты оклада", "area_name": "Название региона",
                  "published_at": "Дата публикации вакансии"}


def csv_reader(file_name):
    title_list = []
    list = []
    with open(file_name, 'r', encoding="UTF_8_sig") as file:
        reader = csv.reader(file, delimiter=',')
        empty = (os.stat(file_name).st_size == 0)
        if empty == True:
            print("Пустой файл")
            sys.exit()
        for i, x in enumerate(reader):
            if i == 0:
                title_list = x
                string_lenght = len(x)
            else:
                if '' not in x and string_lenght == len(x):
                    if len(x) == len(dict_vacancies):
                        list += [x]
    return title_list, list


def csv_filer(reader):
    list_naming = []
    for string in reader[1]:
        dict_t = {}
        for i, x in enumerate(string):
            string[i] = re.sub(r'(\<(/?[^>]+)>)', '', string[i])
            string[i] = Bool(NewLine(string[i]))
            dict_t[reader[0][i]] = string[i]
        list_naming.append(dict_t)
    return list_naming


def formatter(row):
    dict_work_experience = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет",
                            "between3And6": "От 3 до 6 лет", "moreThan6": "Более 6 лет"}
    dict_currencies = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
                       "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли",
                       "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум"}
    for x in row:
        listt = []
        for key, value in x.items():
            if value in dict_work_experience:
                x[key] = dict_work_experience[value]
            if value in dict_currencies:
                x[key] = dict_currencies[value]
            if 'published_at' in key:
                y = x[key].replace('-', ' ').partition('T')[0].split()
                x[key] = y[2] + "." + y[1] + '.' + y[0]
            if 'salary_from' in key:
                p = str(int(float(x[key])))
                if len(p) == 6:
                    p = p[0:3] + ' ' + p[3::]
                if len(p) == 5:
                    p = p[0:2] + ' ' + p[2::]
                if len(p) == 4:
                    p = p[0] + ' ' + p[1::]
                listt.append(p)
            if 'salary_to' in key:
                p = str(int(float(x[key])))
                if len(p) == 6:
                    p = p[0:3] + ' ' + p[3::]
                if len(p) == 5:
                    p = p[0:2] + ' ' + p[2::]
                if len(p) == 4:
                    p = p[0] + ' ' + p[1::]
                listt.append(p)
            if 'salary_gross' in key:
                if x[key] == "Нет":
                    x[key] = ' (С вычетом налогов)'
                if x[key] == 'Да':
                    x[key] = ' (Без вычета налогов)'
                listt.append(x[key])
            if "key_skills" in key:
                x[key] = x[key].split('?')
                x[key] = ('\n'.join(x[key]))

        if len(listt) == 3:
            p = listt[0] + ' - ' + listt[1] + ' (' + x['salary_currency'] + ')' + listt[2]
            x['salary_gross'] = p
    return row


def print_vacansies(dict, numbers, colums, filter_name):
    dict = formatter(dict)
    y = 0
    count = 1
    for x in dict:
        y += 1
        string = ''
        for i in x:
            if dict_vacancies[i] == "Нижняя граница вилки оклада":
                continue
            if dict_vacancies[i] == "Верхняя граница вилки оклада":
                continue
            if dict_vacancies[i] == "Идентификатор валюты оклада":
                continue
            else:
                if len(x[i]) > 100:
                    x[i] = x[i][0:100] + '...'
                string += str(x[i]) + '|'
        string = str(count) + '|' + string
        string = string.rstrip('|')
        string_list = string.split('|')
        if filter_name != "":
            flag = True
            x = filter_name.split(': ')
            if x[0] not in dict_numbers_field:
                print("Параметр поиска некорректен")
                sys.exit()
            numbers_title = dict_numbers_field[x[0]]
            string_no_list = string_list[numbers_title].replace('\n', ', ')
            if 3 == numbers_title:
                if ', ' in x[1]:
                    x_list = x[1].split(', ')
                    a = string_no_list.split(', ')
                    b = x_list
                    d = [x for y in b for x in a if y in x and x == y]
                    if len(d) == len(x_list):
                        mytable.add_row(string.split('|'))
                        count += 1
                flag = False
                for i in string_no_list.split(', '):
                    if x[1] == i or x[1] + '...' == i:
                        mytable.add_row(string.split('|'))
                        count += 1
                        flag = False
            if 7 == numbers_title and x[0] != 'Идентификатор валюты оклада':
                list_oklad = []
                for i in string_no_list:
                    if i == "-":
                        list_oklad.append('-')
                    try:
                        i_int = int(i)
                        list_oklad.append(str(i_int))
                    except:
                        pass
                oklad_str = ("".join(list_oklad)).split('-')
                if int(oklad_str[0]) <= int(x[1]) <= int(oklad_str[1]):
                    mytable.add_row(string.split('|'))
                    count += 1

            if 1 == numbers_title:
                if x[1] == string_no_list:
                    flag = False
                    mytable.add_row(string.split('|'))
                    count += 1
            else:
                if x[1] in string_no_list and flag:
                    mytable.add_row(string.split('|'))
                    count += 1


        else:
            mytable.add_row(string.split('|'))
            count += 1
    mytable.hrules = ALL
    mytable.max_width = 20
    mytable.align = "l"
    table = lambda x, p: x.get_string(start=numbers[0] - 1, end=numbers[1] - 1, fields=colums) if len(
        numbers) == 2 else x.get_string(start=numbers[0] - 1, end=p, fields=colums)
    if count > 1:
        print(table(mytable, y))
    else:
        print("Ничего не найдено")
        sys.exit()


def NewLine(str):
    if str.count('\n') != 0:
        list = str.replace('\n', '?')
        list = " ".join(list.split())
        return list
    else:
        str = " ".join(str.split())
        return str


def Bool(str):
    if str == "False" or str == "FALSE":
        return "Нет"
    if str == "True" or str == "TRUE":
        return "Да"
    return str


file_name = input()
filter_name = input()
if ':' not in filter_name and filter_name != '':
    print("Формат ввода некорректен")
    sys.exit()
reader = csv_reader(file_name)
if len(reader[1]) == 0:
    print("Нет данных")
    sys.exit()
else:
    dict = csv_filer(reader)
    numbers = input().split(' ')
    if numbers[0] != '':
        for i in range(len(numbers)):
            numbers[i] = int(numbers[i])
    else:
        numbers[0] = 1
    colums = ['№'] + input().split(', ')
    if colums[1] == '':
        colums = mytable.field_names
    print_vacansies(dict, numbers, colums, filter_name)