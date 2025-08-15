"""Data Transfer Objects for Moy Nalog API."""

from .income import (
    IncomeType,
    PaymentType,
    CancelCommentType,
    IncomeServiceItem,
    IncomeClient,
    AtomDateTime,
    IncomeRequest,
    CancelRequest,
)
from .payment_type import PaymentType as PaymentTypeModel, PaymentTypeCollection
from .user import UserType
from .tax import Tax, History, HistoryRecords, Payment, PaymentRecords
from .invoice import InvoiceServiceItem, InvoiceClient
from .device import DeviceInfo

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
