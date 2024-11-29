#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, session, abort, redirect
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route("/", methods=["GET"])
def hello() -> str:
    """
    GET /

    Returns:
        str: Welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> str:
    """
    POST /users

    Form data:
        - email
        - password

    Returns:
        str: The new user
    """
    data = request.form.to_dict()
    try:
        new_user = AUTH.register_user(data["email"], data["password"])
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """
    POST /sessions

    Form data:
        - email
        - password

    Returns:
        str: The new session ID
    """
    data = request.form.to_dict()
    if AUTH.valid_login(data["email"], data["password"]):
        session_id = AUTH.create_session(data["email"])
        response = jsonify({"email": data["email"], "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """
    DELETE /sessions

    Form data:
        - session_id

    Returns:
        str: The new session ID
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """
    GET /profile

    Returns:
        str: The user's profile
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """
    POST /reset_password

    Form data:
        - email

    Returns:
        str: The reset password token
    """
    data = request.form.to_dict()
    try:
        reset_token = AUTH.get_reset_password_token(data["email"])
        return jsonify({"email": data["email"], "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """
    PUT /reset_password

    Form data:
        - email
        - reset_token
        - new_password

    Returns:
        str: The new password
    """
    data = request.form.to_dict()
    try:
        AUTH.update_password(data["reset_token"], data["new_password"])
        return jsonify({"email": data["email"], "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
