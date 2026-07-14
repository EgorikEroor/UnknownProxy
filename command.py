import asyncio
from pathlib import Path
import string

async def found_openssl_directory():
    for disk_letter in list(string.ascii_uppercase):
        if Path(fr'{disk_letter}:\Program Files\OpenSSL-Win64\bin').is_dir():
            return Path(fr'{disk_letter}:\Program Files\OpenSSL-Win64\bin')
    for disk_letter in list(string.ascii_uppercase):
        if Path(fr'{disk_letter}:\Program Files\OpenSSL-Win32\bin').is_dir():
            return Path(fr'{disk_letter}:\Program Files\OpenSSL-Win32\bin')
    return None

async def run_powershell(to_what_address):
    file_directory = Path(f'{Path(__file__).resolve().parent}' + r'\Saved_Trusted_Certificate')
    file_directory.mkdir(parents=True, exist_ok=True)
    clean_address = ''.join(needed_symbol for needed_symbol in to_what_address if needed_symbol.isalnum())
    needed_certfile = str(file_directory) + fr'\{clean_address}.crt'
    needed_keyfile = str(file_directory) + fr'\{clean_address}.key'
    if Path(needed_certfile).is_file() and Path(needed_keyfile).is_file():
        return needed_certfile,needed_keyfile
    else:
        path_to_openssl_directory = await found_openssl_directory()
        if path_to_openssl_directory:
            openssl_process = await asyncio.create_subprocess_exec(fr"{path_to_openssl_directory}\openssl.exe",'req','-x509','-newkey','rsa:2048','-nodes','-keyout',fr"{file_directory}\{clean_address}.key",'-out',fr"{file_directory}\{clean_address}.crt",'-days','365','-subj',f'/CN={to_what_address}')
            await openssl_process.wait()
            return needed_certfile,needed_keyfile
        else:
            powershell_process = await asyncio.create_subprocess_shell(cmd="powershell -NoLogo -NoExit",stdin = asyncio.subprocess.PIPE,stdout = asyncio.subprocess.PIPE)
            powershell_process.stdin.write('winget install ShiningLight.OpenSSL.Light --source winget\n'.encode(encoding='utf-8'))
            await powershell_process.stdin.drain()
            powershell_process.stdin.write('exit\n'.encode(encoding='utf-8'))
            await powershell_process.stdin.drain()
            await powershell_process.wait()
            return await run_powershell(to_what_address = to_what_address)

asyncio.run(run_powershell('google.com'))