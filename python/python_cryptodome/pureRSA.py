from Crypto.PublicKey import RSA
from time import time
import psutil

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
    
    message_int = int.from_bytes(message, byteorder='big')# Converte a mensagem em um número inteiro
    
    ciphertext = pow(message_int, public_key.e, public_key.n)# Realiza a criptografia com a fórmula RSA: ciphertext = (message ^ e) % n
    return ciphertext

def decrypt_message_rsa_pure(ciphertext, private_key):
    """Descriptografa uma mensagem usando RSA puro."""
    # Realiza a descriptografia com a fórmula RSA: plaintext = (ciphertext ^ d) % n
    message_int = pow(ciphertext, private_key.d, private_key.n)
    # Converte o número inteiro de volta para bytes
    plaintext = message_int.to_bytes((private_key.n.bit_length() + 7) // 8, byteorder='big').lstrip(b'\x00')
    return plaintext

# Testando o algoritmo
message = b"Mensagem confidencial!"

# Métricas de geração de chaves
(private_key, public_key), keygen_metrics = capture_metrics(generate_keys)

# Métricas de criptografia
encrypted_message, encrypt_metrics = capture_metrics(encrypt_message_rsa_pure, message, public_key)

# Métricas de descriptografia
decrypted_message, decrypt_metrics = capture_metrics(decrypt_message_rsa_pure, encrypted_message, private_key)

# Resultados
print("Métricas de geração de chaves:               ", keygen_metrics)
print("Métricas de criptografia:                    ", encrypt_metrics)
print("Métricas de descriptografia:                 ", decrypt_metrics)


#print("\nMensagem criptografada:     ", encrypted_message)
#print("\nMensagem descriptografada:     ", decrypted_message.decode())
