"""
User-related DTO models.
Based on PHP library's Model/User classes.
"""

from datetime import datetime
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field, field_validator


class UserType(BaseModel):
    """
    User profile model.
    Maps to PHP Model\\User\\UserType.
    """
    
    id: int = Field(..., description="User ID")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")
    display_name: str = Field(..., alias="displayName", description="Display name")
    middle_name: Optional[str] = Field(None, alias="middleName", description="Middle name")
    email: Optional[str] = Field(None, description="Email address")
    phone: str = Field(..., description="Phone number")
    inn: str = Field(..., description="INN (tax identification number)")
    snils: Optional[str] = Field(None, description="SNILS")
    avatar_exists: bool = Field(..., alias="avatarExists", description="Avatar exists")
    initial_registration_date: Optional[datetime] = Field(
        None, 
        alias="initialRegistrationDate", 
        description="Initial registration date"
    )
    registration_date: Optional[datetime] = Field(
        None, 
        alias="registrationDate", 
        description="Registration date"
    )
    first_receipt_register_time: Optional[datetime] = Field(
        None, 
        alias="firstReceiptRegisterTime", 
        description="First receipt registration time"
    )
    first_receipt_cancel_time: Optional[datetime] = Field(
        None, 
        alias="firstReceiptCancelTime", 
        description="First receipt cancellation time"
    )
    hide_cancelled_receipt: bool = Field(
        ..., 
        alias="hideCancelledReceipt", 
        description="Hide cancelled receipts"
    )
    register_available: Union[bool, str, None] = Field(
        None, 
        alias="registerAvailable", 
        description="Register available (mixed type)"
    )
    status: Optional[str] = Field(None, description="User status")
    restricted_mode: bool = Field(..., alias="restrictedMode", description="Restricted mode")
    pfr_url: Optional[str] = Field(None, alias="pfrUrl", description="PFR URL")
    login: Optional[str] = Field(None, description="Login")
    
    @field_validator('initial_registration_date', 'registration_date', 
                     'first_receipt_register_time', 'first_receipt_cancel_time', 
                     mode='before')
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime strings from API."""
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return None
        return v
    
    def is_avatar_exists(self) -> bool:
        """Check if user has avatar."""
        return self.avatar_exists
    
    def is_hide_cancelled_receipt(self) -> bool:
        """Check if cancelled receipts are hidden."""
        return self.hide_cancelled_receipt
    
    def is_restricted_mode(self) -> bool:
        """Check if user is in restricted mode."""
        return self.restricted_mode
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Custom serialization to match API format."""
        def serialize_datetime(dt):
            if dt is None:
                return None
            return dt.isoformat()
        
        return {
            "id": self.id,
            "lastName": self.last_name,
            "displayName": self.display_name,
            "middleName": self.middle_name,
            "email": self.email,
            "phone": self.phone,
            "inn": self.inn,
            "snils": self.snils,
            "avatarExists": self.avatar_exists,
            "initialRegistrationDate": serialize_datetime(self.initial_registration_date),
            "registrationDate": serialize_datetime(self.registration_date),
            "firstReceiptRegisterTime": serialize_datetime(self.first_receipt_register_time),
            "firstReceiptCancelTime": serialize_datetime(self.first_receipt_cancel_time),
            "hideCancelledReceipt": self.hide_cancelled_receipt,
            "registerAvailable": self.register_available,
            "status": self.status,
            "restrictedMode": self.restricted_mode,
            "pfrUrl": self.pfr_url,
            "login": self.login,
        }
