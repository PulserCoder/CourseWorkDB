import json

import psycopg2


def create_and_fill_table_from_json(name: str) -> None:
    with open(name, 'r') as f:
        data = json.load(f)
        conn = psycopg2.connect(
            dbname='coursework',
            user='postgres',
            password='21062006mMm',
            host='localhost'
        )
        cursor = conn.cursor()

        with open('commands.sql', 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()

        try:
            cursor.execute(sql_script)
            print("SQL script executed successfully")
        except Exception as e:
            print(f"An error occurred: {e}")

        cur = conn.cursor()
        for element in data:
            cur.execute(f"""
                INSERT INTO company (name) VALUES (%s) RETURNING company_id
            """, (element["company_name"], ))
            company_id = cur.fetchone()[0]
            conn.commit()
            for vacancy in element["vacancies"]:
                cur.execute(
                    f"INSERT INTO vacancies (name, salary_from, salary_to, url, company_id) VALUES (%s, %s, %s, %s, %s)",
                    (vacancy["name"], vacancy['salary'].get('from', 0), vacancy['salary'].get('to', 0), vacancy["url"], company_id))

        conn.commit()
        print('Success')


create_and_fill_table_from_json('companies.json')