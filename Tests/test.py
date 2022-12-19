import unittest
from main import Vacancy, DataSet, InputConnect


class SalaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.salary = Vacancy({"name": 'Руководитель', "description": '<strong>Обязанности:</strong>', "key_skills": 'Организаторские', "experience_id": 'between3And6',
                  "premium": 'FALSE', "employer_name": 'ПМЦ Авангард',
                  "salary_from": '80000',
                  "salary_to": '100000', "salary_gross": 'FALSE',
                  "salary_currency": 'RUR', "area_name": 'Санкт-Петербург',
                  "published_at": '2022-07-17T18:23:06+0300'})

    def test_salary_from(self):
        self.assertEqual(self.salary.salary_from, 80000.0)

    def test_salary_to(self):
        self.assertEqual(self.salary.salary_to, 100000.0)

    def test_salary_currency(self):
        self.assertEqual(self.salary.salary_currency, 'RUR')


class VacancyTests(unittest.TestCase):

    def setUp(self) -> None:
        self.vacancy = Vacancy({"name": 'Руководитель', "description": '<strong>Обязанности:</strong>', "key_skills": 'Организаторские', "experience_id": 'between3And6',
                  "premium": 'FALSE', "employer_name": 'ПМЦ Авангард',
                  "salary_from": '80000',
                  "salary_to": '100000', "salary_gross": 'FALSE',
                  "salary_currency": 'RUR', "area_name": 'Санкт-Петербург',
                  "published_at": '2022-07-17T18:23:06+0300'})

    def test_vacancy_type(self):
        self.assertEqual(type(self.vacancy).__name__, 'Vacancy')

    def test_vacancy_area(self):
        self.assertEqual(self.vacancy.area_name, 'Санкт-Петербург')

    def test_salary_from_vacancy(self):
        self.assertEqual(self.vacancy.salary_from, 80000.0)

    def test_vacancy_year(self):
        self.assertEqual(self.vacancy.year, 2022)

    def test_vacancy_is_suitible(self):
        self.assertTrue(self.vacancy.name, 'Руководитель')

class TestDataSet(unittest.TestCase):

    def setUp(self) -> None:
        self.dataset = DataSet(r"C:\Users\nikit\Downloads\vacancies_small.csv", '')

    def test_dataset_type(self):
        self.assertEqual(type(self.dataset).__name__, 'DataSet')

    def test_dataset_length(self):
        self.assertEqual(self.dataset.vacancy_name, '')