import argparse
import errno
import logging
import os
import sys
import warnings
from datetime import datetime

import uvicorn
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.core.servers.basehttp import WSGIServer, run
from django.core.wsgi import get_wsgi_application
from django.db import connections
from django.utils import autoreload

warnings.filterwarnings("ignore", category=DeprecationWarning, module="django.conf")

logger = logging.getLogger(__name__)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
    )
    import django

    django.setup()


def get_wsgi_handler():
    """Return the default WSGI handler for the runner."""
    return get_wsgi_application()


def get_asgi_handler():
    """Return the default ASGI handler for the runner."""
    return get_asgi_application()


def check_settings():
    if not settings.DEBUG and not settings.ALLOWED_HOSTS:
        raise ValueError("You must set settings.ALLOWED_HOSTS if DEBUG is False.")


def create_migrations():
    from django.apps import apps
    from django.core.management import call_command

    logger.info("Creating migrations for all apps.")
    for app_config in apps.get_app_configs():
        try:
            call_command("makemigrations", app_config.label)
        except Exception as e:
            logger.error(f"Error while creating migrations for {app_config.label}: {e}")


def check_migrations_and_connections():
    from django.core.management import call_command
    from django.db.utils import ProgrammingError

    call_command("check")

    # Create migrations before applying them
    create_migrations()

    logger.info("Checking for migrations.")
    try:
        call_command("migrate")
    except ProgrammingError as e:
        logger.error("Error while applying migrations: %s", e)

    for conn in connections.all(initialized_only=True):
        conn.close()


def start_server(mode, addr, port, use_reloader, threading, protocol):
    if use_reloader:
        if mode == "wsgi":
            autoreload.run_with_reloader(
                run_wsgi_server, addr, port, threading, protocol
            )
        else:
            autoreload.run_with_reloader(run_asgi_server, addr, port)
    else:
        if mode == "wsgi":
            run_wsgi_server(addr, port, threading, protocol)
        else:
            run_asgi_server(addr, port)


def run_wsgi_server(addr, port, threading, protocol):
    try:
        handler = get_wsgi_handler()
        run(
            addr,
            int(port),
            handler,
            ipv6=False,
            threading=threading,
            on_bind=on_bind(protocol, addr, port),
            server_cls=WSGIServer,
        )
        logger.info("WSGI server started on %s:%s", addr, port)
    except OSError as e:
        handle_error(e)
    except KeyboardInterrupt:
        sys.exit(0)


def run_asgi_server(addr, port):
    try:
        uvicorn.run(
            "src.core.asgi:application",
            host=addr,
            port=int(port),
            log_level="info",
        )
        logger.info("ASGI server started on %s:%s", addr, port)
    except OSError as e:
        handle_error(e)
    except KeyboardInterrupt:
        sys.exit(0)


def handle_error(e):
    errors = {
        errno.EACCES: "You don't have permission to access that port.",
        errno.EADDRINUSE: "That port is already in use.",
        errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
    }
    error_text = errors.get(e.errno, str(e))
    sys.stderr.write("Error: %s\n" % error_text)
    sys.exit(1)


def on_bind(protocol, addr, port):
    from django import get_version

    quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

    now = datetime.now().strftime("%B %d, %Y - %X")

    logger.info("Running Django: %s", now)
    logger.info(
        "Django version %s using settings %s", get_version(), settings.SETTINGS_MODULE
    )
    logger.info("Starting development server on %s://%s:%s", protocol, addr, port)

    print(
        f"Quit the server with {quit_command}.",
        file=sys.stdout,
    )


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--wsgi", action="store_true", help="Run with WSGI")

    group.add_argument("--asgi", action="store_true", help="Run with ASGI")

    args = parser.parse_args()

    if args.wsgi:
        return "wsgi"
    elif args.asgi:
        return "asgi"


def run_auto():
    from src.core.storage import get_storage
    from src.data.handlers import EventHandler, ImageFileHandler, TemplateHandler
    from src.data.managers import EventManager
    from src.users.repositories import UserRepository
    from src.users.schemas import SuperUserCreateSchema
    from src.users.services import UserService

    user_service = UserService(
        repository=UserRepository(),
    )
    if not user_service.is_superuser_exists():
        super_user_create_schema = SuperUserCreateSchema(
            email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
            password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
            is_staff=True,
            is_superuser=True,
        )
        super_user = user_service.create_superuser(
            super_user_create_schema=super_user_create_schema,
        )

        logger.info(
            "Superuser created with email [blue]%s[/]",
            super_user.email,
            extra={"markup": True},
        )
    else:
        logger.info(
            "Superuser already exists",
        )
    image_handler = ImageFileHandler(storage=get_storage())
    image_handler.upload_image(
        filename="register.png",
    )

    template_handler = TemplateHandler(storage=get_storage())
    template_handler.upload_template("register-mail.html")

    event_handler = EventHandler(manager=EventManager())
    # event_handler.start_subscribers()
    event_handler.start_handlers()


def register():
    setup_django()
    mode = parse_arguments()
    addr = getattr(settings, "DJANGO_HOST", "127.0.0.1")
    port = getattr(settings, "DJANGO_PORT", 8000)
    protocol = "https" if getattr(settings, "DJANGO_USE_HTTPS", False) else "http"
    use_reloader = getattr(settings, "DJANGO_USE_RELOADER", True)
    threading = getattr(settings, "DJANGO_USE_THREADING", True)

    if os.getenv("RUN_MAIN") != "true":
        check_settings()
        check_migrations_and_connections()
        run_auto()

    start_server(mode, addr, port, use_reloader, threading, protocol)


if __name__ == "__main__":
    register()
