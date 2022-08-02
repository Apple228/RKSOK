import asyncio
import logging
import sys
from asyncore import read, write

from _socket import close

from config import ENCODING, RequestVerb, ResponseStatus
from db_api import get_user, add_new_user, delete_user
from exceptions import NotSpecifiedIPOrPortError, process_critical_exception
from parse_message import parse_client_request, forms_response_to_client
from validation import validation_server_request


async def handler_client_request(reader: {read},
                                 writer: {write, close}):
    """Handler for processing the request and response to the client
        Arguments:
            reader: a stream to receive any data from the client.
            writer: A stream for sending parsed and processed client data.
    """
    data = b''
    while True:
        line = await reader.read(1024)
        data += line
        if data.endswith(b'\r\n\r\n') or not line:
            break
    message = data.decode(ENCODING)
    addr = writer.get_extra_info('peername')
    logging.info(f"Received {message!r} from {addr!r}")
    print(f"Received {message!r} from {addr!r}")

    parsed_request = parse_client_request(message)

    if parsed_request:
        requested_verb = parsed_request[0]
        name = parsed_request[1]
        request_body = parsed_request[2]
        validation_server_response = await validation_server_request(message)
        if validation_server_response.startswith(ResponseStatus.APPROVED.value):  # сервер проверки вернул true:
            if requested_verb == RequestVerb.GET:
                processed_client_request = await get_user(name)
            elif requested_verb == RequestVerb.WRITE:
                processed_client_request = await add_new_user(request_body, name)
            elif requested_verb == RequestVerb.DELETE:
                processed_client_request = await delete_user(name)
            response_to_client = forms_response_to_client(processed_client_request)
        else:
            response_to_client = validation_server_response
    else:  # Not correct request from client.
        response_to_client = forms_response_to_client(ResponseStatus.INCORRECT_REQUEST)

    print(f"Send: {response_to_client!r}")

    writer.write(f"{response_to_client}".encode(ENCODING))
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    """
    main function starts the server
    """
    try:
        server = await asyncio.start_server(
            handler_client_request, sys.argv[1], int(sys.argv[2]))
    except NotSpecifiedIPOrPortError:
        process_critical_exception(
            "Упс! Меня запускать надо так:\n\n"
            "python server.py SERVER PORT\n\n"
            "где SERVER и PORT — это домен и порт РКСОР сервера, "
            "на котором сервер должен запуститься. Например:\n\n"
            "python server.py my-rksok-server.ru 5555\n")

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
