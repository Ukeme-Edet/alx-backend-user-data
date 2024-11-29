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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
