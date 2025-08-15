#!/usr/bin/env python3
"""
End-to-end async example for rurus_nalog library.

This example demonstrates a complete workflow:
1. Phone challenge authentication
2. SMS verification
3. Income receipt creation
4. Receipt JSON retrieval
5. Receipt print URL generation

Note: This example uses mocked responses for demonstration.
For real usage, replace mock responses with actual SMS codes and API responses.
"""

import asyncio
import logging
from decimal import Decimal

# Configure logging to see the library's error handling
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from rurus_nalog import Client
from rurus_nalog.dto.income import IncomeClient, IncomeServiceItem, IncomeType
from rurus_nalog.exceptions import (
    DomainException,
    PhoneException,
    UnauthorizedException,
    ValidationException,
)


async def phone_challenge_flow_example():
    """
    Example: Phone challenge authentication flow.
    """
    print("📱 Phone Challenge Authentication Flow")
    print("=" * 50)

    try:
        client = Client()

        # Step 1: Start phone challenge
        print("1️⃣ Starting phone challenge...")
        phone = "79001234567"  # Example phone number

        # In real usage, this would send an SMS
        challenge_response = await client.create_phone_challenge(phone)
        print("   ✅ Challenge started")
        print(
            f"   📧 Challenge token: {challenge_response.get('challengeToken', 'N/A')[:20]}..."
        )
        print(f"   ⏱️  Expires in: {challenge_response.get('expireIn', 'N/A')} seconds")

        # Step 2: Simulate SMS code verification
        print("\n2️⃣ Verifying SMS code...")
        # In real usage, get this from user input
        sms_code = "123456"  # Example SMS code

        token_json = await client.create_new_access_token_by_phone(
            phone, challenge_response["challengeToken"], sms_code
        )

        print("   ✅ SMS verification successful")
        print("   🔑 Access token received")

        # Step 3: Authenticate client
        await client.authenticate(token_json)
        print("   🎯 Client authenticated successfully")

        return client

    except PhoneException as e:
        print(f"   ❌ Phone verification error: {e}")
        return None
    except UnauthorizedException as e:
        print(f"   ❌ Authentication error: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return None


async def income_creation_example(client: Client):
    """
    Example: Creating income receipts.
    """
    print("\n💰 Income Receipt Creation")
    print("=" * 50)

    try:
        income_api = client.income()

        # Example 1: Simple receipt
        print("1️⃣ Creating simple receipt...")
        result = await income_api.create(
            name="Консультационные услуги", amount=Decimal("5000.00"), quantity=1
        )

        receipt_uuid = result.get("approvedReceiptUuid")
        print(f"   ✅ Receipt created: {receipt_uuid}")

        # Example 2: Multiple items receipt
        print("\n2️⃣ Creating multi-item receipt...")
        services = [
            IncomeServiceItem(
                name="Разработка веб-сайта",
                amount=Decimal("25000.00"),
                quantity=Decimal("1"),
            ),
            IncomeServiceItem(
                name="Техническая поддержка",
                amount=Decimal("3000.00"),
                quantity=Decimal("3"),  # 3 months
            ),
        ]

        result = await income_api.create_multiple_items(services)
        multi_receipt_uuid = result.get("approvedReceiptUuid")
        print(f"   ✅ Multi-item receipt created: {multi_receipt_uuid}")

        # Example 3: Receipt for legal entity
        print("\n3️⃣ Creating receipt for legal entity...")
        legal_client = IncomeClient(
            contact_phone="+79001234567",
            display_name="ООО 'Пример Технологии'",
            income_type=IncomeType.FROM_LEGAL_ENTITY,
            inn="1234567890",
        )

        result = await income_api.create(
            name="Разработка программного обеспечения",
            amount=Decimal("100000.00"),
            quantity=1,
            client=legal_client,
        )

        legal_receipt_uuid = result.get("approvedReceiptUuid")
        print(f"   ✅ Legal entity receipt: {legal_receipt_uuid}")

        return receipt_uuid, multi_receipt_uuid, legal_receipt_uuid

    except ValidationException as e:
        print(f"   ❌ Validation error: {e}")
        return None, None, None
    except Exception as e:
        print(f"   ❌ Income creation error: {e}")
        return None, None, None


async def receipt_operations_example(client: Client, receipt_uuid: str):
    """
    Example: Receipt operations.
    """
    print("\n🧾 Receipt Operations")
    print("=" * 50)

    try:
        receipt_api = client.receipt()

        # Example 1: Get receipt JSON data
        print("1️⃣ Retrieving receipt JSON...")
        receipt_data = await receipt_api.json(receipt_uuid)
        print("   ✅ Receipt data retrieved")
        print(f"   💰 Total amount: {receipt_data.get('totalAmount', 'N/A')}")
        print(f"   📅 Operation time: {receipt_data.get('operationTime', 'N/A')}")

        # Example 2: Generate print URL
        print("\n2️⃣ Generating print URL...")
        print_url = receipt_api.print_url(receipt_uuid)
        print("   ✅ Print URL generated")
        print(f"   🔗 URL: {print_url}")

        return receipt_data

    except Exception as e:
        print(f"   ❌ Receipt operations error: {e}")
        return None


async def additional_apis_example(client: Client):
    """
    Example: Additional API endpoints.
    """
    print("\n🔧 Additional API Examples")
    print("=" * 50)

    try:
        # User information
        print("1️⃣ Getting user information...")
        user_api = client.user()
        user_data = await user_api.get()
        print(f"   ✅ User: {user_data.get('displayName', 'N/A')}")
        print(f"   📋 INN: {user_data.get('inn', 'N/A')}")

        # Payment types
        print("\n2️⃣ Getting payment types...")
        payment_api = client.payment_type()
        payment_types = await payment_api.table()
        print(f"   ✅ Found {len(payment_types)} payment types")

        favorite = await payment_api.favorite()
        if favorite:
            print(f"   ⭐ Favorite: {favorite.get('bankName', 'N/A')}")

        # Tax information
        print("\n3️⃣ Getting tax information...")
        tax_api = client.tax()
        tax_data = await tax_api.get()
        print("   ✅ Tax data retrieved")

        # Tax history
        history = await tax_api.history()
        print("   📊 Tax history retrieved")

    except Exception as e:
        print(f"   ❌ Additional APIs error: {e}")


async def error_handling_example():
    """
    Example: Error handling and validation.
    """
    print("\n🚨 Error Handling Examples")
    print("=" * 50)

    client = Client()

    # Example 1: Authentication error
    print("1️⃣ Testing authentication error...")
    try:
        await client.create_new_access_token("invalid_inn", "invalid_password")
    except UnauthorizedException as e:
        print(f"   ✅ Caught authentication error: {type(e).__name__}")

    # Example 2: Validation error
    print("\n2️⃣ Testing validation error...")
    try:
        # This should fail validation
        IncomeServiceItem(name="", amount=Decimal("-100"), quantity=Decimal("0"))
    except Exception as e:
        print(f"   ✅ Caught validation error: {type(e).__name__}")

    # Example 3: Phone challenge error
    print("\n3️⃣ Testing phone challenge error...")
    try:
        await client.create_phone_challenge("invalid_phone")
    except (PhoneException, DomainException) as e:
        print(f"   ✅ Caught phone error: {type(e).__name__}")
    except Exception as e:
        print(f"   ℹ️  Mock error (expected): {type(e).__name__}")


async def token_management_example():
    """
    Example: Token storage and management.
    """
    print("\n🔐 Token Management Example")
    print("=" * 50)

    # Example with file-based token storage
    print("1️⃣ Client with file-based token storage...")
    client_with_storage = Client(storage_path="./example_token.json")
    print("   ✅ Client configured with token storage")
    print("   💾 Tokens will be saved to: ./example_token.json")

    # Example with custom device ID
    print("\n2️⃣ Client with custom device ID...")
    client_with_device = Client(device_id="my-custom-device-123")
    print("   ✅ Client configured with custom device ID")

    # Example with custom endpoint
    print("\n3️⃣ Client with custom endpoint...")
    client_custom = Client(base_url="https://custom.api.example.com/api")
    print("   ✅ Client configured with custom endpoint")


async def main():
    """
    Main async example function.
    """
    print("🎯 RuRus Nalog - Complete Async Example")
    print("🚀 Production-ready Python library for Moy Nalog API")
    print("📚 Based on PHP library: https://github.com/shoman4eg/moy-nalog")
    print("=" * 70)

    # Example 1: Phone authentication flow
    # Note: In real usage, this would work with actual API
    try:
        client = await phone_challenge_flow_example()

        if client:
            # Example 2: Income creation
            receipt_uuids = await income_creation_example(client)

            if receipt_uuids[0]:
                # Example 3: Receipt operations
                await receipt_operations_example(client, receipt_uuids[0])

                # Example 4: Additional APIs
                await additional_apis_example(client)

    except Exception as e:
        print(
            "🔄 Note: This example uses mocked data. Actual API calls would work differently."
        )
        print(f"   Error: {e}")

    # Example 5: Error handling
    await error_handling_example()

    # Example 6: Token management
    await token_management_example()

    print("\n🎉 Example completed!")
    print("📖 For more examples, see README.md")
    print("🔗 Documentation: https://github.com/your-repo/rurus-nalog")


if __name__ == "__main__":
    # Run the async example
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("💡 This is expected when running without real API credentials")
