import os 
import threading

print(f"Python proccess running with process id: {os.getpid()}")

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print(f"Python is currently running {total_threads} thread(s)")
print(f"The current thread is {thread_name}")