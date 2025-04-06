from auth.schema_validation import LoginUser, Create_User_request, ResetPassword
from auth.schema import Users
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Request
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database.db_connection import SessionDep
from auth.token import TokenOperation
from pydantic import EmailStr


router = APIRouter(prefix="/auth", tags=["Login"])
bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup", summary="Api Homepage", status_code=status.HTTP_200_OK)
async def home(user_request: Create_User_request, db: SessionDep):
    new_user = Users(name=user_request.name, email=user_request.email,
                     password=bycrypt_context.hash(user_request.password))
    db.add(new_user)
    try:
        db.commit()  # ✅ Attempt to commit the transaction
        db.refresh(new_user)  # ✅ Ensure the object is updated
        return {"message": "User created successfully", "user": new_user.email}

    except IntegrityError:
        db.rollback()  # ❌ Rollback transaction on integrity error (e.g., duplicate email)
        raise HTTPException(
            status_code=400, detail="User with this email already exists")

    except SQLAlchemyError as e:
        db.rollback()  # ❌ Rollback on general DB errors
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@router.post("/login")
def login(creds: LoginUser, db: SessionDep):
    def _verify_password(password, user_data):
        return bycrypt_context.verify(password, user_data.password)
    response = False
    user_data = db.exec(select(Users).where(Users.email == creds.email)).one_or_none()
    if user_data:
        is_verified = _verify_password(creds.password, user_data)
        if is_verified:
            token = TokenOperation(user_data)
            response = {'token': token.get_token, 'description': "JWT Token"}
        else:
            return HTTPException(
                status_code=401, detail="Unauthorize")

    else:
        raise HTTPException(status_code=404, detail="User not found")
    return response


@router.put("/reset/password", summary="Reset Password")
async def reset_password(creds: ResetPassword, db: SessionDep, request:Request):
    user_data = db.exec(select(Users).where(Users.email == creds.email)).one()
    if user_data:
        return {
            "message":"Generate new password using link",
            "url": f"{str(request.base_url)}auth/new/password?email={user_data.email}&new_password=''"
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.get("/new/password", summary="New Password")
async def new_password(db: SessionDep, email: EmailStr, new_password):
    if not email or not new_password:
        raise HTTPException(status_code=404, detail="Required field missing") 
    user_data = db.exec(select(Users).where(Users.email == email)).one_or_none()
    if user_data:
        user_data.password=bycrypt_context.hash(new_password)
        db.commit()  # ✅ Attempt to commit the transaction
        db.refresh(user_data)  # ✅ Ensure the object is updated
        return {"message": "Password update successfully", "user": user_data.email}
    else:
        raise HTTPException(status_code=404, detail="User not found")