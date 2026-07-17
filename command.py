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

async def create_trusted_certificate(to_what_address):
    path_to_saved_trusted_certificate_directory = Path(f'{Path(__file__).resolve().parent}' + r'\Saved_Trusted_Certificate')
    path_to_saved_trusted_certificate_directory.mkdir(parents=True, exist_ok=True)
    clean_address = ''.join(needed_symbol for needed_symbol in to_what_address if needed_symbol.isalnum())
    needed_certfile = str(path_to_saved_trusted_certificate_directory) + fr'\{clean_address}.crt'
    needed_keyfile = str(path_to_saved_trusted_certificate_directory) + fr'\{clean_address}.key'
    if Path(needed_certfile).is_file() and Path(needed_keyfile).is_file():
        return needed_certfile,needed_keyfile
    else:
        path_to_openssl_directory = await found_openssl_directory()
        if path_to_openssl_directory:
            openssl_process = await asyncio.create_subprocess_exec(fr"{path_to_openssl_directory}\openssl.exe",'genrsa','-out',fr"{path_to_saved_trusted_certificate_directory}\{clean_address}.key",'2048')
            await openssl_process.wait()
            openssl_process = await asyncio.create_subprocess_exec(fr"{path_to_openssl_directory}\openssl.exe",'req','-new','-key',fr"{path_to_saved_trusted_certificate_directory}\{clean_address}.key",'-out',fr"{path_to_saved_trusted_certificate_directory}\{clean_address}.csr",'-subj',f'/CN={clean_address}','-config',fr"{path_to_saved_trusted_certificate_directory}\config_for_certification_center.txt")
            await openssl_process.wait()
            openssl_process = await asyncio.create_subprocess_exec(fr"{path_to_openssl_directory}\openssl.exe",'x509','-req','-in',fr"{path_to_saved_trusted_certificate_directory}\{clean_address}.csr",'-CA',fr"{path_to_saved_trusted_certificate_directory}\root_for_certification_center.crt",'-CAkey',fr"{path_to_saved_trusted_certificate_directory}\root_for_certification_center.key",'-CAcreateserial','-out',fr"{path_to_saved_trusted_certificate_directory}\{clean_address}.crt",'-days','365','-sha256')
            await openssl_process.wait()
            return needed_certfile,needed_keyfile
        else:
            powershell_process = await asyncio.create_subprocess_shell(cmd="powershell -NoLogo -NoExit",stdin = asyncio.subprocess.PIPE,stdout = asyncio.subprocess.PIPE)
            powershell_process.stdin.write('winget install ShiningLight.OpenSSL.Light --source winget\n'.encode(encoding='utf-8'))
            await powershell_process.stdin.drain()
            powershell_process.stdin.write('exit\n'.encode(encoding='utf-8'))
            await powershell_process.stdin.drain()
            await powershell_process.wait()
            path_to_openssl_directory = await found_openssl_directory()
            openssl_process = await asyncio.create_subprocess_exec(fr"{path_to_openssl_directory}\openssl.exe",'genrsa','-out',fr"{path_to_saved_trusted_certificate_directory}\root_for_certification_center.key",'2048')
            await openssl_process.wait()
            openssl_process = await asyncio.create_subprocess_exec(fr"{path_to_openssl_directory}\openssl.exe",'req','-x509','-new','-nodes','-key',fr"{path_to_saved_trusted_certificate_directory}\root_for_certification_center.key",'-sha256','-days','36500','-out',fr"{path_to_saved_trusted_certificate_directory}\root_for_certification_center.crt",'-subj',fr'/C=US/ST=Washington/L=Washington/O=TUCFCS/CN=Trusted USA Company For Certificate Signatures')
            await openssl_process.wait()
            with open(file = r'G:\Programming\MyApps\UP\Saved_Trusted_Certificate\config_for_certification_center.txt',mode = 'w',encoding = 'utf-8') as file:
                file.write('[req]\ndistinguished_name=req_distinguished_name\nx509_extensions=v3_ca\n\n[req_distinguished_name]\n\n[v3_ca]\nbasicConstraints = critical,CA:TRUE\nkeyUsage = critical,keyCertSign,cRLSign\nsubjectKeyIdentifier = hash\nauthorityKeyIdentifier = keyid:always,issuer')
            openssl_process = await asyncio.create_subprocess_exec(fr"{path_to_openssl_directory}\openssl.exe",'req','-x509','-new','-nodes','-key',fr"{path_to_saved_trusted_certificate_directory}\root_for_certification_center.key",'-days','36500','-out',fr"{path_to_saved_trusted_certificate_directory}\root_for_certification_center.crt",'-config',fr"{path_to_saved_trusted_certificate_directory}\config_for_certification_center.txt",'-subj','/CN=Trusted USA Company For Certificate Signatures')
            await openssl_process.wait()
            return await create_trusted_certificate(to_what_address = to_what_address)

asyncio.run(create_trusted_certificate('youtube.com'))