from enum import Enum

from src.core.config import BASE_DIR
from src.users.files import read_country_codes

COUNTRY_CODES = read_country_codes(BASE_DIR / "media" / "files" / "country_codes.csv")


def create_country_enum():
    enum = Enum(
        "CountryEnum",
        read_country_codes(BASE_DIR / "media" / "files" / "country_codes.csv"),
    )

    def choices(cls):
        return [(i.name, i.value) for i in cls]

    setattr(enum, "choices", classmethod(choices))

    return enum


CountryCodeEnum = create_country_enum()
