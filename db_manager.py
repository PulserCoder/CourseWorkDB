from typing import Dict, List, Tuple

import psycopg2


class DBManager():
    def __init__(self):
        """Initialize the database connection"""
        self.conn = psycopg2.connect(
            dbname='coursework',
            user='postgres',
            password='21062006mMm',
            host='localhost'
        )

    def get_companies_and_vacancies_count(self) -> Dict[str, int]:
        """
        Get the number of each company in the database
        :return dictionary with name and quantity
        """
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT company.name, COUNT(vacancies.name)
            FROM vacancies
            INNER JOIN company ON vacancies.company_id = company.company_id
            GROUP BY company.name
            """)
            data = cur.fetchall()
            d = {}
            for i in data:
                d[i[0]] = i[1]
            return d

    def get_all_vacancies(self) -> List[str]:
        """
        Get the list of all vacancies in database
        :return: list with vacancies
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies INNER JOIN company ON
                vacancies.company_id = company.company_id
            """)
            data = cur.fetchall()
        result = []
        for i in data:
            f = i[2]
            s = i[3]
            if f is None:
                f = 0
            elif s is None:
                s = 0
            salary = max(f, s)
            result.append(
                f"Должность: {i[1]}, зарплата: {salary}, работодатель: {i[-1]} Ссылка: {i[4]}"
            )
        return result

    def get_avg_salary(self) -> float:
        """
        Get average salary from vacancies
        :return: Average salary
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT AVG(salary) FROM"
                " (SELECT GREATEST(vacancies.salary_to, vacancies.salary_from)"
                " AS salary FROM vacancies) AS subquery")
            return cur.fetchone()[0]


    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """
        Get all vacancies with higher salary than average
        :return list with all info of vacancies which higher salary than average
        """
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM vacancies WHERE GREATEST(salary_to, salary_from) > {self.get_avg_salary()}""")
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Get a list of vacancies which contain the given keyword
        :param keyword: str that should be in vacancy's name
        :return: list of all info about vacancies with the given keyword
        """
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM vacancies WHERE name LIKE '%{keyword}%'
            """)
            return cur.fetchall()



if __name__ == "__main__":
    a = DBManager()
    print(a.get_vacancies_with_keyword("Водитель"))
    print('---' * 20)
    print(a.get_vacancies_with_higher_salary())
    print('---' * 20)
    print(a.get_avg_salary())
    print('---' * 20)
    print(a.get_all_vacancies())
    print('---' * 20)
    print(a.get_companies_and_vacancies_count())