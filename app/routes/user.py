from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    Hash the password.
    """
    try:
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    return new_user


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Update an existing user.
    """
    user_query = db.query(models.User).filter(models.User.id == id)
    user_to_update = user_query.first()
    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Get a user by id.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
