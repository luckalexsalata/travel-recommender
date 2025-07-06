# Travel Recommender API

FastAPI сервіс для генерації туристичних рекомендацій з використанням OpenAI API.

## 🚀 Функціональність

- Генерація туристичних рекомендацій на основі текстового запиту
- Підтримка різних мов (відповідь тією ж мовою, що й запит)
- Можливість виключення конкретних місць
- Збереження історії запитів у SQLite
- Retry-логіка для OpenAI API
- Swagger UI для тестування

## 📋 Вимоги

- Python 3.8+
- OpenAI API ключ

## 🛠 Встановлення

1. **Клонуйте репозиторій:**
```bash
git clone <repository-url>
cd travel-recommender
```

2. **Перейдіть в папку backend:**
```bash
cd backend
```

3. **Створіть віртуальне середовище:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate  # Windows
```

4. **Встановіть залежності:**
```bash
pip install -r requirements.txt
```

5. **Налаштуйте змінні середовища:**
```bash
cp env_example.txt .env
```

Відредагуйте `.env` файл:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./travel_recommender.db
HOST=0.0.0.0
PORT=8000
```

## 🚀 Запуск

```bash
python3 run.py
```

Сервер запуститься на `http://localhost:8000`

## 📚 API Endpoints

### Основні ендпоінти:

- **POST** `/api/v1/recommendations/generate` - Генерація рекомендацій
- **POST** `/api/v1/recommendations/{id}/refine` - Уточнення з виключенням місць
- **GET** `/api/v1/recommendations/history` - Історія запитів
- **GET** `/api/v1/recommendations/{id}` - Отримання конкретних рекомендацій
- **GET** `/api/v1/recommendations/search/?q=query` - Пошук рекомендацій
- **DELETE** `/api/v1/recommendations/{id}` - Видалення рекомендацій

### Системні ендпоінти:

- **GET** `/` - Головна сторінка
- **GET** `/health` - Health check
- **GET** `/docs` - Swagger UI

## 📝 Приклади використання

### Генерація рекомендацій:
```bash
curl -X POST "http://localhost:8000/api/v1/recommendations/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Хочу в Рим, люблю історію та макарони",
    "num_places": 3
  }'
```

### Уточнення з виключенням місць:
```bash
curl -X POST "http://localhost:8000/api/v1/recommendations/1/refine" \
  -H "Content-Type: application/json" \
  -d '{
    "exclude": ["Колізей"]
  }'
```

### Отримання історії:
```bash
curl "http://localhost:8000/api/v1/recommendations/history"
```

## 🏗 Архітектура

```
backend/
├── app/
│   ├── core/           # Конфігурація, middleware, винятки
│   ├── api/            # API роути
│   ├── services/       # Бізнес-логіка
│   ├── models/         # Моделі БД
│   └── schemas/        # Pydantic схеми
├── tests/              # Тести
├── requirements.txt    # Залежності
└── run.py             # Точка входу
```

## 🔧 Технології

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **aiosqlite** - асинхронна SQLite
- **OpenAI** - AI генерація
- **Pydantic** - валідація даних

## 🧪 Тестування

```bash
# Запуск тестів
python -m pytest tests/

# Тестування через Swagger UI
# Відкрийте http://localhost:8000/docs
```

## 📄 Ліцензія

MIT 