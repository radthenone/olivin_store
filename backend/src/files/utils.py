import io

from ninja.files import UploadedFile


def get_file(file: UploadedFile) -> io.BytesIO:
    return io.BytesIO(file.read())


def get_file_name(file: UploadedFile) -> str:
    return file.name
