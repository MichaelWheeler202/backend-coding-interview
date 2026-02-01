from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest

import logging

logger = logging.getLogger(__name__)

class GithubSSOBackend(ModelBackend):
    """Simple test for custom authentication backend"""


def pre_login_callback(user: User, request: WSGIRequest):
    """Callback function called before user is logged in."""
    logger.info(f"Running Pre-Login callback for user: {user}.")

