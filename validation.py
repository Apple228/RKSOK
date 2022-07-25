import asyncio

from config import VALIDATION_SERVER_PORT, VALIDATION_SERVER_URL, PROTOCOL, ENCODING


async def validation_server_request(message: str) -> str:
    reader, writer = await asyncio.open_connection(
        VALIDATION_SERVER_URL, VALIDATION_SERVER_PORT
    )
    request = f"АМОЖНА? {PROTOCOL}\r\n{message}\r\n\r\n".encode(ENCODING)
    writer.write(request)
    await writer.drain()
    response = b''
    while True:  # reading all data from validation server by 1kb blocks
        line = await reader.read(1024)
        response += line
        if response.endswith(b'\r\n\r\n') or not line:
            break
    writer.close()
    await writer.wait_closed()
    print(f'\nREQUEST_TO_VALIDATION_SERVER:\n{request}')
    print(f'\nRESPONSE_FROM_VALIDATION_SERVER:\n{response.decode(ENCODING)}')

    return response.decode(ENCODING)