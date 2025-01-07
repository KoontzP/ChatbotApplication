import os
from os import access

from dotenv import load_dotenv
import db as db
import sqlalchemy.orm as orm
import models as modl
import schemas as schm
import passlib.hash as hash
import jwt as jwt
import fastapi as fapi
import fastapi.security as secu
import datetime as dt
import chatbot as cb

oauth2schema = secu.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "mysecret"

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Sdtoebcp234131!!@localhost:3306/chatbotapp")


def get_db():
    database = db.sessionLocal()
    try:
        yield database
    finally:
        database.close()

async def get_user_by_email(email: str, db: orm.Session):
    return db.query(modl.User).filter(modl.User.email == email).first()

async def create_user(user: schm.UserCreate, db: orm.Session):
    user_obj = modl.User(email=user.email, hashed_password = hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user

async def create_token(user: modl.User):
    user_obj = schm.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token = token, token_type="bearer")

async def get_current_user(db: orm.Session = fapi.Depends(get_db), token: str = fapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(modl.User).get(payload["id"])
    except:
        raise fapi.HTTPException(status_code=401, detail="Invalid Email or Password")

    return schm.User.from_orm(user)

async def create_message(user: schm.User, db: orm.Session, content: str):

    bot_response = cb.generate_response(content)

    message = modl.Message(
        user_id=user.id,
        content=content,
        bot_response=bot_response,
        date_created=dt.datetime.utcnow()
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    return message


async def get_messages(user: schm.User, db: orm.Session):
    messages = db.query(modl.Message).filter_by(user_id = user.id).all()
    return messages


async def message_selector(message_id: int, user: schm.User, db: orm.Session):
    message = (
        db.query(modl.Message)
        .filter_by(user_id = user.id)
        .filter(modl.Message.id == message_id)
        .first()
    )

    if message is None:
        raise fapi.HTTPException(status_code=404, detail="Message does not exist")

    return message


async def get_message(message_id: int, user: schm.User, db: orm.Session):
    message = await message_selector(message_id, user, db)
    return schm.ChatMessageResponse.from_orm(message)


async def delete_message(message_id: int, user: schm.User, db: orm.Session):
    message = await message_selector(message_id, user, db)
    db.delete(message)
    db.commit()
