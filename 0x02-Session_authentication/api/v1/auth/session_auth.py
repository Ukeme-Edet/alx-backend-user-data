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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get a user ID based on a session ID.

        Args:
            session_id (str, optional): The session ID. Defaults to None.

        Returns:
            str: The user ID if the session ID is found, None otherwise.
        """
        if session_id is None or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
