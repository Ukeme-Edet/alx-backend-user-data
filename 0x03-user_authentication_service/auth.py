#!/usr/bin/env python3
"""
Auth module
"""
from bcrypt import hashpw, gensalt
from db import DB, User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user

        Args:
            email (str): The user's email
            password (str): The user's password

        Returns:
            User: The newly created User object
        """
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError(f"User {email} already exists")
        return self._db.add_user(email, _hash_password(password))


def _hash_password(password: str) -> str:
    """
    Hash a password

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """
    return hashpw(password.encode("utf-8"), gensalt())
