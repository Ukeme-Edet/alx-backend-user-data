#!/usr/bin/env python3
"""
SessionExpAuth module
"""
from datetime import datetime, timedelta
import os
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class
    """

    def __init__(self) -> None:
        """
        Initialize a SessionExpAuth instance
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def creeate_session(self, user_id=None):
        """
        Create a new session

        Args:
            user_id: str: User ID

        Returns:
            str: Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Get the User ID by Session ID

        Args:
            session_id: str: Session ID

        Returns:
            str: User ID
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict["user_id"]
            if "created_at" not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict["created_at"] + time_span
            if exp_time < cur_time:
                return None
            return session_dict["user_id"]
