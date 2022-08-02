import logging
from typing import Union

import aiofiles
from aiofiles.os import remove

from config import ResponseStatus, PROTOCOL


async def get_user(name: str) -> Union[ResponseStatus, tuple]:
    """
    Search for a user in the database

     Args:
         name(str): Name from client request.
    Returns:
          Union[ResponsePhrase, tuple]: ResponseStatus OK
          and user_data from file or ResponseStatus NOTFOUND.

    """
    print(f'Ищю {name}')
    print(ResponseStatus.OK.value+PROTOCOL)
    try:
        async with aiofiles.open(f"db/{name}", 'r', encoding='utf-8') as file:
            user = await file.read()
        return (ResponseStatus.OK, user)
    except (FileExistsError, FileNotFoundError, OSError):
        return ResponseStatus.NOTFOUND


async def add_new_user(request_body: str, name: str) ->ResponseStatus:
    """
        Add new user in the database

     Args:
        request_body(str): Body data from client response.
        name(str): Name from client request.
     Returns:
         ResponseStatus OK

    """
    try:
        async with aiofiles.open(f'db/{name}', 'x', encoding='utf-8') as file:
            await file.write(request_body)
        return ResponseStatus.OK
    except FileExistsError:
        async with aiofiles.open(f"db/{name}", 'w', encoding='utf-8') as file:
            await file.write(request_body)
        return ResponseStatus.OK


async def delete_user(name: str) -> ResponseStatus:
    """
    Delete user from database

    Args:
        name(str):  name(str): Name from client request.
    Returns:
        ResponseStatus OK or NOTFOUND
    """
    try:
        await remove(f"db/{name}")
        return ResponseStatus.OK
    except (FileExistsError, FileNotFoundError):
        return ResponseStatus.NOTFOUND



