import fastapi as fapi
import fastapi.security as secu
import sqlalchemy.orm as orm
import schemas as schem
import settings as sett
import models
import db as db
import chatbot as cb
from fastapi.responses import JSONResponse
import datetime as dt
from typing import List


app = fapi.FastAPI()
db.Base.metadata.create_all(bind=db.engine)


# Endpoint to create a new user
@app.post("/api/users/")
async def create_user(user: schem.UserCreate, db: orm.session = fapi.Depends(sett.get_db)):
    db_user = await sett.get_user_by_email(user.email, db)
    if db_user:
        raise fapi.HTTPException(status_code=400, detail="Email already in use")
    user = await sett.create_user(user, db)

    return await sett.create_token(user)

# Endpoint to generate a token for authentication
@app.post("/api/token")
async def generate_token(form_data: secu.OAuth2PasswordRequestForm = fapi.Depends(),
db: orm.Session = fapi.Depends(sett.get_db)):

    user = await sett.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await sett.create_token(user)

@app.get("/api/users/me", response_model=schem.User)
async def get_user(user: schem.User = fapi.Depends(sett.get_current_user)):
    return user


@app.post("/api/messages", response_model=schem.ChatMessageResponse)
async def create_message(
        message: schem.ChatMessageCreate,
        user: schem.User = fapi.Depends(sett.get_current_user),
        db: orm.Session = fapi.Depends(sett.get_db),
):

        message = await sett.create_message(user, db, message.content)

        return schem.ChatMessageResponse(
            id=message.id,
            user_id=message.user_id,
            user_message=message.content,
            bot_response=message.bot_response,
            date_created=message.date_created
        )


@app.get("/api/messages", response_model=List[schem.ChatMessageResponse])
async def get_messages(
        user: schem.User = fapi.Depends(sett.get_current_user),
        db: orm.Session = fapi.Depends(sett.get_db),
):
    messages = await sett.get_messages(user, db)

    # Transform the messages to match the schema
    chat_responses = [
        schem.ChatMessageResponse(
            id = message.id,
            user_id=user.id,
            user_message=message.content,
            bot_response=message.bot_response,
            date_created=dt.datetime.now()
        )
        for message in messages
    ]
    return chat_responses


@app.get("/api/messages/{message_id}", status_code=200)
async def get_message(
        message_id: int,
        user: schem.User = fapi.Depends(sett.get_current_user),
        db: orm.Session = fapi.Depends(sett.get_db),
):
    message = await sett.get_message(message_id, user, db)
    return message


@app.delete("/api/messages/{message_id}", status_code=204)
async def delete_message(
        message_id: int,
        user: schem.User = fapi.Depends(sett.get_current_user),
        db: orm.Session = fapi.Depends(sett.get_db),
):
    await sett.delete_message(message_id, user, db)
    return {"message", "Successfully deleted"}


