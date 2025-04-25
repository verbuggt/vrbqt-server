import string

from fastapi import HTTPException
from starlette import status

EXTENDED_CHARACTERS = string.ascii_letters + string.digits + "-_."


# TODO replace with C lib for speed?
def validate_string(user_input: str, max_length: int, allowed_characters: str, extended: bool) -> bool:
    if not user_input:
        return False
    if extended:
        allowed_characters += EXTENDED_CHARACTERS
    if len(user_input) > max_length:
        return False
    for char in user_input:
        if char not in allowed_characters:
            return False
    return True


def validate(repository_name: str, max_length: int = 128, extended: bool = False) -> None:
    if not validate_string(user_input=repository_name, max_length=max_length, allowed_characters=string.ascii_letters + string.digits, extended=extended):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation Error")
    return
