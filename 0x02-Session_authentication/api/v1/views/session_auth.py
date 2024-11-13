#!/usr/bin/env python3
"""
Module of Session authentication views
"""
from os import getenv
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route(
    "/auth_session/login/", methods=["POST"], strict_slashes=False
)
def login():
    """
    POST /api/v1/auth_session/login/
    Return:
      - User object JSON represented
          - 400 if email is missing
          - 400 if password is missing
          - 404 if no user found for this email
          - 401 if wrong password
    """
    email, password = request.form.get("email"), request.form.get("password")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    from models.user import User

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.auth.session_auth import SessionAuth

    sa = SessionAuth()
    session_id = sa.create_session(user.id)
    session_name = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)
    return response
