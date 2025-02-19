import os
import psutil

def cpu_memory():
    process = psutil.Process(os.getpid())
    cpu_percent = psutil.cpu_percent(interval=0.1)  # %
    memory_info = process.memory_info().rss
    return cpu_percent, memory_info  #bytes