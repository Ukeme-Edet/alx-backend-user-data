#!/usr/bin/env python3
"""
Auth module
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth method

        Args:
            path (str): path
            excluded_paths (List[str]): excluded_paths

        Returns:
            bool: True if path is not None and excluded_paths is not None
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        authorization_header method

        Args:
            request (request): request

        Returns:
            str: None
        """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        current_user method

        Args:
            request (request): request

        Returns:
            TypeVar('User'): None
        """
        return None
