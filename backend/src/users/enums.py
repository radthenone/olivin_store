from enum import Enum

from src.core.config import BASE_DIR
from src.users.files import read_country_codes

COUNTRY_CODES = read_country_codes(BASE_DIR / "media" / "files" / "country_codes.csv")


def create_country_enum(country_codes: dict[str, str] = None):
    if country_codes is None:
        country_codes = COUNTRY_CODES

    enum = Enum(
        "CountryEnum", {code: country for country, code in country_codes.items()}
    )

    def choices(cls):
        return [(i.name, i.value) for i in cls]

    setattr(enum, "choices", classmethod(choices))

    return enum


CountryEnum = create_country_enum()
