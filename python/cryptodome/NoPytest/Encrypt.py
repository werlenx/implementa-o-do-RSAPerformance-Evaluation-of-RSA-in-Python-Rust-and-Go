import os
import time
from Crypto.Cipher import PKCS1_OAEP
from MonitorMenCpu import cpu_memory
from Statistics import calc_mean_std

def benchmark_encrypt(executions, bitkeys, rsa_keys):
    execution_times = {}
    cpu_usages = {}
    memory_usages = {}

    for key_size in bitkeys:
        total_times = []
        total_cpu = []
        total_memory = []

        key = rsa_keys[key_size]
        public_key = key.publickey()
        cipher_rsa = PKCS1_OAEP.new(public_key)
        message = os.urandom(190)

        for _ in range(executions):
            start_time = time.perf_counter()
            cpu_start, memory_start = cpu_memory()

            ciphertext = cipher_rsa.encrypt(message)

            cpu_end, memory_end = cpu_memory()
            end_time = time.perf_counter()

            total_times.append(end_time - start_time)
            total_cpu.append(cpu_end)
            total_memory.append(memory_end - memory_start)

        mean_time, std_time = calc_mean_std(total_times)
        mean_cpu, std_cpu = calc_mean_std(total_cpu)
        mean_memory, std_memory = calc_mean_std(total_memory)

        execution_times[key_size] = (mean_time, std_time)
        cpu_usages[key_size] = (mean_cpu, std_cpu)
        memory_usages[key_size] = (mean_memory, std_memory)

    return execution_times, cpu_usages, memory_usages