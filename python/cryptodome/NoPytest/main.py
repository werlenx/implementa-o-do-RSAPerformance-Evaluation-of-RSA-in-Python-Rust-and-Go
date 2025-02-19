import time
from tabulate import tabulate
from GenerateKeys import benchmark_generate_keys
from Encrypt import benchmark_encrypt
from Decrypt import benchmark_decrypt

iterations = [10]
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