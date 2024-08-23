import csv


def read_country_codes(file_path) -> dict[str, str]:
    country_codes = {}
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            country_codes[row[0].upper()] = row[2]
    return country_codes
