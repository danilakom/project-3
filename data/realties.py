import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Realties(SqlAlchemyBase):
    __tablename__ = 'realties'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    realtor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    house = sqlalchemy.Column(sqlalchemy.String)
    not_solded_flats = sqlalchemy.Column(sqlalchemy.Integer)
    address = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_sold = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    user = orm.relation('User')