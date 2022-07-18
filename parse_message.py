from base64 import b64encode
from typing import Optional

from config import PROTOCOL, RequestVerb, ENCODING


def make_uniq_id(user_name: str) -> str:
    """Make uniq user name id for database file.
    Args:
        user_name (str): user name from request.
    Returns
        (str): encoded user name id.
    """
    encoded_uniq_name = b64encode(user_name.encode(ENCODING)).decode(ENCODING)
    return encoded_uniq_name

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
    if len(take_name(message))>30:
        return None
    if message.split('\r\n', 1)[0].rsplit(' ',1)[1] != PROTOCOL:
        return None

    for verb in RequestVerb:
        if message.startswith(verb.value):
            name = take_name(message)
            encoded_name = make_uniq_id(name)
            request_body = ''.join(message.split('\r\n', 1)[1])
            break  # If found existing request verb.
    else:
        return None
    return (verb, name, encoded_name, request_body)

