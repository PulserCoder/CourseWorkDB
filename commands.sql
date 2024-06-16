-- DO THIS FOR GET TABLES
CREATE TABLE company
(
    company_id SERIAL PRIMARY KEY,
    name       VARCHAR(255) NOT NULL
);

CREATE TABLE vacancies
(
    vacancy_id  SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    salary_from INT DEFAULT 0,
    salary_to   INT DEFAULT 0,
    url         TEXT
);

ALTER TABLE vacancies
    ADD COLUMN company_id INT;
ALTER TABLE vacancies
    ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES company (company_id);


-- DO THIS FOR DROP ALL TABLES
-- ALTER TABLE vacancies
--     DROP CONSTRAINT fk_company_id;
-- TRUNCATE TABLE vacancies CASCADE;
-- TRUNCATE TABLE company CASCADE;
--
--
--
-- TRUNCATE TABLE company RESTART IDENTITY CASCADE;


-- COMMANDS FOR TESTING
-- SELECT company.name, COUNT(vacancies.name)
-- FROM vacancies
--          INNER JOIN company ON vacancies.company_id = company.company_id
-- GROUP BY company.name;
--
--
-- SELECT *
-- FROM vacancies
--          INNER JOIN company ON vacancies.company_id = company.company_id;
--
--
-- SELECT AVG(salary) FROM (SELECT GREATEST(vacancies.salary_to, vacancies.salary_from) AS salary FROM vacancies) AS subquery;
--
--
-- SELECT * FROM vacancies WHERE GREATEST(salary_to, salary_from) > 150000;
