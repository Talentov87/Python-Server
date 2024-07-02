import sys
sys.PORT_NUMBER = 7777

import functions.sql.py_host.log as Logger

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import base64
import threading

import functions.Executor.exe as Exe

app = FastAPI()

TIME_OUT = 3 #seconds

# Allowing CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RootPath = "G:/Python/ServerHosting/MAIN"
RootPath = "/home/ubuntu/serverHost/MAIN"

SECRET_KEY = b"JAY23_Vt-GcUJ0JKNUglyO7gCuK_87MK"
valid_keys = ['JY6odVt-GcUJ0JKNUglyO7gCuKO_4T1FZR8rIKznZpg']

# Function to encrypt data using AES
def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted_data).decode('utf-8')

# Function to decrypt data using AES
def decrypt_aes(encrypted_data, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
        decrypted_data = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
        return True,decrypted_data.decode('utf-8')
    except UnicodeDecodeError:
        return False,None

# Function to check authentication
def authenticate(request: Request):
    encrypted_key = request.headers.get('X-Encrypted-Key')

    if not encrypted_key:
        raise HTTPException(status_code=401, detail="Unauthorized: X-Encrypted-Key header is missing")

    can_decrypt,decrypted_key = decrypt_aes(encrypted_key, SECRET_KEY)

    if(can_decrypt == False):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid key")

    if decrypted_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid key")

sys.SharedMemory = {}
sys.SharedMemory["Modules"] = {}

# Function to call function from the given module path
def call_function_from_path(module_path, function, method, request_body, storeLog = False):
    try:
        if(not function.endswith("_api")):
            function = function+"_api"
        
        if method == 'GET' or method == 'POST':
            
            if(storeLog):
                response_body,TimeDurationData = Exe.run_python_with_restrictions(module_path,function,TIME_OUT,method,request_body)
                threading.Thread(target=Logger.store_execution_log,args=(module_path,function,request_body,response_body,TimeDurationData)).start()
            else:
                response_body,TimeDurationData = Exe.run_python_with_restrictions(module_path,function,10,method,request_body)
            return response_body
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except (ImportError, AttributeError) as e:
        return (str(e)+" - At call_function_from_path")

@app.get("/")
@app.post("/")
def version():
    return "Hello World! from jay telegram bot service"

import asyncio
@app.get("/{path:path}")
@app.post("/{path:path}")
async def dynamic_route(path: str, request: Request):
    # authenticate(request)
    loop = asyncio.get_event_loop()
    
    parts = path.split('/')

    if len(parts) < 3:
        raise HTTPException(status_code=404)

    isApiForService = False
    if(parts[0] == "service"):
        parts = parts[1:]
        isApiForService = True

    package = '/'.join(parts[:-1])
    module_path = RootPath+"/Users/"+package+".py"
    #G:/Python/ServerHosting/MAIN/Users/userid/modulename

    function = parts[-1]
    method = request.method
    try:
        data = await request.json() if method == 'POST' else None
    except:
        data = (await request.body()).decode('utf-8') if method == 'POST' else None

    # result = call_function_from_path(module_path, function, method, data)
    if(isApiForService):
        result = await loop.run_in_executor(None, call_function_from_path, module_path, function, method, data, True)
    else:
        # authenticate(request)
        module_path = "/home/ubuntu/MAIN/functions/sql/"+package+".py"
        result = await loop.run_in_executor(None, call_function_from_path, module_path, function, method, data, False)
        
    return Response(content=result, media_type="application/json")


def run(app,port):
    import sys
    is_live = "ubuntu" in sys.argv[0]
    if is_live:
        # Change the working directory
        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port, ssl_keyfile="/home/ubuntu/MAIN/privkey.pem", ssl_certfile="/home/ubuntu/MAIN/fullchain.pem")
    else:
        # Change the working directory
        # Exe.original_chdir('G:/Python/ServerHosting/MAIN')

        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port)

if __name__ == "__main__":
    run("server_host",sys.PORT_NUMBER)