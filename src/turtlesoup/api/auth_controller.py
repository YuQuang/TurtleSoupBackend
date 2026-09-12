import os

import jwt
from flask import jsonify, request


class AuthController:
    def __init__(self, secret_key: str | None = None) -> None:
        self._secret_key = secret_key or os.getenv("JWT_SECRET_KEY")

    def me(self):
        if not self._secret_key: return jsonify({"error": "JWT secret is not configured"}), 500

        token = request.cookies.get("Authorization")
        if not token: return jsonify({"error": "Authentication required"}), 401

        if token.startswith("Bearer "): token = token[7:]
        
        try:
            claims = jwt.decode(token, self._secret_key, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return jsonify(claims)