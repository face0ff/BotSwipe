from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str
    user_id: int
    refresh_token: str
    access_token: str