# RuRus Nalog - Async Python Client

> 🇷🇺 Асинхронный Python клиент для API сервиса "Мой налог" (lknpd.nalog.ru) для самозанятых

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Async](https://img.shields.io/badge/async-httpx-green.svg)](https://www.python-httpx.org/)

**Русская асинхронная библиотека** для взаимодействия с API налогового сервиса для самозанятых. Портирована с PHP-библиотеки [shoman4eg/moy-nalog](https://github.com/shoman4eg/moy-nalog).

## 🚀 Особенности

- ✅ **Полностью асинхронная** - построена на httpx AsyncClient
- ✅ **Типизированная** - Pydantic v2 модели и mypy support  
- ✅ **Автоматическое обновление токенов** - middleware для 401 ответов
- ✅ **Валидация данных** - строгая проверка ИНН, сумм, дат
- ✅ **Точная арифметика** - Decimal для денежных операций
- ✅ **Покрытие тестами 88%** - pytest + respx моки

## 📦 Установка

```bash
pip install httpx pydantic python-dotenv
# Скопируйте код библиотеки в свой проект
```

## 🔧 Быстрый старт

### Аутентификация по ИНН и паролю

```python
import asyncio
from rurus_nalog import Client

async def main():
    client = Client()
    
    # Получить токен доступа
    token = await client.create_new_access_token("ваш_инн", "ваш_пароль")
    
    # Аутентифицироваться
    await client.authenticate(token)
    
    print("✅ Успешная аутентификация!")

asyncio.run(main())
```

### Аутентификация по номеру телефона

```python
import asyncio
from rurus_nalog import Client

async def main():
    client = Client()
    
    # Шаг 1: Запросить SMS код
    challenge = await client.create_phone_challenge("79001234567")
    print(f"SMS отправлена. Токен: {challenge['challengeToken']}")
    
    # Шаг 2: Ввести код из SMS
    sms_code = input("Введите код из SMS: ")
    token = await client.create_new_access_token_by_phone(
        "79001234567", 
        challenge['challengeToken'], 
        sms_code
    )
    
    # Аутентифицироваться
    await client.authenticate(token)
    print("✅ Успешная аутентификация по телефону!")

asyncio.run(main())
```

## 💼 Создание чеков

### Простой чек

```python
import asyncio
from decimal import Decimal
from rurus_nalog import Client

async def main():
    client = Client()
    await client.authenticate("ваш_токен_json")
    
    # Создать чек
    income_api = client.income()
    result = await income_api.create(
        name="Консультационные услуги",
        amount=Decimal("5000.00"),
        quantity=1
    )
    
    receipt_uuid = result["approvedReceiptUuid"]
    print(f"✅ Чек создан: {receipt_uuid}")
    
    # Получить ссылку на печать чека
    receipt_api = client.receipt()
    print_url = receipt_api.print_url(receipt_uuid)
    print(f"🖨️  Ссылка для печати: {print_url}")

asyncio.run(main())
```

### Чек с несколькими позициями

```python
import asyncio
from decimal import Decimal
from rurus_nalog import Client
from rurus_nalog.dto.income import IncomeServiceItem

async def main():
    client = Client()
    await client.authenticate("ваш_токен_json")
    
    # Создать позиции
    services = [
        IncomeServiceItem(
            name="Разработка сайта", 
            amount=Decimal("25000.00"), 
            quantity=Decimal("1")
        ),
        IncomeServiceItem(
            name="Техподдержка", 
            amount=Decimal("5000.00"), 
            quantity=Decimal("3")  # 3 месяца
        ),
    ]
    
    # Создать чек
    income_api = client.income()
    result = await income_api.create_multiple_items(services)
    
    print(f"✅ Чек на сумму {25000 + 5000*3} руб создан!")
    print(f"UUID: {result['approvedReceiptUuid']}")

asyncio.run(main())
```

### Чек для юридического лица

```python
import asyncio
from decimal import Decimal
from rurus_nalog import Client
from rurus_nalog.dto.income import IncomeClient, IncomeType

async def main():
    client = Client()
    await client.authenticate("ваш_токен_json")
    
    # Клиент - юридическое лицо
    legal_client = IncomeClient(
        display_name="ООО 'Пример'",
        income_type=IncomeType.FROM_LEGAL_ENTITY,
        inn="1234567890",  # ИНН юр.лица (10 цифр)
        contact_phone="+79001234567"
    )
    
    # Создать чек
    income_api = client.income()
    result = await income_api.create(
        name="Разработка ПО",
        amount=Decimal("100000.00"),
        quantity=1,
        client=legal_client
    )
    
    print(f"✅ Чек для {legal_client.display_name} создан!")

asyncio.run(main())
```

## ❌ Отмена чеков

```python
import asyncio
from rurus_nalog import Client
from rurus_nalog.dto.income import CancelCommentType

async def main():
    client = Client()
    await client.authenticate("ваш_токен_json")
    
    income_api = client.income()
    
    # Отменить чек (ошибочно сформирован)
    result = await income_api.cancel(
        receipt_uuid="uuid_чека_для_отмены",
        comment=CancelCommentType.CANCEL
    )
    
    print("✅ Чек отменён!")
    
    # Или возврат средств
    result = await income_api.cancel(
        receipt_uuid="uuid_чека_для_возврата", 
        comment=CancelCommentType.REFUND
    )
    
    print("✅ Возврат оформлен!")

asyncio.run(main())
```

## 📄 Получение данных чека

```python
import asyncio
from rurus_nalog import Client

async def main():
    client = Client()
    await client.authenticate("ваш_токен_json")
    
    receipt_api = client.receipt()
    receipt_uuid = "ваш_uuid_чека"
    
    # Получить JSON данные чека
    receipt_data = await receipt_api.json(receipt_uuid)
    print("📄 Данные чека:", receipt_data)
    
    # Получить ссылку для печати
    print_url = receipt_api.print_url(receipt_uuid)
    print("🖨️  Ссылка для печати:", print_url)

asyncio.run(main())
```

## 🔒 Хранение токенов

```python
import asyncio
from rurus_nalog import Client

async def main():
    # Автоматическое сохранение токена в файл
    client = Client(storage_path="./token.json")
    
    # При первом использовании
    token = await client.create_new_access_token("инн", "пароль")
    await client.authenticate(token)  # Токен сохранится в ./token.json
    
    # При повторном использовании токен загрузится автоматически
    client2 = Client(storage_path="./token.json")
    # Токен уже загружен из файла, можно сразу использовать API
    
asyncio.run(main())
```

## ⚙️ Настройки

```python
from rurus_nalog import Client

# Кастомные настройки
client = Client(
    base_url="https://lknpd.nalog.ru/api",  # По умолчанию
    storage_path="./my_token.json",         # Файл для токена
    device_id="my-device-123",              # Кастомный device ID  
    timeout=15.0                            # Таймаут запросов (сек)
)
```

## 🚨 Обработка ошибок

```python
import asyncio
from rurus_nalog import Client
from rurus_nalog.exceptions import (
    UnauthorizedException,
    ValidationException, 
    PhoneException,
    DomainException
)

async def main():
    client = Client()
    
    try:
        # Неверные учетные данные
        await client.create_new_access_token("неверный_инн", "неверный_пароль")
    except UnauthorizedException as e:
        print(f"❌ Ошибка аутентификации: {e}")
    
    try:
        # Неверные данные чека
        income_api = client.income()
        await income_api.create("", -100, 0)  # Пустое имя, отрицательная сумма
    except ValidationException as e:
        print(f"❌ Ошибка валидации: {e}")
    except ValueError as e:
        print(f"❌ Ошибка данных: {e}")
    
    try:
        # Проблемы с SMS
        await client.create_phone_challenge("неверный_номер")
    except PhoneException as e:
        print(f"❌ Ошибка SMS: {e}")
    
    except DomainException as e:
        print(f"❌ Общая ошибка API: {e}")

asyncio.run(main())
```

## 🧪 Тестирование

```bash
# Установить dev зависимости
pip install pytest pytest-asyncio respx

# Запустить тесты
pytest tests/ -v

# Проверить покрытие
pip install coverage
coverage run -m pytest tests/
coverage report --include="rurus_nalog/*"
```

## 📋 API Reference

### Client

- `create_new_access_token(username, password)` - аутентификация по ИНН/паролю
- `create_phone_challenge(phone)` - запрос SMS кода  
- `create_new_access_token_by_phone(phone, token, code)` - аутентификация по SMS
- `authenticate(token_json)` - установка токена
- `income()` - получить Income API
- `receipt()` - получить Receipt API

### Income API

- `create(name, amount, quantity, operation_time=None, client=None)` - создать чек
- `create_multiple_items(services, operation_time=None, client=None)` - чек с несколькими позициями  
- `cancel(receipt_uuid, comment, operation_time=None, ...)` - отменить чек

### Receipt API  

- `print_url(receipt_uuid)` - ссылка для печати чека
- `json(receipt_uuid)` - данные чека в JSON

## 🔄 Миграция с PHP библиотеки

Эта библиотека полностью совместима по API с [shoman4eg/moy-nalog](https://github.com/shoman4eg/moy-nalog):

| PHP | Python |
|-----|--------|
| `ApiClient::create()` | `Client()` |
| `$client->createNewAccessToken()` | `await client.create_new_access_token()` |
| `$client->income()->create()` | `await client.income().create()` |
| `$client->receipt()->printUrl()` | `client.receipt().print_url()` |

## 📚 Дополнительная информация

- **Оригинальная PHP библиотека**: [shoman4eg/moy-nalog](https://github.com/shoman4eg/moy-nalog)
- **Официальный сервис**: [lknpd.nalog.ru](https://lknpd.nalog.ru/)
- **Документация API**: см. исходную PHP библиотеку

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функциональности
3. Добавьте тесты для своих изменений  
4. Убедитесь, что все тесты проходят
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

> ⚠️ **Внимание**: Эта библиотека является неофициальной и не связана с ФНС России. Используйте на свой страх и риск.
> 
> 🔗 **Базовая PHP версия**: Все идеи и архитектурные решения основаны на работе [Artem Dubinin](https://github.com/shoman4eg)
