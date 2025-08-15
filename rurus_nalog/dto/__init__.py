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
    "AtomDateTime",
    "CancelCommentType",
    "CancelRequest",
    # Device DTOs
    "DeviceInfo",
    "History",
    "HistoryRecords",
    "IncomeClient",
    "IncomeRequest",
    "IncomeServiceItem",
    # Income DTOs
    "IncomeType",
    "InvoiceClient",
    # Invoice DTOs
    "InvoiceServiceItem",
    "Payment",
    "PaymentRecords",
    "PaymentType",
    "PaymentTypeCollection",
    # Payment Type DTOs
    "PaymentTypeModel",
    # Tax DTOs
    "Tax",
    # User DTOs
    "UserType",
]
