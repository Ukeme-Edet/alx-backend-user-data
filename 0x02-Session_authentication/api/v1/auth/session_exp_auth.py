#!/usr/bin/env python3
"""
"""
from datetime import datetime, timedelta
import os
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    def __init__(self) -> None:
        super().__init__()
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def creeate_session(self, user_id=None):
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        if (
            session_id is None
            or self.user_id_by_session_id.get(session_id, None) is None
        ):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]
        if (
            self.user_id_by_session_id[session_id].get("created_at", None)
            is None
            or self.user_id_by_session_id[session_id].get("created_at", None)
            + timedelta(seconds=self.session_duration)
            > datetime.now()
        ):
            return None
        return self.user_id_by_session_id[session_id].get("user_id")
