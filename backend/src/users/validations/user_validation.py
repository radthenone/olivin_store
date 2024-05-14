import re
from uuid import UUID

import phonenumbers
from django.core import validators
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from ninja.errors import HttpError


def do_geocode(user_id, address):
    geopy = Nominatim(user_agent=str(user_id))
    try:
        return geopy.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(user_id, address)


def check_full_address(
    user_id: UUID,
    street: str,
    district: str,
    number: str,
    city: str,
    postal_code: str,
    country: str,
) -> bool:
    postal_pattern = r"^\d{2}-\d{3}$"
    if not user_id:
        raise HttpError(status_code=400, message="User ID is required")
    if not all(
        [
            street,
            number,
            city,
            postal_code,
            country,
        ]
    ):
        raise HttpError(status_code=400, message="All fields are required")
    if not re.match(postal_pattern, postal_code):
        raise HttpError(status_code=400, message="Invalid postal code")

    post_code_location = do_geocode(user_id, postal_code)
    if post_code_location is None:
        raise HttpError(status_code=400, message="Postal code is not correct")
    post_code_location = post_code_location.address.split(", ")
    p_district, p_city = post_code_location[1:3]

    location = do_geocode(user_id, f"{street} {number} {district} {city} {country}")
    if location is None:
        raise HttpError(status_code=400, message="Street, number, city are not correct")
    location = location.address.split(", ")
    u_number, u_street = location[0:2]

    if any(value is None for value in (p_district, p_city, u_number, u_street)):
        raise HttpError(
            status_code=400,
            message="Postal code, district, city, province, country are not correct",
        )
    return True


def check_number_and_country_code(phone: str) -> bool:
    """
    Checks if the phone number is valid.
    phone: like +33612345678
    :param phone: str
    :return: bool
    """
    if not phone:
        raise HttpError(status_code=400, message="Phone number is required")

    country_code = phone[:3]
    number = phone[3:]

    if country_code[0] != "+" or len(country_code) != 3:
        raise HttpError(status_code=400, message="Invalid country code")

    if len(phone) < 9 or isinstance(int(number), int) is False:
        raise HttpError(status_code=400, message="Invalid phone number")
    try:
        parsed_number = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise HttpError(status_code=400, message="Invalid phone number")


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
