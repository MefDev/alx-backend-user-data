"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> User | None:
        """Add a new user
        """
        self._session.add(User(email=email, hashed_password=hashed_password))
        self._session.commit()
        return self._session.query(User).filter_by(email=email).first()

    def find_user_by(self, **kwargs) -> User | None:
        """Find a user by a given attribute
        """
        current_user = self._session.query(User).filter_by(**kwargs).first()
        if (current_user):
            return current_user
        elif (current_user is None):
            raise NoResultFound
        else:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """update a user"""
        found_user = self.find_user_by(id=user_id)
        if (not found_user):
            raise NoResultFound
        for key, value in kwargs.items():
            setattr(found_user, key, value)
        self._session.commit()
