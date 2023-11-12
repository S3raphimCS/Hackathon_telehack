# [Hackathon_telehack](https://telehack.ru/services/)  
## Репозиторий команды <u>ХристOS</u>

## Тема:  
Разработка специального программного обеспечения конвертации результатов измерений радиоконтрольного оборудования тестирования (мониторинга) параметров услуг подвижной радиотелефонной связи.

## Участники команды:
1) <a href="https://github.com/S3raphimCS">Задонский Сергей</a> (<i>Капитан</i>)<br>
2) <a href="https://github.com/Merkucios">Медведев Андрей</a><br>
3) <a href="https://github.com/QuiO-D">Лосев Никита</a><br>
4) <a href="https://github.com/ruPaTRiK">Ликоренко Артем</a><br> 
5) <a href="https://github.com/AFKMDaniel">Малаховский Даниил</a><br> 
  

## Стек используемых технологий:  
- Python ![Static Badge](https://img.shields.io/badge/Python-3.10.4-yellow?logo=python)
- Django (REST) ![Static Badge](https://img.shields.io/badge/Django-4.2.2-green?logo=Django) ![Static Badge](https://img.shields.io/badge/DRF-3.14.0-red?logo=djangorestframework)
- Typescript ![Static Badge](https://img.shields.io/badge/Typescript-5-blue?logo=typescript)
- Nextjs ![Static Badge](https://img.shields.io/badge/Nextjs-14.0.2-black?logo=next.js)
- React  ![Static Badge](https://img.shields.io/badge/React-18-blue?logo=React)
- PostgreSQL ![Static Badge](https://img.shields.io/badge/Postgres-16.0-lightgrey?logo=postgresql)
- Docker ![Static Badge](https://img.shields.io/badge/Docker-3.8-blue?logo=docker)

## Инфраструктура приложения:
<center><img src="readme_src/infra.jpg" width="95%"></center>

## Инструкция по развертыванию 
Перед работой требуется создать сам .env файл и внести изменения для продукта:
>**Linux**: cp .env.tpl .env

>**Windows**: copy .env.tpl .env

Для запуска контейнеров требуется прописать в терминале команду, приведённую ниже, обязательно требуется находиться в корневом каталоге. В проекте существует две вариации работы с докером, это dev и prod версии. Приведём пример на dev версии.
> docker-compose -f docker-compose.dev.yml build\
> docker-compose -f docker-compose.dev.yml up

Для развёртывания приложения требуется передать в параметр -f docker-compose-prod.yml. Prod версия содержит в себе сервисы Certbot и Nginx.

Для выключения контейнеров:
> docker-compose -f docker-compose.dev.yml down

Каждый контейнер записывает логи в формате JSON-файла
> docker info --format '{{.LoggingDriver}}'\
Вывод: json-file

По каждому контейнеру можно просмотреть лог, пример:
> docker logs pgdb

Приложение автоматически работает на соответсвующих портах:
> **Django REST Framework** - Домен:8000\
**React application** -  Домен:3000\
**PostgreSQL** - КластерСУБД:5432

[В начало](#hackathontelehack-)