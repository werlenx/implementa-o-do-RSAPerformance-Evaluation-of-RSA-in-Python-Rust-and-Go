from Crypto.PublicKey import RSA
from time import time
import psutil
import csv

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


def generate_keys(bits=4096):
    """Gera um par de chaves RSA."""
    key = RSA.generate(bits)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key


def encrypt_message_rsa_pure(message, public_key):
    """Criptografa uma mensagem usando RSA puro."""
    message_int = int.from_bytes(message, byteorder='big')  # Converte a mensagem em um número inteiro
    ciphertext = pow(message_int, public_key.e, public_key.n)  # Fórmula RSA: ciphertext = (message ^ e) % n
    return ciphertext


def decrypt_message_rsa_pure(ciphertext, private_key):
    """Descriptografa uma mensagem usando RSA puro."""
    message_int = pow(ciphertext, private_key.d, private_key.n)  # Fórmula RSA: plaintext = (ciphertext ^ d) % n
    plaintext = message_int.to_bytes((private_key.n.bit_length() + 7) // 8, byteorder='big').lstrip(b'\x00')
    return plaintext


# Função para calcular a média das métricas
def calculate_average_metrics(metrics_list):
    avg_metrics = {
        "execution_time": sum(m["execution_time"] for m in metrics_list) / len(metrics_list),
        "memory_usage": sum(m["memory_usage"] for m in metrics_list) / len(metrics_list),
        "cpu_usage": sum(m["cpu_usage"] for m in metrics_list) / len(metrics_list)
    }
    return avg_metrics


# Função para salvar as métricas em um arquivo CSV
def save_metrics_to_csv(filename, keygen_metrics, encrypt_metrics, decrypt_metrics):
    # Cabeçalhos para o CSV
    headers = [
        "Keygen Execution Time", "Keygen Memory Usage", "Keygen CPU Usage",
        "Encrypt Execution Time", "Encrypt Memory Usage", "Encrypt CPU Usage",
        "Decrypt Execution Time", "Decrypt Memory Usage", "Decrypt CPU Usage"
    ]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for i in range(len(keygen_metrics)):
            writer.writerow([
                keygen_metrics[i]["execution_time"], keygen_metrics[i]["memory_usage"], keygen_metrics[i]["cpu_usage"],
                encrypt_metrics[i]["execution_time"], encrypt_metrics[i]["memory_usage"], encrypt_metrics[i]["cpu_usage"],
                decrypt_metrics[i]["execution_time"], decrypt_metrics[i]["memory_usage"], decrypt_metrics[i]["cpu_usage"]
            ])


# Parâmetros de teste
message = b"Mensagem confidencial!"
repetitions = 5
iterations = 10000

# Armazenar métricas para cada operação
keygen_metrics_all = []
encrypt_metrics_all = []
decrypt_metrics_all = []

for _ in range(repetitions):
    for _ in range(iterations):
        # Geração de chaves
        (private_key, public_key), keygen_metrics = capture_metrics(generate_keys)
        keygen_metrics_all.append(keygen_metrics)

        # Criptografia
        encrypted_message, encrypt_metrics = capture_metrics(encrypt_message_rsa_pure, message, public_key)
        encrypt_metrics_all.append(encrypt_metrics)

        # Descriptografia
        decrypted_message, decrypt_metrics = capture_metrics(decrypt_message_rsa_pure, encrypted_message, private_key)
        decrypt_metrics_all.append(decrypt_metrics)

# Calculando as médias
avg_keygen_metrics = calculate_average_metrics(keygen_metrics_all)
avg_encrypt_metrics = calculate_average_metrics(encrypt_metrics_all)
avg_decrypt_metrics = calculate_average_metrics(decrypt_metrics_all)

# Salvar as métricas em um arquivo CSV
save_metrics_to_csv("rsa_metrics_dataset.csv", keygen_metrics_all, encrypt_metrics_all, decrypt_metrics_all)

