from fastapi import HTTPException, status


class ExpireToken(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Token expired"
        self.headers = {"WWW-Authenticate": "Bearer"}


class HeaderNotFound(HTTPException):
    def __ini__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "auth header not found."


class ValidationToken(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Could not validate credentials."
        self.headers = {"WWW-Authenticate": "Bearer"}


class UserAlreadyExists(HTTPException):
    def __init__(self) -> None:
        self.status_code = 400
        self.detail = "user alreadt exists!"


class UserNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "user with this username and password not found!"
