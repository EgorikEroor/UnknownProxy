import asyncio

async def create_trusted_certificate(to_what_address):

async def run_powershell():
    process = await asyncio.create_subprocess_shell(cmd = "powershell -NoLogo -NoExit",stdin = asyncio.subprocess.PIPE,stdout = asyncio.subprocess.PIPE)
    process.stdin.write('winget list openssl\n__END__\n'.encode(encoding = 'utf-8'))
    await process.stdin.drain()
    while True:
        answer = (await process.stdout.readline()).decode(encoding = 'utf-8').rstrip()
        if 'OpenSSL' in answer:
            process.stdin.write(''.encode(encoding = 'utf-8'))
        if answer == '__END__':
            break
    process.stdin.write('winget install ShiningLight.OpenSSL.Light --source winget'.encode(encoding = 'utf-8'))
    await process.stdin.drain()
    await process.wait()
    process.stdin.write('exit'.encode(encoding = 'utf-8'))
    await process.stdin.drain()
    await process.wait()

asyncio.run(run_powershell())