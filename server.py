import asyncio

from config import ENCODING
from parse_message import parse_client_request


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
        encoding_name_name = parsed_request[2]
        request_body = parsed_request[3]

    sample_answer = "НИНАШОЛ РКСОК/1.0"
    print(f"Send: {message!r}")
    # print(data)
    writer.write(data)
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