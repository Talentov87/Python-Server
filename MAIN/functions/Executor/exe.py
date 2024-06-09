import importlib.util
import sys
import threading
import builtins
import os
import gc
import queue
import json
from decimal import Decimal

def js(resp):
    try:
        # Convert Decimal objects to float or int before serializing
        resp_serialized = json.dumps(resp, default=lambda o: int(o) if o == int(o) else float(o) if isinstance(o, Decimal) else o)
        return resp_serialized
    except Exception as e:
        print(e)


# Define restricted functions
def restricted_operation(*args, **kwargs):
    raise PermissionError("Some Operations Are Restricted")

# Save original functions to restore later
original_open = builtins.open
original_remove = os.remove
original_chdir = os.chdir
original_getcwd = os.getcwd
original_mkdir = os.mkdir
original_makedirs = os.makedirs

# Replace the original functions with the restricted ones
builtins.open = restricted_operation
os.remove = restricted_operation
os.chdir = restricted_operation
os.mkdir = restricted_operation
os.makedirs = restricted_operation

import ctypes

def stop_thread(thread):
    """Raises an exception in the threads with id tid"""
    tid = thread.ident
    exctype = SystemExit
    if not isinstance(tid, int):
        raise TypeError("Only integers are allowed for thread id")
    if not issubclass(exctype, BaseException):
        raise ValueError("Only subclasses of BaseException are allowed for exception type")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("Invalid thread id")
    elif res != 1:
        # If it returns a number greater than one, we're in trouble, and we need to call it again with exc=0 to revert
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    

def run_python_with_restrictions(script_path,function_name,time_out,payload=None):
    print("Script START")
    # Function to execute the target script
    def execute_target(result_queue):
        try:
            # Execute the target script
            spec = importlib.util.spec_from_file_location("temp", script_path)
            if(spec == None):
                result_queue.put({"Message" : f"File '{script_path}' not found or not callable"})
            else:
                target_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(target_module)
                target_function = getattr(target_module, function_name, None)
                # Check if the function exists
                if target_function is not None and callable(target_function):
                    # Call the function
                    if(payload):
                        result = target_function(payload)
                    else:
                        result = target_function()
                    result_queue.put(result)
                else:
                    result_queue.put({"Message" : f"Function '{function_name}' not found or not callable"})
                print("Script executed successfully.")
        except Exception as e:
            result_queue.put({"Message" : f"Script failed with error: {e}"})
        finally:
            if 'temp' in sys.modules:
                del sys.modules['temp']
            # Explicitly trigger garbage collection
            # gc.collect()

    # Create a queue to hold the result
    result_queue = queue.Queue()
    # Start a daemon thread to execute the target script
    target_thread = threading.Thread(target=execute_target,args=(result_queue,))
    target_thread.daemon = True
    target_thread.start()
    # Wait for the target script to complete or the timeout to occur
    target_thread.join(time_out)
    is_over_time_run = target_thread.is_alive()
    if(is_over_time_run):
        stop_thread(target_thread)

    print("Script END")
    if not result_queue.empty():
        result = result_queue.get()
    else:
        if(is_over_time_run):
            result = {"Status":"Failed","Message" : "Time Exceed","Detail":f"This Message is from the jay's server represents that the api call you triggered is taking more than {time_out} seconds","Terms":f"Your Python file must be imported and need to be executed within {time_out} seconds"}
        else:
            result = {}
    return js(result)

# if len(sys.argv) != 4:
#     print("Usage: python test.py module_name.py function_name timeout")
#     sys.exit(1)

# target_script_path = sys.argv[1]
# function_name = sys.argv[2]+"_api"
# time_out = int(sys.argv[3])

# run_python_with_restrictions(target_script_path,function_name,time_out)