from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import auth
import throttling
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Registration + Throttling Handling",
        "description": "Operations with registration users. The **login and throttling** logic is also here.",
    }
]

app = FastAPI(title="FastApi Throttling", openapi_tags=tags_metadata)

# Register a new account.
@app.post("/register",
response_model=schemas.UserResponse,
    responses={
        400: {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"detail": "Email already registered"}}},
        }
    }, tags=["Registration + Throttling Handling"]
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # verify the existing Email.
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    hashed_password = auth.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}


@app.post(
    "/login",
    response_model=schemas.Token,
    responses={
        401: {
            "description": "Unauthorized",
            "content": {"application/json": {"example": {"detail": "Invalid credentials"}}},
        },
        429: {
            "description": "Too Many Requests",
            "content": {"application/json": {"example": {"detail": "Too many failed attempts. Try again later."}}},
        },
    }, tags=["Registration + Throttling Handling"]
)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check for throttling
    if throttling.is_throttled(user.email):
        raise HTTPException(
            status_code=429,  # Too Many Requests
            detail="Too many failed attempts. Try again later."
        )
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        throttling.log_failed_attempt(user.email)  # Log the failed attempt
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Reset failed attempts on successful login
    throttling.reset_attempts(user.email)
    
    access_token = auth.create_access_token(data={"email": db_user.email, "id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

