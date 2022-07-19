from typing import Union

from config import ResponseStatus, PROTOCOL


async def get_user(name: str, encoded_name: str) -> Union[ResponseStatus, tuple]:
    print(f'Ищю {name}')
    user = ('name', '123')
    print(ResponseStatus.OK.value+PROTOCOL)

    return ResponseStatus.OK, user
