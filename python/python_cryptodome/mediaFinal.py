import csv

def calcular_medias(arquivo_csv):
    with open(arquivo_csv, 'r') as arquivo:
        leitor = csv.reader(arquivo)
        cabecalho = next(leitor)  # Lê a primeira linha como cabeçalho
        colunas = len(cabecalho)
        somas = [0.0] * colunas
        contador = 0

        for linha in leitor:
            valores = [float(valor) for valor in linha]
            somas = [soma + valor for soma, valor in zip(somas, valores)]
            contador += 1

        medias = [soma / contador for soma in somas]
        
        # Exibir o resultado
        print("Médias calculadas:")
        for nome, media in zip(cabecalho, medias):
            print(f"{nome}: {media:.6f}")

# Chamar a função passando o nome do arquivo
calcular_medias('calculated_metrics.csv')
