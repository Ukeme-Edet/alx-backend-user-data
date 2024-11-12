#!/usr/bin/env python3
"""
Auth module
"""
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
            decoded_base64_authorization_header (str): decoded_base64_authorization_header

        Returns:
            (str, str): None
        """
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":", 1))
