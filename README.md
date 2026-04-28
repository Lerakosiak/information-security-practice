# Electronic Dean's Office API

## Опис 

REST API на базі FastAPI + SQLite. Практична робота з дисципліни "Безпека інформаційних систем".

---

## Запуск

```bash
docker compose up --build
```

Після запуску:

* API: http://localhost:3010
* Swagger: http://localhost:3010/docs

---

## Перевірка

```http
GET /health
```

Повертає стан сервера і кількість таблиць у БД.

---

## Аутентифікація

Я реалізувала реєстрацію та логін користувачів.

---

### Реєстрація

```http
POST /auth/register
```

Приклад:

```json
{
  "username": "newuser",
  "email": "new@university.edu",
  "password": "SecurePass123!",
  "full_name": "Новий Користувач"
}
```

Можливі помилки:

* 409 — якщо username або email вже існує
* 422 — якщо дані не проходять валідацію

---

### Логін

```http
POST /auth/login
```

Приклад:

```json
{
  "username": "admin",
  "password": "Admin123!@#"
}
```

Якщо все ок — повертається 200.
Якщо логін або пароль неправильні — 401.

---

## Тестові користувачі

* admin
* teacher01
* student01

(паролі не вказую)

---

## Що я зробила

* додала реєстрацію і логін
* використала bcrypt для хешування паролів
* зробила валідацію через Pydantic
* перевірила все через Swagger


