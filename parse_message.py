from base64 import b64encode

from typing import Optional, Union

from config import PROTOCOL, RequestVerb, ENCODING, ResponseStatus


def _take_name(message: str) -> str:
    """take requestet user name from message from client.
    Args:
        message (str): message from client.
    Returns:
        (str):  user name.
    """
    name = message.split('\r\n', 1)[0].rsplit(' ', 1)[0].split(' ', 1)[1]
    return name


def parse_client_request(message: str) -> Optional[tuple]:
    """
    Parse client request and return RequestVerb, name, request body from message
    if request correct, else None

    Args:
        message(str): user message
    Returns:
        (Optional[tuple]): verb name user request body in tuple or none
    """
    if not ' ' in message:
        return None
    if len(_take_name(message)) > 30:
        return None
    if message.split('\r\n', 1)[0].rsplit(' ', 1)[1] != PROTOCOL:
        return None

    for verb in RequestVerb:
        if message.split()[0] == verb.value:
            name = _take_name(message)
            request_body = ''.join(message.split('\r\n', 1)[1])
            break  # If found existing request verb.
    else:
        return None
    return (verb, name, request_body)


def forms_response_to_client(response: Union[ResponseStatus, tuple]) -> str:
    """
    Forms response to client with RKSOK protocol.
    Args:
        response(Union[ResponsePhrase, tuple]): ResponseStatus with user data, if they are.
    Returns:
        (str): Formed string for response to client by RKSOK protocol.
    """

    if type(response) is tuple:
        status, user_data = response
        return f"{status.value} {PROTOCOL}\r\n{user_data}\r\n\r\n"
    return f'{response.value} {PROTOCOL}\r\n\r\n'
