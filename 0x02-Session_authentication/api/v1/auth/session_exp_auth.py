#!/usr/bin/env python3
"""
Session expiration authentication module
"""
import os
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration."""

    def __init__(self) -> None:
        """Initializes a new SessionExpAuth instance."""
        super().__init__()
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a new session ID for a given user ID.

        Args:
            user_id (str, optional): The ID of the user. Defaults to None.

        Returns:
            str: The generated session ID if successful, None otherwise.
                Returns None if user_id is None or not a string."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get a user ID based on a session ID.

        Args:
            session_id (str, optional): The session ID. Defaults to None.

        Returns:
            str: The user ID if the session ID is found, None otherwise.
        """
        sessiod_dict = self.user_id_by_session_id.get(session_id)
        if sessiod_dict is None:
            return None
        if self.session_duration <= 0:
            return sessiod_dict.get("user_id")
        if (
            sessiod_dict.get(
                "created_at",
                datetime(1, 1, 1) + timedelta(seconds=self.session_duration),
            )
            < datetime.now()
        ):
            return None
        return sessiod_dict.get("user_id")
