import datetime as dt
import pydantic as pyd

class UserBase(pyd.BaseModel):
    email: str

class UserCreate(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True


class ChatMessageCreate(pyd.BaseModel):
    content: str


class ChatMessageResponse(pyd.BaseModel):
    id: int
    user_id: int
    user_message: str
    bot_response: str
    date_created: dt.datetime

    class Config:
        orm_mode = True