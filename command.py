import asyncio
from pathlib import Path

async def run_powershell(to_what_address):
    file_directory = Path(f'{Path(__file__).resolve().parent}' + '\\Saved_Trusted_Certificate')
    file_directory.mkdir(parents=True, exist_ok=True)
    clean_address = ''.join(needed_symbol for needed_symbol in to_what_address if needed_symbol.isalnum())

    process = await asyncio.create_subprocess_shell(cmd = "powershell -NoLogo -NoExit",stdin = asyncio.subprocess.PIPE,stdout = asyncio.subprocess.PIPE)
    process.stdin.write('winget install ShiningLight.OpenSSL.Light --source winget\n'.encode(encoding='utf-8'))
    await process.stdin.drain()
    process.stdin.write(f'& "C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe" req -x509 -newkey rsa:2048 -nodes -keyout {str(file_directory).replace('\\','\\\\') + '\\' + clean_address}.key -out {str(file_directory).replace('\\','\\\\') + '\\' + clean_address}.crt -days 365 -subj "/CN={to_what_address}"\n'.encode(encoding = 'utf-8'))
    await process.stdin.drain()
    process.stdin.write('exit\n'.encode(encoding = 'utf-8'))
    await process.stdin.drain()
    await process.wait()

asyncio.run(run_powershell(to_what_address = 'google.com'))