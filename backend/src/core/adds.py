from src.core.config import BASE_DIR


class AppExtras:
    VERSION: str

    def __init__(self):
        self.VERSION = self._create_version()

    @staticmethod
    def _create_version():
        try:
            with open(BASE_DIR / "VERSION.txt", "r") as version_file:
                version = version_file.read()
                return version.strip()
        except FileNotFoundError:
            with open(BASE_DIR / "VERSION.txt", "w") as version_file:
                version_file.write("0.0.0")
            return "0.0.0"
