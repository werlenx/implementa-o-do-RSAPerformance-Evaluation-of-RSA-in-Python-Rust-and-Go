import os
#import timeit
import time
import numpy as np
import psutil
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from tabulate import tabulate

# Média e desvio padrão
def calc_mean_std(data):
    mean = np.mean(data)
    std = np.std(data)
    return mean, std

# CPU e memória de todos os processos
def cpu_memory():
    process = psutil.Process(os.getpid())
    cpu_percent = psutil.cpu_percent(interval=0.1)  # %
    memory_info = process.memory_info().rss
    return cpu_percent, memory_info  #bytes

# Geração de chaves
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

# Cifração
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

# Decifração
def benchmark_decrypt(executions, bitkeys, rsa_keys):
    execution_times = {}
    cpu_usages = {}
    memory_usages = {}

    for key_size in bitkeys:
        total_times = []
        total_cpu = []
        total_memory = []

        key = rsa_keys[key_size]
        cipher_rsa = PKCS1_OAEP.new(key)
        message = os.urandom(190)
        ciphertext = cipher_rsa.encrypt(message)

        for _ in range(executions):
            start_time = time.perf_counter()
            cpu_start, memory_start = cpu_memory()

            plaintext = cipher_rsa.decrypt(ciphertext)

            cpu_end, memory_end = cpu_memory()
            end_time = time.perf_counter()

            total_times.append(end_time - start_time)
            cpu_used = max(cpu_end - cpu_start, 0)
            total_cpu.append(cpu_used)
            total_memory.append(memory_end - memory_start)

        mean_time, std_time = calc_mean_std(total_times)
        mean_cpu, std_cpu = calc_mean_std(total_cpu)
        mean_memory, std_memory = calc_mean_std(total_memory)

        execution_times[key_size] = (mean_time, std_time)
        cpu_usages[key_size] = (mean_cpu, std_cpu)
        memory_usages[key_size] = (mean_memory, std_memory)

    return execution_times, cpu_usages, memory_usages






# Valores de iterações e chaves
iterations = [10,100, 1000, 10000]
bitkeys = [2048, 4096]

# Criar tabela com os dados
table_data = []
for executions in iterations:
    rsa_keys, generate_times, generate_cpu, generate_memory = benchmark_generate_keys(executions, bitkeys, return_keys=True)
    encrypt_times, encrypt_cpu, encrypt_memory = benchmark_encrypt(executions, bitkeys, rsa_keys)
    decrypt_times, decrypt_cpu, decrypt_memory = benchmark_decrypt(executions, bitkeys, rsa_keys)

    for key_size in bitkeys:
        # Geração de chaves
        gen_time_mean, gen_time_std = generate_times[key_size]
        gen_cpu_mean, gen_cpu_std = generate_cpu[key_size]
        gen_memory_mean, gen_memory_std = generate_memory[key_size]

        # Cifração
        enc_time_mean, enc_time_std = encrypt_times[key_size]
        enc_cpu_mean, enc_cpu_std = encrypt_cpu[key_size]
        enc_memory_mean, enc_memory_std = encrypt_memory[key_size]

        # Decifração
        dec_time_mean, dec_time_std = decrypt_times[key_size]
        dec_cpu_mean, dec_cpu_std = decrypt_cpu[key_size]
        dec_memory_mean, dec_memory_std = decrypt_memory[key_size]

        # Adicionar à tabela
        table_data.append([
            key_size,
            executions,
            gen_time_mean, gen_time_std,
            gen_cpu_mean, gen_cpu_std,
            gen_memory_mean, gen_memory_std,
            enc_time_mean, enc_time_std,
            enc_cpu_mean, enc_cpu_std,
            enc_memory_mean, enc_memory_std,
            dec_time_mean, dec_time_std,
            dec_cpu_mean, dec_cpu_std,
            dec_memory_mean, dec_memory_std,
        ])

# Cabeçalhos da tabela
headers = [
    "Tamanho da Chave",
    "Iterações",
    "Geração Tempo Médio (s)", "Geração Desvio Tempo (s)",
    "Geração CPU Médio (%)", "Geração Desvio CPU (%)",
    "Geração Memória Média (bytes)", "Geração Desvio Memória (bytes)",
    "Cifração Tempo Médio (s)", "Cifração Desvio Tempo (s)",
    "Cifração CPU Médio (%)", "Cifração Desvio CPU (%)",
    "Cifração Memória Média (bytes)", "Cifração Desvio Memória (bytes)",
    "Decifração Tempo Médio (s)", "Decifração Desvio Tempo (s)",
    "Decifração CPU Médio (%)", "Decifração Desvio CPU (%)",
    "Decifração Memória Média (bytes)", "Decifração Desvio Memória (bytes)",
]

# Exibir tabela
print(tabulate(table_data, headers=headers, floatfmt=".6f"))