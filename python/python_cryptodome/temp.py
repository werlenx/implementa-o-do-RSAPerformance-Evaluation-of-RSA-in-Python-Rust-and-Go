import pandas as pd
import matplotlib.pyplot as plt
import io  # Importar o módulo io para lidar com strings como arquivos

# Dados como string CSV
data = """Keygen Execution Time,Keygen Memory Usage,Keygen CPU Usage,Encrypt Execution Time,Encrypt Memory Usage,Encrypt CPU Usage,Decrypt Execution Time,Decrypt Memory Usage,Decrypt CPU Usage
0.5433257675170898,0.0075,100.102,0.000385689735412552,0.0,87.65,0.03187676429748531,0.0,100.764
0.5300327749252319,0.00075,99.8652,0.00038414907455439816,0.0,126.19639999999998,0.031641805171966506,0.0,99.81360000000001
0.7657823534965515,0.00085,99.00402,0.0005038351535796613,0.0,95.5139,0.038508414888381914,5e-05,99.09812"""

# Converter para um DataFrame usando io.StringIO
df = pd.read_csv(io.StringIO(data))

# Adicionar a coluna de iterações
df['Iterations'] = [10, 100, 1000]

# Configurar os gráficos
plt.figure(figsize=(14, 10))

# Métricas para visualização
metrics = {
    "Keygen Execution Time": "Keygen Execution Time (s)",
    "Encrypt Execution Time": "Encrypt Execution Time (s)",
    "Decrypt Execution Time": "Decrypt Execution Time (s)",
    "Keygen Memory Usage": "Keygen Memory Usage (MB)",
    "Encrypt Memory Usage": "Encrypt Memory Usage (MB)",
    "Decrypt Memory Usage": "Decrypt Memory Usage (MB)",
    "Keygen CPU Usage": "Keygen CPU Usage (%)",
    "Encrypt CPU Usage": "Encrypt CPU Usage (%)",
    "Decrypt CPU Usage": "Decrypt CPU Usage (%)"
}

# Plotar cada métrica
for i, (metric, ylabel) in enumerate(metrics.items(), 1):
    plt.subplot(3, 3, i)  # Grade 3x3 para os gráficos
    plt.bar(df["Iterations"], df[metric], width=0.6, color='skyblue', alpha=0.8, edgecolor='black')  # Ajustando largura
    plt.title(metric, fontsize=10)
    plt.xlabel("Iterations")
    plt.ylabel(ylabel)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Adicionar valores nas barras
    for x, y in zip(df["Iterations"], df[metric]):
        plt.text(x, y, f"{y:.3f}", ha='center', va='bottom', fontsize=8)

# Ajustar layout
plt.tight_layout()

# Salvar o gráfico como imagem
output_file = "metrics_bar_graph_thicker.png"
plt.savefig(output_file, dpi=300)  # Salvar como PNG com alta resolução
plt.show()

print(f"Gráfico salvo como: {output_file}")
