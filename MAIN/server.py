from flask import Flask, abort, request
import importlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import sys

sys.SharedMemory = {}


app = Flask(__name__)
"""
up cmd
scp -i C:/Users/HP/Documents/KEYS/jay-key.pem -r D:\SERVER ec2-user@ec2-35-154-184-31.ap-south-1.compute.amazonaws.com:/home/ec2-user/SERVER

scp -i C:/Users/HP/Documents/KEYS/jay-key.pem -r D:\SERVER\functions ec2-user@ec2-35-154-184-31.ap-south-1.compute.amazonaws.com:/home/ec2-user/SERVER

"""

SECRET_KEY = b"JAY23_Vt-GcUJ0JKNUglyO7gCuK_87MK"
valid_keys = ['JY6odVt-GcUJ0JKNUglyO7gCuKO_4T1FZR8rIKznZpg']
# gAkhJbEBXzR5CVj2rngd9S1kL+FFAGeAGvkmbIx1CUpvshOXceq80P58/qAKAajz


def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted_data).decode('utf-8')


def decrypt_aes(encrypted_data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    decrypted_data = unpad(cipher.decrypt(
        base64.b64decode(encrypted_data)), AES.block_size)
    return decrypted_data.decode('utf-8')


# Function to check authentication
def authenticate(request):
    encrypted_key = request.headers.get('X-Encrypted-Key')

    if not encrypted_key:
        abort(401, "Unauthorized: X-Encrypted-Key header is missing")

    decrypted_key = decrypt_aes(encrypted_key, SECRET_KEY)

    if decrypted_key not in valid_keys:
        abort(401, "Unauthorized: Invalid key")


sys.SharedMemory["Modules"] = []

def call_function_from_path(module_path, function, method, data):
    try:
        if(module_path in sys.SharedMemory["Modules"]):
            module = sys.SharedMemory["Modules"][module_path]
        else:
            module = importlib.import_module(f'functions.{module_path}')
            sys.SharedMemory["Modules"].append(module)

        # try:
        #     module = importlib.reload(
        #         importlib.import_module(f'functions.{module_path}'))
        # except ImportError as e:
        #     module = importlib.import_module(f'functions.{module_path}')

        function_obj = getattr(module, function, None)

        if function_obj is not None and callable(function_obj):
            if method == 'GET':
                return function_obj()
            elif method == 'POST':
                return function_obj(data)
            else:
                abort(400, "Invalid method")
        else:
            abort(404)
    except (ImportError, AttributeError) as e:
        return str(e)


@app.route("/", methods=['GET', 'POST'])
def version():
    return "Hello World! from jay and hari version - 25 November 2023 12:40 AM"


@app.route("/<path:path>", methods=['GET', 'POST'])
def dynamic_route(path):
    authenticate(request)
    parts = path.split('/')

    if len(parts) < 2:
        abort(404)

    package = '.'.join(parts[:-1])
    function = parts[-1]

    method = request.method
    data = request.json if method == 'POST' else None
    return call_function_from_path(package, function, method, data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
