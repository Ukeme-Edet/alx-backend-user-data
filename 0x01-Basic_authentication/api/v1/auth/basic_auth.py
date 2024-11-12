#!/usr/bin/env python3
"""
Auth module
"""
from .auth import Auth


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