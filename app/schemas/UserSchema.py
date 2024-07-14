from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    role: str
    password: str