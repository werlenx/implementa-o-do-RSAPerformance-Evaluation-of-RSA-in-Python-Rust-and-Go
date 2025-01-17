import matplotlib.pyplot as plt
import numpy as np
from Crypto.PublicKey import RSA
from time import time
import psutil
import statistics

# Funções de captura de métricas e operações RSA
def capture_metrics(func, *args, **kwargs):
    """Captura métricas de tempo, CPU e memória ao executar uma função."""
    process = psutil.Process()
    start_time = time()
    start_memory = process.memory_info().rss  # Memória inicial
    start_cpu = process.cpu_percent(interval=None)  # CPU inicial

    # Executa a função
    result = func(*args, **kwargs)

    end_time = time()
    end_memory = process.memory_info().rss  # Memória final
    end_cpu = process.cpu_percent(interval=None)  # CPU final

    metrics = {
        "execution_time": end_time - start_time,
        "memory_usage": (end_memory - start_memory) / (1024 * 1024),  # Convertido para MB
        "cpu_usage": end_cpu
    }

    return result, metrics

def generate_keys(bits=2048):
    """Gera um par de chaves RSA."""
    key = RSA.generate(bits)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key

def encrypt_message_rsa_pure(message, public_key):
    """Criptografa a mensagem usando RSA puro."""
    message_int = int.from_bytes(message, byteorder='big')  # Converte a mensagem em um número inteiro
    ciphertext = pow(message_int, public_key.e, public_key.n)  # Realiza a criptografia com RSA
    return ciphertext

def decrypt_message_rsa_pure(ciphertext, private_key):
    """Descriptografa a mensagem usando RSA puro."""
    message_int = pow(ciphertext, private_key.d, private_key.n)
    plaintext = message_int.to_bytes((private_key.n.bit_length() + 7) // 8, byteorder='big').lstrip(b'\x00')
    return plaintext

# Função para salvar os resultados em um arquivo de log
def save_metrics_to_file(file_path, keygen_metrics, encrypt_metrics, decrypt_metrics):
    with open(file_path, 'a') as f:
        f.write(f"{keygen_metrics['execution_time']},{keygen_metrics['memory_usage']},{keygen_metrics['cpu_usage']},"
                f"{encrypt_metrics['execution_time']},{encrypt_metrics['memory_usage']},{encrypt_metrics['cpu_usage']},"
                f"{decrypt_metrics['execution_time']},{decrypt_metrics['memory_usage']},{decrypt_metrics['cpu_usage']}\n")

# Teste de 5 repetições para 10 iterações
iterations = 10
repetitions = 5
log_file = 'resultados_metrica_rsa.txt'

# Inicializando o arquivo de log com cabeçalho
with open(log_file, 'w') as f:
    f.write("keygen_exec_time,keygen_mem_usage,keygen_cpu_usage,"
            "encrypt_exec_time,encrypt_mem_usage,encrypt_cpu_usage,"
            "decrypt_exec_time,decrypt_mem_usage,decrypt_cpu_usage,"
            "keygen_exec_time_median,keygen_mem_usage_median,keygen_cpu_usage_median,"
            "encrypt_exec_time_median,encrypt_mem_usage_median,encrypt_cpu_usage_median,"
            "decrypt_exec_time_median,decrypt_mem_usage_median,decrypt_cpu_usage_median,"
            "keygen_exec_time_std,keygen_mem_usage_std,keygen_cpu_usage_std,"
            "encrypt_exec_time_std,encrypt_mem_usage_std,encrypt_cpu_usage_std,"
            "decrypt_exec_time_std,decrypt_mem_usage_std,decrypt_cpu_usage_std\n")

# Rodando as repetições
for rep in range(repetitions):
    print(f"Repetição {rep + 1}/{repetitions}...")
    
    keygen_metrics_list = []
    encrypt_metrics_list = []
    decrypt_metrics_list = []
    
    for _ in range(iterations):
        # Métricas de geração de chaves
        (private_key, public_key), keygen_metrics = capture_metrics(generate_keys)

        # Métricas de criptografia
        encrypted_message, encrypt_metrics = capture_metrics(encrypt_message_rsa_pure, b"Mensagem confidencial!", public_key)

        # Métricas de descriptografia
        decrypted_message, decrypt_metrics = capture_metrics(decrypt_message_rsa_pure, encrypted_message, private_key)
        
        keygen_metrics_list.append(keygen_metrics)
        encrypt_metrics_list.append(encrypt_metrics)
        decrypt_metrics_list.append(decrypt_metrics)

    # Cálculo da mediana e desvio padrão para cada métrica
    def calculate_median_and_std(metrics_list, key):
        values = [metrics[key] for metrics in metrics_list]
        return statistics.median(values), statistics.stdev(values)

    # Coletando medianas e desvios padrão
    keygen_exec_time_median, keygen_exec_time_std = calculate_median_and_std(keygen_metrics_list, 'execution_time')
    keygen_mem_usage_median, keygen_mem_usage_std = calculate_median_and_std(keygen_metrics_list, 'memory_usage')
    keygen_cpu_usage_median, keygen_cpu_usage_std = calculate_median_and_std(keygen_metrics_list, 'cpu_usage')

    encrypt_exec_time_median, encrypt_exec_time_std = calculate_median_and_std(encrypt_metrics_list, 'execution_time')
    encrypt_mem_usage_median, encrypt_mem_usage_std = calculate_median_and_std(encrypt_metrics_list, 'memory_usage')
    encrypt_cpu_usage_median, encrypt_cpu_usage_std = calculate_median_and_std(encrypt_metrics_list, 'cpu_usage')

    decrypt_exec_time_median, decrypt_exec_time_std = calculate_median_and_std(decrypt_metrics_list, 'execution_time')
    decrypt_mem_usage_median, decrypt_mem_usage_std = calculate_median_and_std(decrypt_metrics_list, 'memory_usage')
    decrypt_cpu_usage_median, decrypt_cpu_usage_std = calculate_median_and_std(decrypt_metrics_list, 'cpu_usage')

    # Salvando as métricas no arquivo de log
    with open(log_file, 'a') as f:
        f.write(f"{keygen_metrics_list[0]['execution_time']},{keygen_metrics_list[0]['memory_usage']},{keygen_metrics_list[0]['cpu_usage']},"
                f"{encrypt_metrics_list[0]['execution_time']},{encrypt_metrics_list[0]['memory_usage']},{encrypt_metrics_list[0]['cpu_usage']},"
                f"{decrypt_metrics_list[0]['execution_time']},{decrypt_metrics_list[0]['memory_usage']},{decrypt_metrics_list[0]['cpu_usage']},"
                f"{keygen_exec_time_median},{keygen_mem_usage_median},{keygen_cpu_usage_median},"
                f"{encrypt_exec_time_median},{encrypt_mem_usage_median},{encrypt_cpu_usage_median},"
                f"{decrypt_exec_time_median},{decrypt_mem_usage_median},{decrypt_cpu_usage_median},"
                f"{keygen_exec_time_std},{keygen_mem_usage_std},{keygen_cpu_usage_std},"
                f"{encrypt_exec_time_std},{encrypt_mem_usage_std},{encrypt_cpu_usage_std},"
                f"{decrypt_exec_time_std},{decrypt_mem_usage_std},{decrypt_cpu_usage_std}\n")

    # Gráficos
    metrics_to_plot = {
        'keygen': {
            'execution_time': [metrics['execution_time'] for metrics in keygen_metrics_list],
            'memory_usage': [metrics['memory_usage'] for metrics in keygen_metrics_list],
            'cpu_usage': [metrics['cpu_usage'] for metrics in keygen_metrics_list]
        },
        'encrypt': {
            'execution_time': [metrics['execution_time'] for metrics in encrypt_metrics_list],
            'memory_usage': [metrics['memory_usage'] for metrics in encrypt_metrics_list],
            'cpu_usage': [metrics['cpu_usage'] for metrics in encrypt_metrics_list]
        },
        'decrypt': {
            'execution_time': [metrics['execution_time'] for metrics in decrypt_metrics_list],
            'memory_usage': [metrics['memory_usage'] for metrics in decrypt_metrics_list],
            'cpu_usage': [metrics['cpu_usage'] for metrics in decrypt_metrics_list]
        }
    }

    # Gráficos de linha para execução do tempo, uso de memória e uso de CPU
    for op in ['keygen', 'encrypt', 'decrypt']:
        fig, axes = plt.subplots(3, 1, figsize=(10, 15))
        axes[0].plot(metrics_to_plot[op]['execution_time'], label=f'{op} Exec. Time', color='b')
        axes[1].plot(metrics_to_plot[op]['memory_usage'], label=f'{op} Mem Usage', color='g')
        axes[2].plot(metrics_to_plot[op]['cpu_usage'], label=f'{op} CPU Usage', color='r')

        axes[0].set_title(f'{op} - Execution Time')
        axes[0].set_xlabel('Iteration')
        axes[0].set_ylabel('Execution Time (s)')

        axes[1].set_title(f'{op} - Memory Usage')
        axes[1].set_xlabel('Iteration')
        axes[1].set_ylabel('Memory Usage (MB)')

        axes[2].set_title(f'{op} - CPU Usage')
        axes[2].set_xlabel('Iteration')
        axes[2].set_ylabel('CPU Usage (%)')

        plt.tight_layout()
        plt.savefig(f"{op}_metrics.png")
        plt.close()
