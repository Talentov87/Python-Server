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


def check_and_start_bot(file_name,kill_file_name):
    old_pids = get_pid(f"python3 {file_name}")

    print(file_name,old_pids)
    # print("IDs :",old_pids)
    if(old_pids and len(old_pids) == 1):
        try:
            # Start the new process in a detached mode
            cmd = f"nohup python3 {file_name} &"
            new_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, close_fds=True)
            new_pid = new_process.pid
            print("New process started successfully with PID:", new_pid)
        except Exception as e:
            print("Error starting new process:", str(e))
    time.sleep(1)
    if os.path.exists(f"/home/ubuntu/{kill_file_name}.txt"):
        try:
            os.remove(f"/home/ubuntu/{kill_file_name}.txt")
        except Exception as e:
            print("Error deleting file:", str(e))
        try:
            # Start the new process in a detached mode
            cmd = f'pkill -f "python3 {file_name}"'
            new_process = subprocess.Popen(cmd, shell=True)
            print("Telegram Bot Killed")
        except Exception as e:
            print("Error killing process:", str(e))

while True:
    check_and_start_bot("serverHost/bot.py","kill1")
    check_and_start_bot("controller_tg.py","kill")


# while(True):
#     old_pids = get_pid("python3 controller_tg.py")
#     # print("IDs :",old_pids)
#     if(old_pids and len(old_pids) == 1):
#         try:
#             # Start the new process in a detached mode
#             cmd = "nohup python3 controller_tg.py &"
#             new_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, close_fds=True)
#             new_pid = new_process.pid
#             print("New process started successfully with PID:", new_pid)
#         except Exception as e:
#             print("Error starting new process:", str(e))
#     time.sleep(1)
#     if os.path.exists("/home/ubuntu/kill.txt"):
#         try:
#             os.remove("/home/ubuntu/kill.txt")
#         except Exception as e:
#             print("Error deleting file:", str(e))
#         try:
#             # Start the new process in a detached mode
#             cmd = 'pkill -f "python3 controller_tg.py"'
#             new_process = subprocess.Popen(cmd, shell=True)
#             print("Telegram Bot Killed")
#         except Exception as e:
#             print("Error killing process:", str(e))