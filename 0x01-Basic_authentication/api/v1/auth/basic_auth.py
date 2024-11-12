#!/usr/bin/env python3
"""
Auth module
"""
from typing import TypeVar
from .auth import Auth
import base64


class BasicAuth(Auth):
    """
    BasicAuth class
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        extract_base64_authorization_header method

        Args:
            authorization_header (str): authorization_header

        Returns:
            str: None
        """
        if (
            authorization_header is None
            or type(authorization_header) is not str
        ):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        decode_base64_authorization_header method

        Args:
            base64_authorization_header (str): base64_authorization_header

        Returns:
            str: None
        """
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) is not str
        ):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header.encode("utf-8")
            ).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        extract_user_credentials method

        Args:
            decoded_base64_authorization_header (str):\
                decoded_base64_authorization_header

        Returns:
            (str, str): None
        """
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)
        i = decoded_base64_authorization_header.index(":")
        return (
            decoded_base64_authorization_header[:i],
            decoded_base64_authorization_header[i + 1 :],
        )

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        user_object_from_credentials method

        Args:
            user_email (str): user_email
            user_pwd (str): user_pwd

        Returns:
            TypeVar('User'): None
        """
        from models.user import User

        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({"email": user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        current_user method

        Args:
            request (request): request

        Returns:
            TypeVar('User'): None
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )
        if base64_auth_header is None:
            return None
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        if decoded_base64_auth_header is None:
            return None
        user_credentials = self.extract_user_credentials(
            decoded_base64_auth_header
        )
        if user_credentials[0] is None or user_credentials[1] is None:
            return None
        return self.user_object_from_credentials(
            user_credentials[0], user_credentials[1]
        )
