"""
Device-related DTO models.
Based on PHP library's DTO\\DeviceInfo class.
"""

from typing import Any, Dict

from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    """
    Device information model for API requests.
    Maps to PHP DTO\\DeviceInfo.
    """
    
    # Constants from PHP class
    SOURCE_TYPE_WEB = "WEB"
    APP_VERSION = "1.0.0"
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    )
    
    source_type: str = Field(
        default=SOURCE_TYPE_WEB,
        alias="sourceType", 
        description="Source type (usually WEB)"
    )
    source_device_id: str = Field(
        ..., 
        alias="sourceDeviceId", 
        description="Device ID"
    )
    app_version: str = Field(
        default=APP_VERSION,
        alias="appVersion", 
        description="Application version"
    )
    user_agent: str = Field(
        default=USER_AGENT,
        description="User agent string"
    )
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Custom serialization to match PHP jsonSerialize format."""
        return {
            "sourceType": self.source_type,
            "sourceDeviceId": self.source_device_id,
            "appVersion": self.app_version,
            "metaDetails": {
                "userAgent": self.user_agent
            }
        }
