#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a new session

        Args:
            user_id: str: User ID

        Returns:
            str: Session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = user_id
            UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """
        Get the User ID by Session ID

        Args:
            session_id: str: Session ID

        Returns:
            str: User ID
        """
        if not session_id:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        if not user_id:
            user_session = UserSession.search({"session_id": session_id})
            if user_session:
                user_id = user_session[0].user_id
                self.user_id_by_session_id[session_id] = user_id
        return user_id

    def destroy_session(self, request=None):
        """
        Destroy a session

        Args:
            request: obj: HTTP request object

        Returns:
            bool: True if session was destroyed, False if it was not possible
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        user_sessions = UserSession.search({"session_id": session_id})
        for user_session in user_sessions:
            user_session.remove()
        return True
