"""
Tax-related DTO models.
Based on PHP library's Model/Tax classes.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class Tax(BaseModel):
    """
    Tax information model.
    Maps to PHP Model\\Tax\\Tax.
    """
    
    # Tax model fields would be defined based on API response structure
    # Since we don't have the exact PHP model structure, we'll use flexible Dict
    data: Dict[str, Any] = Field(default_factory=dict, description="Tax data")
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Return the raw data dictionary."""
        return self.data


class History(BaseModel):
    """
    Tax history entry model.
    Maps to PHP Model\\Tax\\History.
    """
    
    # History fields would be defined based on API response
    data: Dict[str, Any] = Field(default_factory=dict, description="History entry data")
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Return the raw data dictionary."""
        return self.data


class HistoryRecords(BaseModel):
    """
    Collection of tax history records.
    Maps to PHP Model\\Tax\\HistoryRecords.
    """
    
    records: List[History] = Field(default_factory=list, description="History records")
    
    def __iter__(self):
        """Make collection iterable."""
        return iter(self.records)
    
    def __len__(self):
        """Get collection length."""
        return len(self.records)
    
    def __getitem__(self, index):
        """Get item by index."""
        return self.records[index]


class Payment(BaseModel):
    """
    Tax payment model.
    Maps to PHP Model\\Tax\\Payment.
    """
    
    # Payment fields would be defined based on API response
    data: Dict[str, Any] = Field(default_factory=dict, description="Payment data")
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Return the raw data dictionary."""
        return self.data


class PaymentRecords(BaseModel):
    """
    Collection of tax payment records.
    Maps to PHP Model\\Tax\\PaymentRecords.
    """
    
    records: List[Payment] = Field(default_factory=list, description="Payment records")
    
    def __iter__(self):
        """Make collection iterable."""
        return iter(self.records)
    
    def __len__(self):
        """Get collection length."""
        return len(self.records)
    
    def __getitem__(self, index):
        """Get item by index."""
        return self.records[index]
