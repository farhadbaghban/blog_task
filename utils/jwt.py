from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from schemas.auth_schema import TokenData, TokenResponseSchema
from typing import Annotated
from fastapi import Header

from config.jwtconfig import (
    JWT_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
)
from _exceptions import ExpireToken, HeaderNotFound, ValidationToken


class JWTHandler:
    @classmethod
    def generate_token(self, username: str) -> TokenResponseSchema:
        expire_access = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_to_encode = {"username": username, "exp": expire_access}
        encode_access = jwt.encode(
            access_to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM
        )
        return TokenResponseSchema(access=encode_access)

    @classmethod
    def verify_token(self, auth_token: Annotated[str, Header()]) -> TokenData:
        if not auth_token:
            raise HeaderNotFound
        try:
            token_data = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

            token_exp_timestamp = token_data["exp"]
            token_exp_datetime = datetime.fromtimestamp(
                token_exp_timestamp, timezone.utc
            )
            current_datetime_utc = datetime.now(timezone.utc)
            if token_exp_datetime < current_datetime_utc:
                raise ExpireToken
        except JWTError:
            raise ValidationToken

        return TokenData(**token_data)
