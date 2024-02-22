import subprocess
import platform
from flask import Flask, request, jsonify, render_template
import os
import sys
import zipfile

import os

# Specify the new working directory path
SERVER_working_directory = os.getcwd()+"/MAIN"

os.chdir(SERVER_working_directory)
print(os.getcwd())


app = Flask(__name__)
sys.SharedMemory = {}
sys.SharedMemory["process"] = None
sys.SharedMemory["is_process_running"] = False


def exe(cmd):
    subprocess.Popen(cmd, shell=True)

def start_server(target_file_path = "server"):
    if(sys.SharedMemory["is_process_running"]):
        print(f"Already a process is running")
        return False
    try:
        exe("gunicorn -w 4 -b 0.0.0.0:5000 server:app")
        sys.SharedMemory["is_process_running"]= True;
        return True
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        return False

def start_server1(target_file_path = "server"):
    if(sys.SharedMemory["is_process_running"]):
        print(f"Already a process is running")
        return False
    try:
        if platform.system() == "Windows":
            sys.SharedMemory["process"] = subprocess.Popen(["python", f"MAIN/{target_file_path}.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            sys.SharedMemory["process"] = subprocess.Popen(["python3", f"MAIN/{target_file_path}.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sys.SharedMemory["is_process_running"]= True;
        return True
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        return False

def stop_server():
    if sys.SharedMemory["is_process_running"]:
        try:
            exe("pkill -f \"gunicorn -w 4 -b 0.0.0.0:5000 server:app\"")
            sys.SharedMemory["is_process_running"] = False
            return True
        except Exception as e:
            print(f"Error stopping Flask app: {e}")
            return False
    else:
        return False
    
def stop_server1():
    if sys.SharedMemory["process"] and sys.SharedMemory["process"].poll() is None:
        try:
            sys.SharedMemory["process"].kill()
            sys.SharedMemory["process"].wait()
            sys.SharedMemory["process"] = None
            return True
        except Exception as e:
            print(f"Error stopping Flask app: {e}")
            return False
    else:
        return False

def extract_zip(file):
    if file:
        try:
            # if not os.path.exists('MAIN/'):
            #     os.makedirs('MAIN/')
            with zipfile.ZipFile(file, 'r') as zip_ref:
                # zip_ref.extractall('MAIN/')
                zip_ref.extractall()
            return True
        except Exception as e:
            print(f"Error extracting file: {e}")
            return False
    else:
        return False

@app.route('/start', methods=['GET'])
def start_flask_app():
    if sys.SharedMemory["process"] is None or sys.SharedMemory["process"].poll() is not None:
        return jsonify({"status": start_server()})
    else:
        return jsonify({"status": "Flask app is already running."})

@app.route('/stop', methods=['GET'])
def stop_flask_app():
    return jsonify({"status": stop_server()})

@app.route('/extract', methods=['POST'])
def extract_zip_():
    if 'file' not in request.files:
        return jsonify({"status": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "No selected file"})
    
    return jsonify({"status": extract_zip(file)})

@app.route('/restart', methods=['POST'])
def restart_server():
    log = ""
    try:
        if(stop_server()):
            log += "Stopped,"
        else:
            log += "Not In Run,"
        if(start_server()):
            log += "Started"
        else:
            log += "Failed To Start"
        return jsonify({"status": log})
    except:
        return jsonify({"status": "Error log : "+log})
    
@app.route('/code_up', methods=['POST'])
def code_up_server():
    stop_server()
    extract_status = extract_zip(request.files['file'])
    if extract_status:
        return jsonify({"status": start_server()})
    else:
        return jsonify({"status": "Error extracting file"})


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
