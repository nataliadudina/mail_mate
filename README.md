# Mail Mate

Mail Mate - это сервис управления рассылками, который позволяет администраторам создавать, редактировать и удалять рассылки, а также получать статистику по ним. Пользователи могут регистрироваться по электронной почте, редактировать свой профиль и формировать и запускать свои рассылки немедленно или по расписанию.

## Установка и настройка

1. Клонируйте репозиторий: `git clone https://github.com/nataliadudina/mail_mate`
2. Перейдите в директорию проекта: `cd mailmate`
3. Создайте виртуальное окружение: `python3 -m venv env`
4. Активируйте виртуальное окружение: `source env/bin/activate` (Linux/Mac) или `.\env\Scripts\activate` (Windows)
5. Установите зависимости: `pip install -r requirements.txt`
6. Создайте файл .env с необходимыми переменными окружения (пример в разделе ниже).
7. Примените миграции: `python manage.py migrate`
8. Запустите сервер: `python manage.py runserver`

Пример содержимого файла .env:
```
SECRET_KEY=

ALLOWED_HOSTS = 127.0.0.1, localhost,

POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_PORT=1111
POSTGRES_DB=postgres

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_SSL = True

CACHE_ENABLED = True
CACHE_LOCATION = redis://127.0.0.1:6379

```

## Структура проекта

```
mailmate/
├── main/
├── blog/
├── users/
├── manage.py
├── requirements.txt
└── .env
```

## Приложения

Проект состоит из трех приложений:

1. **Main App**: 
Главная страница с общей статистикой, окном для регистрации и 3 случайными статьями из блога;
 
Функционал для создания, редактирования, удаления шаблонов, клиентов, рассылок; 

Планировщик запуска рассылок.
Запуск рассылки возможен немедленно или по расписанию. Планировщик запускается через интерфейс приложения или по команде в консоли.
Можно запланировать разовую рассылку или настроить периодичность запуска (раз в день, раз в неделю, раз в месяц).

3. **Blog App**: Список статей, например, по теме маркетинга и бизнеса. Все пользователи могут просматривать статьи. Только контент-менеджер их создаёт, редактирует и удаляет, публикует или нет.

4. **Users App**: Приложение для работы с пользователями. Регистрация возможна по паролю и email, авторизация - по usernane/email и паролю.
Требуется верификация по почте.
Пользователям доступно редактирование своего профиля, смена и восстановление пароля. Каждый пользователь имеет доступ только к своим шаблонам, клиентам и рассылкам.
Контент-менеджер, как и главный админ (superuser) имеет доступ к админке, а также к странице со списком пользователей, где может их блокировать.
