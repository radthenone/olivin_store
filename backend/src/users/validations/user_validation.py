import re

from django.core import validators
from ninja.errors import HttpError


def check_passwords_match(password: str, rewrite_password: str) -> bool:
    if password != rewrite_password:
        raise HttpError(status_code=400, message="Passwords do not match")
    return True


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise HttpError(
            status_code=400,
            message="Password must be at least 8 characters long",
        )
    if not any(char.isdigit() for char in password):
        raise HttpError(
            status_code=400,
            message="Password must contain at least one number",
        )
    if not any(char.isupper() for char in password):
        raise HttpError(
            status_code=400,
            message="Password must contain at least one uppercase letter",
        )
    if not any(char.islower() for char in password):
        raise HttpError(
            status_code=400,
            message="Password must contain at least one lowercase letter",
        )
    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>/?~" for char in password):
        raise HttpError(
            status_code=400,
            message="Password must contain at least one special character",
        )
    return password


def validate_username(username: str) -> str:
    pattern = r"^[a-zA-Z0-9_-]{3,16}$"
    if not re.match(pattern, username):
        raise HttpError(status_code=400, message="Invalid username")
    return username


def validate_email(email: str) -> str:
    try:
        validators.validate_email(email)
    except validators.ValidationError:
        raise HttpError(status_code=400, message="Invalid email address")
    return email
