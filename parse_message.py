from base64 import b64encode

from typing import Optional, Union

from config import PROTOCOL, RequestVerb, ENCODING, ResponseStatus



def take_name(message: str) -> str:
    """take requestet user name from message from client.
    Args:
        message (str): message from client.
    Returns:
        (str): cutted name.
    """
    name = message.split('\r\n', 1)[0].rsplit(' ', 1)[0].split(' ', 1)[1]
    return name


def parse_client_request(message: str) -> Optional[tuple]:
    if not ' ' in message:
        return None
    if len(take_name(message)) > 30:
        return None
    if message.split('\r\n', 1)[0].rsplit(' ', 1)[1] != PROTOCOL:
        return None

    for verb in RequestVerb:
        if message.split()[0] == verb.value:
            name = take_name(message)
            request_body = ''.join(message.split('\r\n', 1)[1])
            break  # If found existing request verb.
    else:
        return None
    return (verb, name, request_body)


def forms_response_to_client(response: Union[ResponseStatus, tuple]) -> str:
    if type(response) is tuple:
        status, user_data = response
        return f"{status.value} {PROTOCOL}\r\n{user_data}\r\n\r\n"
    return f'{response.value} {PROTOCOL}\r\n\r\n'
