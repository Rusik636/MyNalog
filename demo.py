#!/usr/bin/env python3
"""
Демонстрация работы rurus_nalog - асинхронной Python библиотеки для API "Мой налог".

Этот скрипт показывает основные возможности библиотеки:
- Аутентификация
- Создание чеков
- Получение информации о чеках
- Отмена чеков
"""

import asyncio
import json
from decimal import Decimal

from rurus_nalog import Client
from rurus_nalog.dto.income import (
    IncomeClient,
    IncomeServiceItem,
    IncomeType,
)
from rurus_nalog.exceptions import ValidationException


async def demo_authentication():
    """Демонстрация аутентификации."""

    client = Client()

    # В реальном коде используйте настоящие учетные данные
    fake_token = {
        "token": "demo_access_token",
        "refreshToken": "demo_refresh_token",
        "profile": {
            "inn": "123456789012",
            "displayName": "Demo User",
            "email": "demo@example.com",
        },
    }

    await client.authenticate(json.dumps(fake_token))

    return client


async def demo_income_creation(client: Client):
    """Демонстрация создания чеков."""

    # Вместо реальных HTTP запросов покажем структуру данных
    try:
        # Создаем объекты для демонстрации валидации
        IncomeServiceItem(
            name="Консультационные услуги",
            amount=Decimal("5000.00"),
            quantity=Decimal("1"),
        )
    except ValidationException:
        pass

    services = [
        IncomeServiceItem(
            name="Разработка сайта", amount=Decimal("25000.00"), quantity=Decimal("1")
        ),
        IncomeServiceItem(
            name="Техподдержка", amount=Decimal("5000.00"), quantity=Decimal("3")
        ),
    ]

    sum(item.get_total_amount() for item in services)

    IncomeClient(
        display_name="ООО 'Демо Компания'",
        income_type=IncomeType.FROM_LEGAL_ENTITY,
        inn="1234567890",
        contact_phone="+79001234567",
    )


async def demo_receipt_operations(client: Client):
    """Демонстрация операций с чеками."""

    demo_receipt_uuid = "demo-receipt-uuid-123"

    # Получение URL для печати
    receipt_api = client.receipt()
    receipt_api.print_url(demo_receipt_uuid)

    # Структура отмены чека


async def demo_error_handling():
    """Демонстрация обработки ошибок."""

    # Валидация неверных данных

    try:
        # Пустое название услуги
        IncomeServiceItem(name="", amount=Decimal("100"), quantity=Decimal("1"))
    except ValueError:
        pass

    try:
        # Отрицательная сумма
        IncomeServiceItem(name="Услуга", amount=Decimal("-100"), quantity=Decimal("1"))
    except Exception:
        pass

    try:
        # Нулевое количество
        IncomeServiceItem(name="Услуга", amount=Decimal("100"), quantity=Decimal("0"))
    except Exception:
        pass

    try:
        # Неверный ИНН
        IncomeClient(inn="123")  # Слишком короткий
    except Exception:
        pass


async def demo_data_serialization():
    """Демонстрация сериализации данных."""

    # Сериализация IncomeServiceItem
    item = IncomeServiceItem(
        name="Демо услуга", amount=Decimal("1500.50"), quantity=Decimal("2")
    )

    item.model_dump()

    # Сериализация IncomeClient
    client_data = IncomeClient(
        contact_phone="+79001234567",
        display_name="Демо Клиент",
        income_type=IncomeType.FROM_INDIVIDUAL,
        inn="123456789012",
    )

    client_data.model_dump()


async def main():
    """Главная функция демонстрации."""

    # Демонстрация аутентификации
    client = await demo_authentication()

    # Демонстрация создания чеков
    await demo_income_creation(client)

    # Демонстрация операций с чеками
    await demo_receipt_operations(client)

    # Демонстрация обработки ошибок
    await demo_error_handling()

    # Демонстрация сериализации
    await demo_data_serialization()


if __name__ == "__main__":
    asyncio.run(main())
