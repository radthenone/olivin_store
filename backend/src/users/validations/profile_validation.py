from datetime import date, datetime

import phonenumbers
from ninja_extra.exceptions import APIException


def validate_phone(country_code: str, number: str) -> str:
    if not number:
        raise APIException(
            detail="Phone number is required",
            code=400,
        )

    if not country_code:
        raise APIException(
            detail="Country code required",
            code=400,
        )

    if len(number) < 9 or isinstance(int(number), int) is False:
        raise APIException(
            detail="Phone number must be 9 digits long",
            code=400,
        )
    phone = country_code + number
    parsed_number = phonenumbers.parse(phone, None)
    if not phonenumbers.is_valid_number(parsed_number):
        raise APIException(
            detail=f"Invalid phone number {parsed_number.national_number}",
            code=400,
        )
    return country_code + str(parsed_number.national_number)


def validate_code(code: str) -> str:
    if not code:
        raise APIException(
            detail="Code is required",
            code=400,
        )

    if len(code) != 4:
        raise APIException(
            detail="Code must be 4 digits long",
            code=400,
        )
    return code


def validate_birth_date(birth_date: str) -> str:
    today_date = datetime.now().date()

    try:
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except APIException:
        raise APIException(
            detail="Invalid birth date format. Valid format is YYYY-MM-DD.",
            code=400,
        )
    if today_date.year - birth_date.year > 200:
        raise APIException(
            detail="User must be less than 200 years old",
            code=400,
        )

    if birth_date > today_date:
        raise APIException(
            detail="Birth date cannot be in the future",
            code=400,
        )

    if today_date.year - birth_date.year < 18:
        raise APIException(
            detail="User must be at least 18 years old",
            code=400,
        )

    return birth_date.strftime("%Y-%m-%d")
