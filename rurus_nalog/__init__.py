"""
Asynchronous Python client for Russian self-employed tax service (Moy Nalog).

This is a Python port of the PHP library shoman4eg/moy-nalog,
providing async HTTP client for interaction with lknpd.nalog.ru API.

Original PHP library: https://github.com/shoman4eg/moy-nalog
Author: Artem Dubinin <artem@dubinin.me>
License: MIT
"""

from .client import Client
from .exceptions import (
    DomainException,
    ValidationException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    ClientException,
    PhoneException,
    ServerException,
    UnknownErrorException,
)

__version__ = "0.1.0"
__all__ = [
    "Client",
    "DomainException",
    "ValidationException", 
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ClientException",
    "PhoneException",
    "ServerException",
    "UnknownErrorException",
]
