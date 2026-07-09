import asyncio

async def listen_socket_data(reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
    addres = writer.get_extra_info(name='peername')
    client_data_request = b''
    while True:
        client_data_getting_request = await reader.read(4096)
        if not client_data_getting_request:
            break
        client_data_request += client_data_getting_request
        if b'\r\n\r\n' in client_data_request:
            break
    print(client_data_request)

async def run_unknown_proxy():
    listen_socket = await asyncio.start_server(client_connected_cb=listen_socket_data,host='0.0.0.0',port='8080')
    await listen_socket.serve_forever()
asyncio.run(run_unknown_proxy())
