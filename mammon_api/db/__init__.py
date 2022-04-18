import threading
from typing import Union
from functools import total_ordering

from sqlalchemy import create_engine
from sqlalchemy.sql import sqltypes, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from mammon_api.db.utils import filters
from mammon_api.settings.config import SQLITE_ENGINE


def create_session() -> scoped_session:
    """
    Creates a session to connect to the database
    Returns:
        scoped_session: Created session
    """
    engine = create_engine(SQLITE_ENGINE, connect_args={'check_same_thread': False})

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=Base.metadata.bind, autoflush=False, expire_on_commit=False))


Base = declarative_base()
session = create_session()
INSERTION_LOCK = threading.RLock()


def with_insertion_lock(func):
    """Blocks a thread while adding an entry"""
    def insertion_lock(*args, **kwargs):
        with INSERTION_LOCK:
            return func(*args, **kwargs)

    return insertion_lock


def inserting_errors_handling(func):
    """Handling errors on unsuccessful addition"""
    def error_handling(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as err:
            session.rollback()
            raise ValueError(*err.args) from err
        finally:
            session.close()

    return error_handling


@total_ordering
class BaseModel(Base):
    """Base Model"""
    __abstract__ = True
    id = schema.Column(sqltypes.Integer, primary_key=True, autoincrement=True, unique=True)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    @classmethod
    def _filter_input(cls, **kwargs: dict) -> dict:
        """Clears the input of unnecessary arguments"""
        required_fields = cls.__table__.columns.keys()
        filtered_kwargs = filters.leave_required_keys(kwargs, required_fields)
        required_fields.remove('id')

        # Checking that all required fields have been passed
        if set(required_fields) - set(filtered_kwargs):
            raise KeyError(f"Required fields were not passed: {set(required_fields) - set(filtered_kwargs)}")

        return filtered_kwargs

    @classmethod
    @with_insertion_lock
    @inserting_errors_handling
    def set_or_get(cls, **kwargs) -> 'BaseModel':
        """Create or get an existing model"""
        filtered_kwargs = cls._filter_input(**kwargs)
        record = session.query(cls).filter_by(**filtered_kwargs).limit(1).scalar()
        if not record:
            if 'id' in filtered_kwargs:
                filtered_kwargs.pop('id')

            record = cls(**filtered_kwargs)
            session.add(record)
            session.commit()

        return record

    @classmethod
    @with_insertion_lock
    @inserting_errors_handling
    def set(cls, **kwargs) -> 'BaseModel':
        """Create a new table entry"""
        filtered_kwargs = cls._filter_input(**kwargs)

        record = cls(**filtered_kwargs)
        session.add(record)
        session.commit()

        return record

    @classmethod
    def get_all(cls, **kwargs) -> list['BaseModel']:
        """Get all records"""
        required_fields = cls.__table__.columns.keys()
        filtered_kwargs = filters.leave_required_keys(kwargs, required_fields)

        return session.query(cls).filter_by(**filtered_kwargs).all()

    @classmethod
    def get_last(cls, **kwargs) -> Union['BaseModel', None]:
        """Get the latest record from the passed data"""
        required_fields = cls.__table__.columns.keys()
        filtered_kwargs = filters.leave_required_keys(kwargs, required_fields)

        return session.query(cls).filter_by(**filtered_kwargs).limit(1).scalar()

    @with_insertion_lock
    @inserting_errors_handling
    def update(self, update: dict) -> 'BaseModel':
        """
        Update record field data
        Args:
            update (dict): Dictionary of fields with updating values

        Returns:
            BaseModel - Class instance with updated data
        """
        session.query(self.__class__).filter_by(id=self.id).update(update)
        session.commit()

        # pylint: disable=E1101
        self.__dict__ |= update  # Merging dictionaries to update class entries
        return self

    @classmethod
    def get_pool_with_offset(cls, offset: int, pool: int) -> list['BaseModel']:
        """
        Get list of records with offset
        Args:
            offset (int): Offset in the list
            pool (int): Number of records

        Returns:
            list[BaseModel] - List of records of this model
        """
        return session.query(cls).order_by(cls.id.desc()).offset(offset).limit(pool).all()
