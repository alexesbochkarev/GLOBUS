
Системные требования
----------
* Python 3.8
* Works on Linux, Windows, macOS, BSD

Установка проекта из репозитория (Linux и macOS)
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
cd GLOBUS
```
2. Cоздать и активировать виртуальное окружение:
```bash
python3.8 -m venv venv

source venv/bin/activate
```
3. Установить зависимости из файла ```requirements.txt```:
```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

4. Выполнить миграции:
```bash

python manage.py migrate
```

5. Запустить redis-server в docker-контейнере:
```bash

docker pull redis:latest

docker run --name redis-server -p 6379:6379 -d redis:latest

```

6. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустить проект (в режиме сервера Django):
```bash
python manage.py runserver
```

8. Перейти по адресу сервера Django:
```bash
http://127.0.0.1:8000/admin/
```
