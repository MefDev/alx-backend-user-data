#!/usr/bin/env python3
# """The auth module."""
from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> str:
    """Hash a password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    def register_user(self, email: str, password: str) -> User | None:
        """Register a user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))


