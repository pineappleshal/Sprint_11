import json

import allure


SECRET_KEYS = {'password', 'submitpassword', 'access_token', 'refresh_token', 'authorization', 'token'}


def redact_secrets(value):
    if isinstance(value, dict):
        return {
            key: '<скрыто>' if key.lower() in SECRET_KEYS else redact_secrets(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    return value


def attach_json(name, value):
    allure.attach(
        json.dumps(redact_secrets(value), ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )
