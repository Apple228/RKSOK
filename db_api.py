from typing import Union

import aiofiles
from aiofiles.os import remove

from config import ResponseStatus, PROTOCOL


async def get_user(name: str) -> Union[ResponseStatus, tuple]:
    print(f'Ищю {name}')
    user = ('name', '123')
    print(ResponseStatus.OK.value+PROTOCOL)
    try:
        async with aiofiles.open(f"db/{name}", 'r', encoding='utf-8') as file:
            user = await file.read()
        return (ResponseStatus.OK, user)
    except (FileExistsError, FileNotFoundError, OSError):
        return ResponseStatus.NOTFOUND


async def add_new_user(request_body, name) ->ResponseStatus:
    try:
        async with aiofiles.open(f'db/{name}', 'x', encoding='utf-8') as file:
            await file.write(request_body)
        return ResponseStatus.OK
    except FileExistsError:
        async with aiofiles.open(f"db/{name}", 'w', encoding='utf-8') as file:
            await file.write(request_body)
        return ResponseStatus.OK


async def delete_user(name: str) -> ResponseStatus:
    try:
        await remove(f"db/{name}")
        return ResponseStatus.OK
    except (FileExistsError, FileNotFoundError):
        return ResponseStatus.NOTFOUND



