import asyncio

from config import ENCODING


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