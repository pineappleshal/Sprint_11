import os


API_URL = os.getenv('API_URL', 'https://qa-desk.education-services.ru/api').rstrip('/')
REQUEST_TIMEOUT = (5, 30)
