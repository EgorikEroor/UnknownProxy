import asyncio

async def listen_socket_data(reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
    address = writer.get_extra_info(name = 'peername')
    client_data_request = b''
    while True:
        client_data_getting_request = await reader.read(4096)
        if not client_data_getting_request:
            break
        client_data_request += client_data_getting_request
        if b'\r\n\r\n' in client_data_request:
            break
    client_data_request = client_data_request.decode('utf-8').strip().split(sep = '\r\n')
    request_information = {}
    request_information['Request_method'],request_information['Request_address'],_ = client_data_request[0].split(sep = ' ',maxsplit = 2)
    request_information['Request_host'],request_information['Request_port'] = request_information['Request_address'].split(sep = ':',maxsplit= 1)
    server_socket = await asyncio.open_connection(host=request_information['Request_host'],port=request_information['Request_port'])
async def run_unknown_proxy():
    listen_socket = await asyncio.start_server(client_connected_cb=listen_socket_data,host='0.0.0.0',port='8080')
    await listen_socket.serve_forever()
asyncio.run(run_unknown_proxy())
