# Python modile
import datetime
import jwt
from datetime import datetime as dt, timezone

# Fastapi module
from fastapi import HTTPException, status
from sqlmodel import select

# Custom import
from database.connection import get_config
from database.db_connection import SessionDep
from auth.schema import Users



# Token Life
EXPIRY_DELTA = 100 * 60

# algorithm
algorithm = "HS256"


# Token Operations
class TokenOperation(object):

    def __init__(self, user: object = False):
        self.user = user

    @property
    def get_token(self) -> str:
        configure = get_config()
        payload = {
            "id": self.user.id,
            "name": self.user.email,
            "exp": dt.now(timezone.utc) + datetime.timedelta(seconds=EXPIRY_DELTA)
        }
        return jwt.encode(payload, configure['secret_key'], algorithm=algorithm)

    @staticmethod
    def _verify_token(token, db:SessionDep):
        configure = get_config()
        try:
            decode_token = jwt.decode(
                token, configure['secret_key'], algorithms=[algorithm])
            if all(decode_token.values()) is False:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorize Access")
            return db.exec(select(Users).where(Users.id == decode_token.get('id'))).one_or_none()
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=400, detail="Signature Expired")
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401, detail="Invalid Token")
