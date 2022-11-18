"""
Class for application configuration to setup env variables
"""

import os
from typing import get_type_hints, Union
from dotenv import load_dotenv

load_dotenv()

# pylint: disable=E1101


class AppConfigError(Exception):
    """
    Class for configuration error
    """


def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ["true", "yes", "1"]


class AppConfig:
    """
    AppConfig class with required fields, default values, type checking,
    and typecasting for int and bool values
    """

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    FTP_HOST: str
    FTP_USER: str
    FTP_PASS: str

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError(f"The {field} field is required")

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)

            except ValueError:
                raise AppConfigError(
                    f"Unable to cast value of {env[field]} to type {var_type} for {field} field"
                )

    def __repr__(self):
        return str(self.__dict__)


# Expose Config object for app to import
Config = AppConfig(os.environ)
