import pandas as pd

def calculate_overall_metrics(csv_file, output_file):
    # Carregar o arquivo CSV
    data = pd.read_csv(csv_file)
    
    # Calcular as médias gerais
    metrics = {
        "Keygen Execution Time": data["Keygen Execution Time"].mean(),
        "Keygen Memory Usage": data["Keygen Memory Usage"].mean(),
        "Keygen CPU Usage": data["Keygen CPU Usage"].mean(),
        "Encrypt Execution Time": data["Encrypt Execution Time"].mean(),
        "Encrypt Memory Usage": data["Encrypt Memory Usage"].mean(),
        "Encrypt CPU Usage": data["Encrypt CPU Usage"].mean(),
        "Decrypt Execution Time": data["Decrypt Execution Time"].mean(),
        "Decrypt Memory Usage": data["Decrypt Memory Usage"].mean(),
        "Decrypt CPU Usage": data["Decrypt CPU Usage"].mean()
    }

    # Converter as métricas para um DataFrame
    metrics_df = pd.DataFrame([metrics])

    # Verificar se o arquivo de saída já existe para não duplicar o cabeçalho
    try:
        # Tenta carregar o arquivo de saída para verificar se existe
        existing_data = pd.read_csv(output_file)
        # Se o arquivo existir, define header=False para não duplicar os cabeçalhos
        metrics_df.to_csv(output_file, mode='a', header=False, index=False)
    except FileNotFoundError:
        # Se o arquivo não existir, cria com o cabeçalho
        metrics_df.to_csv(output_file, index=False)

# Exemplo de uso
csv_file = "rsa_metrics_dataset.csv"
output_file = "calculated_metrics.csv"

calculate_overall_metrics(csv_file, output_file)
