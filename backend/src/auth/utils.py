from django.contrib.auth.hashers import make_password


def hash_password(password: str) -> str:
    password = make_password(password)

    return password
