import os
import time

def monitor_file(file_path):
    last_modified_time = os.path.getmtime(file_path)

    while True:
        time.sleep(1)  # Check every second
        current_modified_time = os.path.getmtime(file_path)

        if current_modified_time != last_modified_time:
            print(f"The file '{file_path}' has been modified.")
            last_modified_time = current_modified_time

# Usage
monitor_file('main.py')