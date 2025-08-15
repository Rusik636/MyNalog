# 📁 Структура проекта RuRus Nalog

## 🏗️ Основные файлы

### 📋 Конфигурация проекта
- **`pyproject.toml`** - Конфигурация Python проекта, зависимости, инструменты разработки
- **`README.md`** - Документация с примерами использования (383 строки)
- **`MIGRATION_REPORT.md`** - Подробный отчёт о миграции PHP → Python

### 🎯 Демонстрация
- **`demo.py`** - Рабочие примеры всех возможностей библиотеки

### 🚀 CI/CD
- **`.github/workflows/ci.yml`** - GitHub Actions для тестирования, линтинга и проверки безопасности

## 📦 Основная библиотека (`rurus_nalog/`)

### 🔧 Ядро системы
- **`__init__.py`** - Публичный API, экспорт классов и исключений
- **`client.py`** - Главный фасад Client с фабричными методами (203 строки)
- **`_http.py`** - Асинхронный HTTP клиент с middleware аутентификации (170 строк)
- **`auth.py`** - Провайдер аутентификации AuthProviderImpl (277 строк)

### 📊 API модули
- **`income.py`** - Income API для создания и отмены чеков (150 строк)
- **`receipt.py`** - Receipt API для получения данных чеков (74 строки)
- **`exceptions.py`** - Иерархия исключений и маппинг HTTP кодов (95 строк)

### 📋 DTO модели (`dto/`)
- **`__init__.py`** - Экспорт DTO классов
- **`income.py`** - Pydantic модели для Income API (242 строки)
  - `IncomeServiceItem` - позиция чека
  - `IncomeClient` - информация о клиенте
  - `IncomeRequest` / `CancelRequest` - запросы к API
  - `AtomDateTime` - сериализация дат в ISO формат
  - Enums: `IncomeType`, `PaymentType`, `CancelCommentType`

## 🧪 Тесты (`tests/`)

### 📝 Тестовые файлы (46 тестов total)
- **`__init__.py`** - Инициализация пакета тестов
- **`test_auth_async.py`** - Тесты аутентификации (14 тестов, 293 строки)
  - AuthProviderImpl: создание токенов, phone challenge, refresh
  - Client: публичные методы аутентификации
  - RefreshMiddleware: автоматическое обновление токенов при 401
- **`test_income_async.py`** - Тесты Income API (22 теста, 395 строк)
  - Создание чеков (single/multiple items)
  - Валидация клиентов (физ/юр лица)
  - Отмена чеков
  - DTO валидация и сериализация
- **`test_receipt_async.py`** - Тесты Receipt API (10 тестов, 185 строк)
  - Генерация URL для печати
  - Получение JSON данных чека
  - Валидация параметров

## 📊 Статистика по файлам

### 🎯 Основные модули (покрытие тестами)
```
rurus_nalog/_http.py      63 строки   90% покрытие
rurus_nalog/auth.py       88 строк    80% покрытие
rurus_nalog/client.py     38 строк    89% покрытие
rurus_nalog/income.py     39 строк   100% покрытие ✅
rurus_nalog/receipt.py    18 строк   100% покрытие ✅
rurus_nalog/exceptions.py 38 строк    68% покрытие
rurus_nalog/dto/income.py 111 строк   92% покрытие
```

### 📋 Общая статистика
- **Всего строк кода:** 397 (основная библиотека)
- **Тестовых строк:** 873 (в 3 файлах)
- **Документации:** 466 строк (README + отчёты)
- **Общее покрытие:** 88%

## 🔧 Технологический стек

### 🐍 Python зависимости
```toml
# Основные
httpx>=0.25.0        # Async HTTP client
pydantic>=2.0.0      # DTO validation
python-dotenv>=1.0.0 # Config management

# Разработка  
pytest>=7.0.0        # Testing framework
pytest-asyncio>=0.21.0 # Async test support
respx>=0.20.0        # HTTP mocking
ruff>=0.1.0          # Linting
black>=23.0.0        # Code formatting
mypy>=1.0.0          # Type checking
coverage>=7.0.0      # Test coverage
```

### 🏗️ Архитектурные принципы
- **Асинхронность:** httpx.AsyncClient + asyncio
- **Типизация:** Pydantic v2 + mypy
- **Модульность:** четкое разделение ответственности
- **Тестируемость:** 88% покрытие с async тестами
- **Совместимость:** 100% API соответствие с PHP версией

## 📚 Дополнительные файлы

### 🗂️ Служебные директории
- **`.pytest_cache/`** - Кэш pytest
- **`rurus_nalog.egg-info/`** - Метаданные установленного пакета
- **`__pycache__/`** - Скомпилированные Python файлы
- **`.coverage`** - Данные покрытия тестами

### 🔍 Исходный PHP проект (`PHPLibMoyNalog/`)
- Оригинальная PHP библиотека для анализа и портирования
- Используется как reference implementation
- Содержит тесты, документацию и примеры

## 🎯 Использование

### 🚀 Быстрый старт
```python
from rurus_nalog import Client

client = Client()
token = await client.create_new_access_token("inn", "password")
await client.authenticate(token)

# Создать чек
income_api = client.income()  
result = await income_api.create("Услуга", 1000, 1)

# Получить данные чека
receipt_api = client.receipt()
receipt_data = await receipt_api.json(result["approvedReceiptUuid"])
```

### 🧪 Запуск тестов
```bash
pytest tests/ -v                    # Все тесты
python -m coverage run -m pytest    # С покрытием
python demo.py                      # Демонстрация
```

---

**Итого:** Полнофункциональная асинхронная Python библиотека с 88% покрытием тестами, готовая к использованию в продакшене.
