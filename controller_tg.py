TOKEN = "7107513022:AAEGIY1qKvWmF0L_h9nsznRRAR9uavykb4Y"

import time
import subprocess
import os
import sys


# from flask import Flask, jsonify, render_template

# # Import FastAPI and related dependencies
# from fastapi import FastAPI
# from flask import jsonify, render_template
# from uvicorn import Config, Server

# Shared memory for process management
sys.SharedMemory = {}
sys.SharedMemory["process"] = None
sys.SharedMemory["is_process_running"] = False


# Specify the new working directory path
if("MAIN" not in os.getcwd()):
    SERVER_working_directory = os.path.join(os.getcwd(), "MAIN")
else:
    SERVER_working_directory = os.getcwd()

os.chdir(SERVER_working_directory)

print(os.getcwd())

# Function to execute shell commands
def exe(cmd):
    subprocess.Popen(cmd, shell=True)


def get_log():
    try:
        cmd = "tail -n 20 /home/ubuntu/nohup.out"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Read the standard output and standard error
        stdout, stderr = process.communicate()
        # Print the output
        log = "\n" + stdout.decode('utf-8')
        # Print any error if occurred
        if stderr:
            log += "\nError : \n" + stderr.decode('utf-8')
        return log
    except Exception as e:
        return str(e)
    

# Function to start the FastAPI server
def start_server(whomServer="all"):
    ServerPorts = {"vellore":"50088","virar":"50087","talentov":"5000"}
    try:
        if(whomServer == "all"):
            exe("uvicorn vellore:app --host 0.0.0.0 --port 50088 --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")
            exe("uvicorn virar:app --host 0.0.0.0 --port 50087 --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")
            exe("uvicorn talentov:app --host 0.0.0.0 --port 5000 --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")    
        else:
            port = ServerPorts[whomServer]
            exe(f"uvicorn {whomServer}:app --host 0.0.0.0 --port {port} --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")
    except:
        pass
    if sys.SharedMemory["is_process_running"]:
        try:
            sys.SharedMemory["is_process_running"] = False
            return True
        except Exception as e:
            print(f"Error stopping FastAPI app: {e}")
            return False
    else:
        return False

# Function to stop the FastAPI server
def stop_server(whomServer="all"):
    try:
        if(whomServer == "all"):
            exe("sudo pkill -f 'uvicorn.*vellore:app'")
            exe("sudo pkill -f 'uvicorn.*virar:app'")
            exe("sudo pkill -f 'uvicorn.*talentov:app'")
        else:
            exe(f"sudo pkill -f 'uvicorn.*{whomServer}:app'")
    except:
        pass
    if sys.SharedMemory["is_process_running"]:
        try:
            sys.SharedMemory["is_process_running"] = False
            return True
        except Exception as e:
            print(f"Error stopping FastAPI app: {e}")
            return False
    else:
        return False


import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Start Server","Restart","Stop Server"],
    ["Stats","Bot Reboot"],
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    context.user_data["data"] = []
    await update.message.reply_text(
        "Welcome Jay!",
        reply_markup=markup,
    )

    return CHOOSING

import requests

# URLs to check
urls = {
    "talentov": "https://jay-python-aws-server.in.net:5000/sql/talentov/root/get",
    "virar": "https://jay-python-aws-server.in.net:50087/sql/virar/root/get",
    "vellore": "https://jay-python-aws-server.in.net:50088/sql/vellore/root/get"
}


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text("Hello Boss")
    return CHOOSING

async def bot_reboot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text("Please /start Again...",reply_markup=ReplyKeyboardRemove())
    # delayed_restart(context)
    with open("/home/ubuntu/kill.txt","w") as f:
        f.write("")
    context.user_data.clear()
    return ConversationHandler.END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text("Loading...")

    system_total_ram_mb = 0
    system_ram_percent_str = 0

    for name, url in urls.items():
        txt = ""
        try:
            # await update.message.reply_text("Hitting : "+url)
            # response = requests.get(url, headers={
            #     'Cache-Control': 'no-cache, no-store, must-revalidate',
            #     'Pragma': 'no-cache',
            #     'Expires': '0'
            # }, timeout=5)

            cmd = f"ps aux | grep '{name}' | grep -v grep"

            # Execute the command
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Capture the output and errors
            stdout, stderr = process.communicate()

            # Decode the output from bytes to string
            output = stdout.decode('utf-8')
            lines = output.strip().split("\n")
            
            if lines == ['']:
                txt = f"{name} is Down"
            else:
                # Extract the PIDs and calculate RAM usage
                pids = []
                total_ram = 0.0
                total_ram_percent = 0.0
                for line in lines:
                    parts = line.split()
                    pids.append(parts[1])  # PID is the second column
                    total_ram += float(parts[5])  # RSS is the 6th column (RAM usage in KB)
                    total_ram_percent += float(parts[3])  # %MEM is the 4th column

                # Convert total RAM usage to MB
                total_ram_mb = total_ram / 1024.0

                pids_str = ",".join(pids)
                ram_str = f"{total_ram_mb:.2f} MB"
                ram_percent_str = f"{total_ram_percent:.2f}%"

                system_total_ram_mb += total_ram_mb
                system_ram_percent_str += total_ram_percent

                # Construct the final message
                txt = f"{name} is Fine\nProcess ID: {pids_str}\nRAM Taken: {ram_str} - {ram_percent_str}"
    
        except requests.exceptions.RequestException as e:
            txt = f"{name} is Down"
        await update.message.reply_text(txt)
    if(system_total_ram_mb > 0 or system_ram_percent_str > 0):
        ram_str = f"{system_total_ram_mb:.2f} MB"
        ram_percent_str = f"{system_ram_percent_str:.2f}%"
        await update.message.reply_text(f"Total RAM Taken: {ram_str} - {ram_percent_str}")
    await update.message.reply_text("That's It Boss!",reply_markup=markup)
    return CHOOSING

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text(
        "File Log : " + get_log(),
        reply_markup=markup,
    )

    return CHOOSING
 
import asyncio
async def run_hold_restart_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text(f"wait boss!")
    if(text.split(' ')[0] == "Run"):
        start_server(text.split(' ')[1])
        await update.message.reply_text("Started!",reply_markup=markup)
    elif(text.split(' ')[0] == "Hold"):
        stop_server(text.split(' ')[1])
        await update.message.edit_message_reply_markup("Stopped!",reply_markup=markup)
    elif(text.split(' ')[0] == "Restart"):
        stop_server(text.split(' ')[1])
        await asyncio.sleep(2)
        await update.message.reply_text("Stopped!")
        start_server(text.split(' ')[1])
        await asyncio.sleep(2)
        await update.message.reply_text("Started!")
        await update.message.reply_text("Restart Finished",reply_markup=markup)
    else:
        pass
    # log = "Here is the Log File" + get_log()
    return CHOOSING

async def start_stop_restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    # context.user_data["choice"] = text
    # await update.message.reply_text(f"wait boss!")

    responce_text = ""
    if(text == "Restart"):
        await update.message.reply_text(
            "Please Choose the DB to Restart!",
            reply_markup = ReplyKeyboardMarkup([
                ["Restart all", "Restart virar"],
                ["Restart vellore", "Restart talentov"],
            ], one_time_keyboard=True),
        )
    elif(text == "Start Server"):
        await update.message.reply_text(
            "Please Choose the DB to Run!",
            reply_markup = ReplyKeyboardMarkup([
                ["Run all", "Run virar"],
                ["Run vellore", "Run talentov"],
            ], one_time_keyboard=True),
        )
    elif(text == "Stop Server"):
        await update.message.reply_text(
            "Please Choose the DB to Stop/Hold!",
            reply_markup = ReplyKeyboardMarkup([
                ["Hold all", "Hold virar"],
                ["Hold vellore", "Hold talentov"],
            ], one_time_keyboard=True),
        )

    # await update.message.reply_text(responce_text)

    return CHOOSING


async def normal_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    text = update.message.text
    context.user_data["data"].append(text)
    
    await update.message.reply_text("Stored")

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    context.user_data

    await update.message.reply_text(
        "Here is the data : "+(','.join(context.user_data['data']))+"",
        reply_markup=ReplyKeyboardRemove(),
    )

    context.user_data.clear()
    return ConversationHandler.END

async def progress(update: Update, context: CallbackContext):
    # Initialize progress
    progress = 0
    message = await update.message.reply_text("Progress: Starting 0%")
    
    # Update the progress every second until it reaches 100%
    while progress < 100:
        await asyncio.sleep(1)  # Sleep for 1 second
        progress += 1  # Increment progress by 10%
        # Update the message with the new progress bar
        await message.edit_text(f"Progress: [{'#' * (progress // 10)}{'-' * (10 - progress // 10)}] {progress}%")

    # Optionally, you can perform additional actions after completion
    await update.message.reply_text("Task completed!",reply_markup=markup)

    return CHOOSING




def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^(Hello|hello|Helo|helo)$"), hello),
                MessageHandler(filters.Regex("^(Done|done)$"), done),
                MessageHandler(filters.Regex("^(Restart|Start Server|Stop Server)$"), start_stop_restart),
                # MessageHandler(filters.Regex("^(Log|log)$"), log),
                MessageHandler(filters.Regex("^(Bot Reboot)$"), bot_reboot),
                MessageHandler(filters.Regex("^(Stats|stats)$"), stats),
                MessageHandler(filters.Regex("^Run.*$"), run_hold_restart_server),
                MessageHandler(filters.Regex("^Hold.*$"), run_hold_restart_server),
                MessageHandler(filters.Regex("^Restart.*$"), run_hold_restart_server), 
                MessageHandler(filters.Regex("^Progress.*$"), progress), 
                MessageHandler(filters.Regex("^.*$"), normal_messages)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)
    sys.sh = application.shutdown
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

main()