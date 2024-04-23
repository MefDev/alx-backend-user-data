#!/usr/bin/env python3
"""Simple flask app"""

from flask import Flask, jsonify, Response, request
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def status() -> Response:
    """Welcome to the app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> Response:
    """Register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
