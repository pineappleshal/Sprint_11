from secrets import token_urlsafe
from uuid import uuid4

from helpers.models import Credentials


def generate_email():
    return f'vk_desk_{uuid4().hex}@example.com'


def generate_credentials():
    return Credentials(email=generate_email(), password=f'Desk_{token_urlsafe(18)}!')
