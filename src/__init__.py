"""
Password Generator Package
A simple yet robust password generation utility.
"""

__version__ = "1.0.0"
__author__ = "Password Generator"

from .generator import PasswordGenerator
from .validator import PasswordCriteria

__all__ = ["PasswordGenerator", "PasswordCriteria"]
