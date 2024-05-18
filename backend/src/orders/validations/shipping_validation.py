import re
from uuid import UUID

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from ninja.errors import HttpError


def do_geocode(user_id, address):
    geopy = Nominatim(user_agent=str(user_id))
    try:
        return geopy.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(user_id, address)


def validate_address(
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
