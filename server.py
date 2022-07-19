import asyncio

from config import ENCODING, RequestVerb
from db_api import get_user, add_new_user
from parse_message import parse_client_request, forms_response_to_client


async def handler_client_request(reader, writer):
    data = b''
    while True:
        line = await reader.read(1024)
        data += line
        if data.endswith(b'\r\n\r\n') or not line:
            break
    message = data.decode(ENCODING)
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r}")

    parsed_request = parse_client_request(message)


    if parsed_request:
        requested_verb = parsed_request[0]
        name = parsed_request[1]
        request_body = parsed_request[2]
        if True:  # сервер проверки вернул true:
            if requested_verb == RequestVerb.GET:
                processed_client_request = await get_user(name)
            elif requested_verb == RequestVerb.WRITE:
                processed_client_request = await add_new_user(request_body, name)
            # elif requested_verb == RequestVerb.DELETE:
            #     processed_client_request = await delete_user(name, encoding_name)
            response_to_client = forms_response_to_client(processed_client_request)



    print(f"Send: {response_to_client!r}")

    writer.write(response_to_client.encode(ENCODING))
    await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handler_client_request, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())