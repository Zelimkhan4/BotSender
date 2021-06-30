import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Resident(SqlAlchemyBase):
    __tablename__ = "Residents" 
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    chat_id = sa.Column(sa.Integer)
    name = sa.Column(sa.String)
    surname = sa.Column(sa.String)
    track = sa.Column(sa.String)
    skill = sa.Column(sa.String)
    groups = sa.Column(sa.String, default="")


class Group(SqlAlchemyBase):
    __tablename__ = "Group"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Integer)
    