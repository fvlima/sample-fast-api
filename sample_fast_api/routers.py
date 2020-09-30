import logging
from importlib import import_module

logger = logging.getLogger(__name__)

app_routers = [
    "sample_fast_api.apps.users.routers",
    "sample_fast_api.apps.auth.routers",
]


def load_routers(app):
    for path in app_routers:
        module = import_module(path)

        function = getattr(module, "include_router")
        function(app)

        logger.info("Initialized router to %s", path)
