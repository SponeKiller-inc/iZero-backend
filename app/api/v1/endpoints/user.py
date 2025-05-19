from fastapi import APIRouter, Response, Depends, HTTPException, status
from sqlalchemy.orm import Session


from ..schemas import user as schema
from app.database.session import get_db
from app.models.users import Users
from app.utils import utils



router = APIRouter(prefix="/users", tags=["authentications"])

@router.post("/local", status_code=status.HTTP_201_CREATED)
async def register(
    user: schema.LocalRegistrationIn,
    db: Session = Depends(get_db)
):
    
    # Verify existance user in db
    retrieved_user = db.query(Users).filter(
        Users.email == user.email
    ).first()
    
    if retrieved_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    
    # Insert new user to db
    new_user = Users(
        email=user.email,
        password=utils.hash_password(user.password),
    )
    
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    
    if new_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later"
        )

@router.post("/google", status_code=status.HTTP_201_CREATED)
async def register(response: Response,
                   user: schema.UserRegisterIn,
                   db: Session = Depends(get_db)):
    
    
    retrieved_user = db.query(Users).filter(
        Users.email == user.email
    ).first()
    
    if retrieved_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")
    
    new_user = Users(
        email=user.email,
        password=pwd_context.hash(user.password),
    )
    
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    