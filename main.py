import asyncio,ssl

async def listen_socket_data(client_reader:asyncio.StreamReader,client_writer:asyncio.StreamWriter):
    client_data_request = await client_reader.readuntil(separator = b'\r\n\r\n')
    request_information = {}
    request_information['Request_method'],request_information['Request_address'],_ = client_data_request.decode('utf-8').strip().split(sep = '\r\n')[0].split(sep = ' ',maxsplit = 2)
    request_information['Request_host'],request_information['Request_port'] = request_information['Request_address'].split(sep = ':',maxsplit= 1)
    server_reader,server_writer = await asyncio.open_connection(host=request_information['Request_host'],port=request_information['Request_port'])
    if request_information['Request_method'] == 'CONNECT':
        client_writer.write('HTTP/1.1 200 Connection Established\r\n\r\n'.encode('utf-8'))
        client_context = ssl.create_default_context()
        server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        server_context.load_cert_chain(certfile = r'G:\Programming\Git\ca.crt',keyfile = r'G:\Programming\Git\ca.key')
        await client_writer.start_tls(sslcontext = server_context)
        await server_writer.start_tls(sslcontext = client_context,server_hostname = request_information['Request_host'])
        async def transmission_decrypted_data(reader_deciphered,writer_deciphered):
            while True:
                data_deciphered = await reader_deciphered.readuntil(separator = b'\r\n\r\n')
                if not data_deciphered:
                    break
                print(data_deciphered)
                writer_deciphered.write(data_deciphered)
                await server_writer.drain()
        await asyncio.gather(transmission_decrypted_data(reader_deciphered = client_reader,writer_deciphered= server_writer),transmission_decrypted_data(reader_deciphered= server_reader,writer_deciphered = client_writer))
    else:
        server_writer.write(client_data_request)
        server_data_response = await server_reader.readuntil(separator = b'\r\n\r\n')
        client_writer.write(server_data_response)

async def run_unknown_proxy():
    listen_socket = await asyncio.start_server(client_connected_cb = listen_socket_data,host = '127.0.0.1',port = 8080)
    await listen_socket.serve_forever()

asyncio.run(run_unknown_proxy())
