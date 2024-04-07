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
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "user with this username and password not found!"


class IsNotYours(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "this post or comment is not your's"


class PostNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "post not found"


class CommentNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "post not found"
