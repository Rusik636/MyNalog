"""Data Transfer Objects for Moy Nalog API."""

from .device import DeviceInfo
from .income import (
    AtomDateTime,
    CancelCommentType,
    CancelRequest,
    IncomeClient,
    IncomeRequest,
    IncomeServiceItem,
    IncomeType,
    PaymentType,
)
from .invoice import InvoiceClient, InvoiceServiceItem
from .payment_type import PaymentType as PaymentTypeModel
from .payment_type import PaymentTypeCollection
from .tax import History, HistoryRecords, Payment, PaymentRecords, Tax
from .user import UserType

__all__ = [
    # Income DTOs
    "IncomeType",
    "PaymentType",
    "CancelCommentType",
    "IncomeServiceItem",
    "IncomeClient",
    "AtomDateTime",
    "IncomeRequest",
    "CancelRequest",
    # Payment Type DTOs
    "PaymentTypeModel",
    "PaymentTypeCollection",
    # User DTOs
    "UserType",
    # Tax DTOs
    "Tax",
    "History",
    "HistoryRecords",
    "Payment",
    "PaymentRecords",
    # Invoice DTOs
    "InvoiceServiceItem",
    "InvoiceClient",
    # Device DTOs
    "DeviceInfo",
]
