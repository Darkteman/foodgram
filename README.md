![Foodgram](https://github.com/Darkteman/foodgram/actions/workflows/main.yml/badge.svg)
# Проект «Продуктовый помощник» - Foodgram
Foodgram - Продуктовый помощник. Сервис позволяет публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологический стек
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

## Адреса проекта на удаленном сервере:
#### http://51.250.66.232/

## В ходе работы над проектом сделано:
* Настроено взаимодействие Python-приложения с внешними API-сервисами
* Создан собственный API-сервис на базе проекта Django
* Создан Telegram-бот
* Подключено SPA к бэкенду на Django через API
* Созданы образы и запущены контейнеры Docker
* Созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения

## Запуск проекта в Docker контейнере
Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адрес проекта в файле `nginx.conf`
* Склонируйте репозиторий:
```bash
git clone https://github.com/Darkteman/foodgram.git
```
* Создайте .env файл в директории infra/ (пример заполнения):
```bash
SECRET_KEY=<секретный ключ django>
DEBUG='False'
ALLOWED_HOSTS='*'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
```  
* Запустите docker compose:
```bash
docker-compose up -d
```  
* Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
* Загрузите ингредиенты и теги:
```bash
docker-compose exec backend python manage.py import_ingredients
docker-compose exec backend python manage.py import_tags
```
* Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

### Пользовательские роли в проекте
1. Анонимный пользователь
2. Аутентифицированный пользователь
3. Администратор

### Анонимные пользователи могут:
1. Просматривать список рецептов
2. Просматривать отдельные рецепты
3. Фильтровать рецепты по тегам
4. Создавать аккаунт

### Аутентифицированные пользователи могут:
1. Получать данные о своей учетной записи
2. Изменять свой пароль
3. Просматривать, публиковать, удалять и редактировать свои рецепты
4. Добавлять понравившиеся рецепты в избранное и удалять из избранного
5. Добавлять рецепты в список покупок и удалять из списка
6. Подписываться и отписываться на авторов
7. Скачать список покупок

#### Набор доступных эндпоинтов:
- ```api/docs/redoc``` - Подробная документация по работе API
- ```api/tags/``` - Получение, списка тегов (GET)
- ```api/tags/{id}``` - Получение, тега с соответствующим id (GET)
- ```api/ingredients/``` - Получение, списка ингредиентов (GET)
- ```api/ingredients/``` - Получение ингредиента с соответствующим id (GET)
- ```api/recipes/``` - Получение списка с рецептами и публикация рецептов (GET, POST)
- ```api/recipes/{id}``` - Получение, изменение, удаление рецепта с соответствующим id (GET, PATCH, DELETE)
- ```api/recipes/{id}/shopping_cart/``` - Добавление рецепта с соответствующим id в список покупок и удаление из списка (GET, DELETE)
- ```api/recipes/download_shopping_cart/``` - Скачать файл со списком покупок .txt (GET)
- ```api/recipes/{id}/favorite/``` - Добавление рецепта с соответствующим id в список избранного и его удаление (GET, DELETE)

#### Операции с пользователями:
- ```api/users/``` - получение информации о пользователе и регистрация новых пользователей (GET, POST)
- ```api/users/{id}/``` - Получение информации о конкертном пользователе по id (GET)
- ```api/users/me/``` - получение данных своей учётной записи. Доступна только авторизованному пользователю (GET)
- ```api/users/set_password/``` - изменение собственного пароля (PATCH)
- ```api/users/{id}/subscribe/``` - Подписаться на пользователя с соответствующим id или отписаться от него (GET, DELETE)
- ```api/users/subscribe/subscriptions/``` - Просмотр пользователей на которых подписан текущий пользователь (GET)

#### Аутентификация и создание новых пользователей:
- ```api/auth/token/login/``` - Получение токена (POST)
- ```api/auth/token/logout/``` - Удаление токена (POST)

## Авторы
[Пищулин А.А.](https://github.com/darkteman) - Бэкенд и деплой для сервиса Foodgram

[Яндекс.Практикум](https://github.com/yandex-praktikum) - Фронтенд для сервиса Foodgram
