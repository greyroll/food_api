Food API

Требования

- Python 3.12
- Установленные зависимости из файла requirements.txt


Клонируйте репозиторий
Установите зависимости:
pip install -r requirements.txt

Конфигурация

Проект использует переменные окружения для хранения конфиденциальных данных, таких как токен доступа.

Создайте файл .env в корне проекта и добавьте в него следующие строки:
ACCESS_TOKEN_SECRET=your_secret_token_here


Запустите приложение с помощью Uvicorn:

uvicorn main:app --reload
После этого приложение будет доступно по адресу http://127.0.0.1:8000.

Использование

Для авторизации перейдите на эндпоинт /login и введите данные в форму.
Эндпоинт /validate_login обрабатывает форму и устанавливает cookie access_token.
Остальные эндпоинты требуют наличия корректного токена.

Дополнительная информация

Проект использует FastAPI для разработки API.
Шаблоны HTML находятся в папке templates.
Access token хранится в HTTP-only cookie и значение задается через переменную окружения ACCESS_TOKEN_SECRET.
