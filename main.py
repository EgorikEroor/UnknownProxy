import asyncio

async def listen_socket_data(reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
    client_data_request = await reader.readuntil(separator = b'\r\n\r\n')
    request_information = {}
    request_information['Request_method'],request_information['Request_address'],_ = client_data_request.decode('utf-8').strip().split(sep = '\r\n')[0].split(sep = ' ',maxsplit = 2)
    request_information['Request_host'],request_information['Request_port'] = request_information['Request_address'].split(sep = ':',maxsplit= 1)
    server_reader,server_write = await asyncio.open_connection(host=request_information['Request_host'],port=request_information['Request_port'])
    client_reader,client_writer = await asyncio.open_connection(host = '127.0.0.1',port = 8080)
    server_write.write(client_data_request)
    server_data_response = await server_reader.readuntil(separator = b'\r\n\r\n')
    client_writer.write(server_data_response)

async def run_unknown_proxy():
    listen_socket = await asyncio.start_server(client_connected_cb = listen_socket_data,host = '127.0.0.1',port = 8080)
    await listen_socket.serve_forever()

asyncio.run(run_unknown_proxy())
