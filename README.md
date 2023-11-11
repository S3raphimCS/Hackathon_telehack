# Hackathon_telehack  
## Репозиторий команды ХристOS  
  
Участники команды:  
1) Задонский Сергей  
2) Медведев Андрей  
3) Лосев Никита  
4) Ликоренко Артем  
5) Малаховский Даниил  
  
## Тема:  
Разработка специального программного обеспечения конвертации результатов измерений радиоконтрольного оборудования тестирования (мониторинга) параметров услуг подвижной радиотелефонной связи.  
  
## Стек используемых технологий:  
- Python  
- Django (REST)  
- JavaScript  
- React  
- PostgreSQL  
- Docker

## Инструкция по развертыванию 
Перед работой требуется создать сам .env файл и внести изменения для продукта (Linux/Windows):
>```cp .env.tpl .env```
> ```copy .env.tpl```

Для запуска контейнеров требуется прописать в терминале команду, приведённую ниже, обязательно требуется находиться в корневом каталоге. t
> docker-compose build\
> docker-compose up\
> docker exec -it django_web sh -c "python manage.py makemigrations"\
> docker exec -it django_web sh -c "python manage.py migrate"\
> docker restart django_web\

Для выключения контейнеров:
> docker-compose down

Каждый контейнер записывает логи в формате JSON-файла
> docker info --format '{{.LoggingDriver}}'\
Вывод: json-file

По каждому контейнеру можно просмотреть лог, пример:
> docker logs nginx

Приложение автоматически работает на соответсвующих портах:
> Django REST Framework - Домен:8000\
React application -  Домен:3000