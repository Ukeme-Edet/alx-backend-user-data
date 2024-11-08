#!/usr/bin/env python3
"""
This module contains a method that returns the log message obfuscated
"""
import re
from typing import List
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum

        Args:
            record (logging.LogRecord): a log record

        Returns:
            str: the log message obfuscated
        """
        return filter_datum(
            self.fields,
            self.REDACTION,
            super().format(record),
            self.SEPARATOR,
        )


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Returns the log message obfuscated

    Args:
        fields (List[str]): a list of strings representing all fields to\
            obfuscate
        redaction (str): a string representing by what the field will be\
            obfuscated
        message (str): a string representing the log line
        separator (str): a string representing by which character is\
            separating all fields in the log line

    Returns:
        str: the log message obfuscated
    """
    for field in fields:
        message = re.sub(
            f"{field}=(.*?){separator}",
            f"{field}={redaction}{separator}",
            message,
        )
    return message


def get_logget() -> logging.Logger:
    """
    Returns a logging.Logger object

    Returns:
        logging.Logger: a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
