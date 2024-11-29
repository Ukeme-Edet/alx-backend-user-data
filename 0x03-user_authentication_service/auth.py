#!/usr/bin/env python3
"""
Auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB, User, NoResultFound
from uuid import uuid4


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
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login

        Args:
            email (str): The user's email
            password (str): The user's password

        Returns:
            bool: True if the password is valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode("utf-8"), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for a user

        Args:
            email (str): The user's email

        Returns:
            str: The new session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user from a session ID

        Args:
            session_id (str): The session ID

        Returns:
            User: The user associated with the session ID
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session

        Args:
            user_id (int): The user identifier
        """
        self._db.update_user(user_id, session_id=None)


def _hash_password(password: str) -> str:
    """
    Hash a password

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """
    Generate a new UUID

    Returns:
        str: The new UUID
    """
    return str(uuid4())
