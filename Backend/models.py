import sqlalchemy as sql
import sqlalchemy.orm as orm
import passlib.hash as hash
import datetime as dt
from db import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    name = sql.Column(sql.String(255))
    email = sql.Column(sql.String(255), unique=True, index=True)
    hashed_password = sql.Column(sql.String(255))


    message = orm.relationship("Message", back_populates="user")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)

class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'), nullable=True)
    content = sql.Column(sql.Text, nullable=False, index=True)
    bot_response = sql.Column(sql.Text, nullable=True)
    date_created = sql.Column(sql.DateTime, default=dt.datetime.utcnow())



    user = orm.relationship("User", back_populates="message")
