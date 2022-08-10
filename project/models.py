from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genres(models.Base):
    __tablename__ = "genres"

    name = Column(String(100), unique=True, nullable=False)


class Directors(models.Base):
    __tablename__ = "directors"

    name = Column(String(100), unique=True, nullable=False)


class Movies(models.Base):
    __tablename__ = "movies"

    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(100), unique=True, nullable=False)
    trailer = Column(String(100), unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey(f"{Genres.__tablename__}.id"), nullable=False)
    director_id = Column(Integer, ForeignKey(f"{Directors.__tablename__}.id"), nullable=False)
    director = relationship("Directors")
    genre = relationship("Genres")


class Users(models.Base):
    __tablename__ = "users"

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    favourite_genre = Column(Integer, ForeignKey(f"{Genres.__tablename__}.id"))
    genre = relationship("Genres")
