import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    question = sa.Column(sa.String, nullable=True)
    answer = sa.Column(sa.String, nullable=True)


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    question = sa.Column(sa.String, nullable=True)


class Game(SqlAlchemyBase):
    __tablename__ = 'Game'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    game = sa.Column(sa.String, nullable=True)
    answer_game = sa.Column(sa.String, nullable=True)
