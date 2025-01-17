import matplotlib.pyplot as plt
import numpy as np

# Dados fornecidos para a análise
key_sizes = [2048, 4096]
data = {
    "Keygen Execution Time": [0.585702, 5.311739],
    "Encrypt Execution Time": [0.000407, 0.000868],
    "Decrypt Execution Time": [0.033137, 0.221898],
    "Keygen Memory Usage": [0.002419, 0.002872],
    "Encrypt Memory Usage": [0.0, 0.0],
    "Decrypt Memory Usage": [0.000019, 0.000643],
    "Keygen CPU Usage": [99.737161, 99.794183],
    "Encrypt CPU Usage": [103.364538, 84.724775],
    "Decrypt CPU Usage": [99.920427, 99.862229]
}

# Criando gráfico para tempos de execução
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.25
x = np.arange(len(key_sizes))

# Plotando tempos de execução
ax.bar(x - bar_width, data["Keygen Execution Time"], bar_width, label="Keygen", color="salmon", edgecolor="black")
ax.bar(x, data["Encrypt Execution Time"], bar_width, label="Encrypt", color="skyblue", edgecolor="black")
ax.bar(x + bar_width, data["Decrypt Execution Time"], bar_width, label="Decrypt", color="lightgreen", edgecolor="black")

# Configurações do gráfico de tempos de execução
ax.set_xticks(x)
ax.set_xticklabels([f"{size} bits" for size in key_sizes])
ax.set_title("Tempo de Execução por Operação e Tamanho da Chave")
ax.set_ylabel("Tempo (s)")
ax.set_xlabel("Tamanho da Chave")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Salvando imagem do gráfico de tempos de execução
plt.tight_layout()
plt.savefig("rsa_execution_times.png")

# Criando gráfico para uso de memória
fig, ax = plt.subplots(figsize=(10, 6))

# Plotando uso de memória
ax.bar(x - bar_width, data["Keygen Memory Usage"], bar_width, label="Keygen", color="salmon", edgecolor="black")
ax.bar(x, data["Encrypt Memory Usage"], bar_width, label="Encrypt", color="skyblue", edgecolor="black")
ax.bar(x + bar_width, data["Decrypt Memory Usage"], bar_width, label="Decrypt", color="lightgreen", edgecolor="black")

# Configurações do gráfico de uso de memória
ax.set_xticks(x)
ax.set_xticklabels([f"{size} bits" for size in key_sizes])
ax.set_title("Uso de Memória por Operação e Tamanho da Chave")
ax.set_ylabel("Memória (MB)")
ax.set_xlabel("Tamanho da Chave")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Salvando imagem do gráfico de uso de memória
plt.tight_layout()
plt.savefig("rsa_memory_usage.png")

# Criando gráfico para uso de CPU
fig, ax = plt.subplots(figsize=(10, 6))

# Plotando uso de CPU
ax.bar(x - bar_width, data["Keygen CPU Usage"], bar_width, label="Keygen", color="salmon", edgecolor="black")
ax.bar(x, data["Encrypt CPU Usage"], bar_width, label="Encrypt", color="skyblue", edgecolor="black")
ax.bar(x + bar_width, data["Decrypt CPU Usage"], bar_width, label="Decrypt", color="lightgreen", edgecolor="black")

# Configurações do gráfico de uso de CPU
ax.set_xticks(x)
ax.set_xticklabels([f"{size} bits" for size in key_sizes])
ax.set_title("Uso de CPU por Operação e Tamanho da Chave")
ax.set_ylabel("CPU (%)")
ax.set_xlabel("Tamanho da Chave")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Salvando imagem do gráfico de uso de CPU
plt.tight_layout()
plt.savefig("rsa_cpu_usage.png")
