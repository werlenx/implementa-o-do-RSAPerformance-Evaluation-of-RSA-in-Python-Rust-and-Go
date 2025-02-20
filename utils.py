def format_duration(seconds):
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def format_memory(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024**2:
        return f"{bytes / 1024:.2f} KB"
    else:
        return f"{bytes / (1024**2):.2f} MB"


def print_benchmark_header(operation, key_size, library, iterations):
    print(f"\n{'='*80}")
    print(f"Benchmark: {operation}")
    print(f"Biblioteca: {library}")
    print(f"Tamanho da chave: {key_size} bits")
    print(f"Iterações: {iterations}")
    print('='*80)


def print_benchmark_results(name, results):
    print(f"\n▶ Resultados para {name}:")

    for metric, values in results.items():
        print(f"  └─ {metric}:")
        print(f"     ├─ Média: {values['mean']}")
        print(f"     ├─ Desvio padrão: {values['std_dev']}")
        print(f"     ├─ Mediana: {values['median']}")
        print(f"     └─ Min/Max: {values['min']} / {values['max']}")
