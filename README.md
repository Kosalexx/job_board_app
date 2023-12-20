# job_board_app

Job board service (hh.ru or similar analog).

    The main goal of the project is to learn Django framework (DRF).

___


## Contents:

- [Technologies](#technologies)
- [Description](#description)
- [Installation and starting](#installation-and-starting)
- [Authors](#authors)

---

## Technologies


**Programming languages and modules:**

[![Python](https://img.shields.io/badge/-python_3.10^-464646?logo=python)](https://www.python.org/)
[![datetime](https://img.shields.io/badge/-datetime-464646?logo=python)](https://docs.python.org/3/library/datetime.html)
[![os](https://img.shields.io/badge/-os-464646?logo=python)](https://docs.python.org/3/library/os.html)
[![random](https://img.shields.io/badge/-random-464646?logo=python)](https://docs.python.org/3/library/random.html)
[![re](https://img.shields.io/badge/-re-464646?logo=python)](https://docs.python.org/3/library/re.html)
[![sys](https://img.shields.io/badge/-sys-464646?logo=python)](https://docs.python.org/3/library/sys.html)
[![dacite](https://img.shields.io/badge/-dacite-464646?logo=python)](https://pypi.org/project/dacite/)
[![pillow](https://img.shields.io/badge/-pillow-464646?logo=python)](https://python-pillow.org/)
[![python-dotenv](https://img.shields.io/badge/-python_dotenv-464646?logo=python)](https://pypi.org/project/python-dotenv/)
[![Faker](https://img.shields.io/badge/-Faker-464646?logo=python)](https://pypi.org/project/Faker/)

**Frameworks:**

[![Django](https://img.shields.io/badge/-Django-464646?logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?logo=Django)](https://www.django-rest-framework.org/)

**Databases:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/-Redis-464646?logo=Redis)](https://redis.io/)


**Containerization:**

[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)

**Tests:**

[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Unittest](https://img.shields.io/badge/-Unittest-464646?logo=Python)](https://docs.pytest.org/en/latest/)

[⬆️Contents](#contents)

---
## Description:

You can create a job seeker or HR account in the service.

HR users can add new companies as well as new vacancies.

Job seekers can view vacancies, information about companies, respond to vacancies.
<h1></h1>

[⬆️Contents](#contents)

---

## Installation and starting:

<details><summary>Pre-conditions</summary>

It is assumed that the user has installed [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on the local machine or on the server where the project will run. You can check if they are installed using the command:

```bash
docker --version && docker-compose --version
```
</details>


Local launch:

1. Clone the repository from GitHub and enter the data for the environment variables in the [.env] file:
```bash
git clone https://github.com/Kosalexx/job_board_app.git
```
<details><summary>Local launch: Django/PostgreSQL</summary><br>

***!!! It is assumed that the user has installed [PostgreSQL](https://www.postgresql.org/) and [poetry](https://python-poetry.org/) !!!***

1.1* Create a new PostgreSQL database and pass the credentials to the [.env] file as specified in the [.env.template] file.

2. All required dependencies described in **pyproject.toml** file. To install all required libraries and packages, run the command:
```bash
poetry install
```

3. Run the migrations and launch the application:
```bash
python tree_menu/manage.py makemigrations && \
python tree_menu/manage.py migrate && \
python tree_menu/manage.py runserver
```
The project will run locally at `http://127.0.0.1:8000/`

</details>

<details><summary>Local launch: Docker Compose/PostgreSQL</summary>

2. From the root directory of the project, execute the command:
```bash
docker-compose -f docker-compose.yml up -d --build
```
The project will be hosted in two docker containers (db, app) at `http://localhost:8000/`.

3. You can stop docker and delete containers with the command from the root directory of the project:
```bash
docker-compose -f docker-compose.yml down
```
add flag -v to delete volumes ```docker-compose -f docker-compose.yml down -v```
</details><h1></h1>

[⬆️Contents](#contents)

---

## Authors:

[Aliaksei Kastsiuchonak](https://github.com/Kosalexx)

<h1></h1>

[⬆️ Back to top](#project-microblogging_app)