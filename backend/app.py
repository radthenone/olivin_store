import errno
import logging
import os
import sys
from datetime import datetime

from django.conf import settings
from django.core.servers.basehttp import WSGIServer, run
from django.core.wsgi import get_wsgi_application
from django.db import connections
from django.utils import autoreload

logger = logging.getLogger(__name__)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


def setup_django():
    (os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),)
    import django

    django.setup()


def get_handler():
    """Return the default WSGI handler for the runner."""
    return get_wsgi_application()


def check_settings():
    if not settings.DEBUG and not settings.ALLOWED_HOSTS:
        raise ValueError("You must set settings.ALLOWED_HOSTS if DEBUG is False.")


def check_migrations_and_connections():
    from django.core.management import call_command

    call_command("check")
    call_command("migrate")
    for conn in connections.all(initialized_only=True):
        conn.close()


def start_server(addr, port, use_reloader, threading, protocol):
    if use_reloader:
        autoreload.run_with_reloader(inner_run, addr, port, threading, protocol)
    else:
        inner_run(addr, port, threading, protocol)


def inner_run(addr, port, threading, protocol):
    try:
        handler = get_handler()
        run(
            addr,
            int(port),
            handler,
            ipv6=False,
            threading=threading,
            on_bind=on_bind(protocol, addr, port),
            server_cls=WSGIServer,
        )
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
    quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

    now = datetime.now().strftime("%B %d, %Y - %X")

    if "django" in settings.SETTINGS_MODULE:
        from django import get_version

        version = get_version()

    else:
        version = "unknown"

    logger.info("Running Django: %s", now)
    logger.info(
        "Django version %s using settings %s", version, settings.SETTINGS_MODULE
    )
    logger.info("Starting development server on %s://%s:%s", protocol, addr, port)

    print(
        f"Quit the server with {quit_command}.",
        file=sys.stdout,
    )


def run_auto():
    from src.core.storage import get_storage
    from src.data.handlers import EventHandler, ImageFileHandler, TemplateHandler
    from src.data.managers import EventManager

    image_handler = ImageFileHandler(storage=get_storage())
    image_handler.upload_image(
        filename="register.png",
    )

    template_handler = TemplateHandler(storage=get_storage())
    template_handler.upload_template("register-mail.html")

    event_handler = EventHandler(manager=EventManager())
    event_handler.start_handlers()


def register():
    setup_django()
    addr = getattr(settings, "DJANGO_HOST", "127.0.0.1")
    port = getattr(settings, "DJANGO_PORT", 8000)
    protocol = "https" if getattr(settings, "DJANGO_USE_HTTPS", False) else "http"
    use_reloader = getattr(settings, "DJANGO_USE_RELOADER", True)
    threading = getattr(settings, "DJANGO_USE_THREADING", True)

    if os.getenv("RUN_MAIN") != "true":
        check_settings()
        check_migrations_and_connections()
        run_auto()

    start_server(addr, port, use_reloader, threading, protocol)


if __name__ == "__main__":
    register()
