from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

