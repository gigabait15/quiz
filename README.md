# CyberForm Quiz System

Проект представляет собой онлайн-систему тестирования, разработанную с использованием Django и Django REST Framework. Пользователи могут проходить тесты, загруженные из CSV, а система сохраняет их ответы и подсчитывает результат.

## 📦 Возможности

- Импорт тестов из CSV-файла
- Прохождение тестов пользователями
- Сохранение и отображение ответов
- Подсчет и отображение итогов тестирования
- Swagger UI для документации API
- Поддержка Docker-контейнеризации

---

## ⚙️ Установка (локально)

1. **Клонируйте репозиторий и перейдите в каталог проекта:**
   ```bash
   git clone https://github.com/gigabait15/quiz.git
   cd QuizDRF
   ```

2. **Создайте виртуальное окружение и установите зависимости:**
    ```bash 
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Примените миграции:**
    ```bash 
    python manage.py migrate
   ```
   
4. **Импортируйте тесты из CSV:**
    ```bash
   python manage.py import_tests test_data.csv
    ```
   
5. **Создайте суперпользователя (по желанию):**
    ```bash
   python manage.py createsuperuser
    ```

6. **Запустите сервер:**
    ```bash
   python manage.py runserver
    ```
   
## Запуск через Docker
1. **Сборка и запуск контейнера**
   ```bash
   docker-compose up --build -d
   ```
   
2. **Настройка переменных окружения в контейнере**
   ```bash
   echo "DB_NAME=quizdb
   DB_USER=quizuser
   DB_PASSWORD=quizpass
   DB_HOST=db
   DB_PORT=5432" > .env
   ```
   **После запуска контейнера применить миграции и создать пользователя**
   ```
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```
   

---

## 🔌 API Эндпоинты

| Метод | URL                              | Описание                                                | Авторизация |
|-------|----------------------------------|----------------------------------------------------------|--------------|
| GET   | `/api/tests/<id>/questions/`     | Получить список вопросов конкретного теста с пагинацией | ❌ Нет       |
| GET   | `/api/tests/<id>/with-answers/`  | Получить тест с ответами текущего пользователя          | ✅ Да        |
| POST  | `/api/answers/`                  | Сохранить или обновить ответ пользователя               | ✅ Да        |
| POST  | `/api/tests/<id>/submit/`        | Завершить тест и получить количество правильных ответов | ✅ Да        |

---

### 🧪 Swagger UI

Документация API доступна по адресу:
-  /swagger/

--- 
### Тестирование
Для запуска тестов выполнить 
```bash
  ./manage.py test quiz
   ```
