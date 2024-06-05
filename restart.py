import subprocess
import time
import os


# Function to get the PID of a process by its command
def get_pid(command):
    try:
        cmd = 'pgrep -f "{}"'.format(command)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        pids = result.stdout.decode('utf-8').strip().split("\n")
        return pids
    except subprocess.CalledProcessError:
        return None

while(True):
    old_pids = get_pid("python3 controller_tg.py")
    # print("IDs :",old_pids)
    if(old_pids and len(old_pids) == 1):
        try:
            # Start the new process in a detached mode
            cmd = "nohup python3 controller_tg.py &"
            new_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, close_fds=True)
            new_pid = new_process.pid
            print("New process started successfully with PID:", new_pid)
        except Exception as e:
            print("Error starting new process:", str(e))
    time.sleep(1)
    if os.path.exists("/home/ubuntu/kill.txt"):
        try:
            os.remove("/home/ubuntu/kill.txt")
        except Exception as e:
            print("Error deleting file:", str(e))
        try:
            # Start the new process in a detached mode
            cmd = 'pkill -f "python3 controller_tg.py"'
            new_process = subprocess.Popen(cmd, shell=True)
            print("Telegram Bot Killed")
        except Exception as e:
            print("Error killing process:", str(e))