#!/usr/bin/env python3
"""
Session authentication module
"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    SessionAuth class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session ID for a given user ID.

        Args:
            user_id (str, optional): The ID of the user. Defaults to None.

        Returns:
            str: The generated session ID if successful, None otherwise.
                Returns None if user_id is None or not a string.

        Note:
            The session ID is generated using UUID4 and stored in
            the class dictionary user_id_by_session_id.
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
