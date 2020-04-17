import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Realties(SqlAlchemyBase):
    __tablename__ = 'realties'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    realtor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    house = sqlalchemy.Column(sqlalchemy.String)
    desc = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')