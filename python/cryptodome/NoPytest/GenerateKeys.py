import time
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Statistics import calc_mean_std
from MonitorMenCpu import cpu_memory


def benchmark_generate_keys(executions, bitkeys, return_keys=False):
    execution_times = {}
    cpu_usages = {}
    memory_usages = {}
    rsa_keys = {}

    for key_size in bitkeys:
        total_times = []
        total_cpu = []
        total_memory = []

        for _ in range(executions):
            start_time = time.perf_counter()
            cpu_start, memory_start = cpu_memory()

            rsa_keys[key_size] = RSA.generate(key_size)

            cpu_end, memory_end = cpu_memory()
            end_time = time.perf_counter()

            total_times.append(end_time - start_time)
            total_cpu.append(cpu_end)  # Uso de CPU durante a execução
            memory_used = max(memory_end - memory_start, 0) # garante que resultado nao será negativo
            total_memory.append(memory_used)  # Uso de memória durante a execução

        mean_time, std_time = calc_mean_std(total_times)
        mean_cpu, std_cpu = calc_mean_std(total_cpu)
        mean_memory, std_memory = calc_mean_std(total_memory)

        execution_times[key_size] = (mean_time, std_time)
        cpu_usages[key_size] = (mean_cpu, std_cpu)
        memory_usages[key_size] = (mean_memory, std_memory)

    if return_keys:
        return rsa_keys, execution_times, cpu_usages, memory_usages
    else:
        return execution_times, cpu_usages, memory_usages