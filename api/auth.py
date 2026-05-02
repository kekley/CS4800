"""
Utility functions for authentication and authorization using Auth0.
"""

import requests
from constants import (
    AUTH0_ALGORITHMS,
    AUTH0_API_IDENTIFIER,
    AUTH0_DOMAIN,
)
from flask import g, jsonify, request
from flask_extensions import db
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from models.user import User
from sqlalchemy import select


def get_user(token):
    try:
        res = requests.get(
            f"https://{AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": token},
        )
        user_info = res.json()
        return user_info
    except Exception as e:
        print(f"Failed to fetch user info from Auth0: {e}")
        return None


def is_m2m_token(payload):
    sub = payload.get("sub", "")
    if "@clients" in sub:
        return True
    if "client_id" in payload and "email" not in payload:
        return True
    return False


def get_jwks():
    jwks_json = requests.get(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    return jwks_json.json()


def require_auth(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", None)
        if not token:
            return jsonify({"message": "Missing token"}), 401

        token = token.split()[1]
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if not rsa_key:
            return jsonify({"message": "Invalid token"}), 401

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=AUTH0_ALGORITHMS,
                audience=AUTH0_API_IDENTIFIER,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
        except ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except JWTClaimsError:
            return jsonify({"message": "Invalid claims"}), 401
        except Exception:
            return jsonify({"message": "Invalid token"}), 401

        if not is_m2m_token(payload):
            sub = payload.get("sub")
            user = db.session.execute(
                select(User).where(User.auth0_subject == sub)
            ).scalar_one_or_none()

            if not user:
                user_info = get_user(request.headers.get("Authorization", None))
                if not user_info:
                    return jsonify({"message": "Failed to fetch user information."}), 500
                
                user = User(
                    auth0_subject=sub,
                    email=user_info["email"],
                    avatar_url=user_info["picture"],
                    displayName=f"{user_info['given_name']} {user_info['family_name']}"
                )

                db.session.add(user)
                db.session.commit()

            g.user = user
        else:
            g.user = "AGENT"
            
        request.user = payload
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper
