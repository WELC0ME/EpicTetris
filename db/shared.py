import sqlalchemy
from .db_session import SqlAlchemyBase


class Shared(SqlAlchemyBase):
    __tablename__ = 'shared'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True,
                           primary_key=True)
    data = sqlalchemy.Column(sqlalchemy.String)
