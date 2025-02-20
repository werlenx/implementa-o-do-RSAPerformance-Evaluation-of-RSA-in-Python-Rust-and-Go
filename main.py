import time
import statistics
import psutil
import os
import gc
import utils
import cryptography_utils as cryptography
import pycryptodome_utils as pycryptodome


def measure_resources(func, *args):
    # Força garbage collection antes da medição
    gc.collect()

    # Pocesso rodando
    process = psutil.Process(os.getpid())

    # Medições mais precisas de CPU
    cpu_percent_list = []
    mem_samples = []

    # Resetar CPU
    process.cpu_percent()

    # Medir memória inicial
    for _ in range(3):
        mem_samples.append(process.memory_info().rss)
    mem_before = statistics.mean(mem_samples)

    # Medir tempo e CPU
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()

    # Coletar várias amostras de CPU
    for _ in range(3):
        cpu_percent_list.append(process.cpu_percent())

    # Medir memória final (média de algumas amostras)
    mem_samples = []
    for _ in range(3):
        mem_samples.append(process.memory_info().rss)
    mem_after = statistics.mean(mem_samples)

    # Medir memória final
    mem_after = process.memory_info().rss

    return {
        'time': end_time - start_time,
        'cpu': statistics.mean(cpu_percent_list),
        'memory': mem_after - mem_before
    }


def benchmark(func, *args, iterations_list, repetitions):
    results = {}

    for iterations in iterations_list:
        print(f"\nExecutando benchmark com {iterations} iterações...")

        time_measurements = []
        cpu_measurements = []
        memory_measurements = []

        for rep in range(repetitions):
            print(f"  Repetição {rep + 1}/{repetitions}")
            measurements = []

            # Coletar medições para cada iteração
            for _ in range(iterations):
                time.sleep(0.1)
                measurement = measure_resources(func, *args)
                measurements.append(measurement)

            # Calcular médias para esta repetição
            if measurements:  # Verificar se há medições
                avg_time = statistics.mean(m['time'] for m in measurements)
                avg_cpu = statistics.mean(m['cpu'] for m in measurements)
                avg_memory = statistics.mean(m['memory'] for m in measurements)

                time_measurements.append(avg_time)
                cpu_measurements.append(avg_cpu)
                memory_measurements.append(avg_memory)

        # Calcular estatísticas para todas as repetições
        results[iterations] = {
            'time': {
                'mean': utils.format_duration(statistics.mean(time_measurements)),
                'std_dev': utils.format_duration(statistics.stdev(time_measurements)),
                'median': utils.format_duration(statistics.median(time_measurements)),
                'min': utils.format_duration(min(time_measurements)),
                'max': utils.format_duration(max(time_measurements))
            },
            'cpu': {
                'mean': f"{statistics.mean(cpu_measurements):.2f}%",
                'std_dev': f"{statistics.stdev(cpu_measurements):.2f}%",
                'median': f"{statistics.median(cpu_measurements):.2f}%",
                'min': f"{min(cpu_measurements):.2f}%",
                'max': f"{max(cpu_measurements):.2f}%"
            },
            'memory': {
                'mean': utils.format_memory(statistics.mean(memory_measurements)),
                'std_dev': utils.format_memory(statistics.stdev(memory_measurements)),
                'median': utils.format_memory(statistics.median(memory_measurements)),
                'min': utils.format_memory(min(memory_measurements)),
                'max': utils.format_memory(max(memory_measurements))
            }
        }

    return results


def main():
    key_sizes = [2048, 4096]
    libraries = ["cryptography", "pycryptodome"]
    message = b'a' * 190
    iterations_list = [1]
    repetitions = 2

    for lib in libraries:
        for key_size in key_sizes:
            if lib == "cryptography":
                key_gen_func = cryptography.generate_key
            else:
                key_gen_func = pycryptodome.generate_key

            utils.print_benchmark_header(
                "Geração de Chaves",
                key_size,
                lib,
                iterations_list
            )

            results = benchmark(
                key_gen_func,
                key_size,
                iterations_list=iterations_list,
                repetitions=repetitions
            )

            for iterations, metrics in results.items():
                print(f"\nIterações: {iterations}")
                utils.print_benchmark_results("Tempo de Execução", {
                    'Tempo': metrics['time']})
                utils.print_benchmark_results(
                    "Uso de CPU", {'CPU': metrics['cpu']})
                utils.print_benchmark_results(
                    "Uso de Memória", {'Memória': metrics['memory']})

            # Gerar um par de chaves para os próximos testes
            private_key, public_key = key_gen_func(key_size)

            # Benchmark de cifração
            if lib == "cryptography":
                encrypt_func = cryptography.encrypt
            else:
                encrypt_func = pycryptodome.encrypt

            utils.print_benchmark_header(
                "Cifração", key_size, lib, iterations_list)
            results = benchmark(
                encrypt_func,
                message,
                public_key,
                iterations_list=iterations_list,
                repetitions=repetitions
            )

            for iterations, metrics in results.items():
                print(f"\nIterações: {iterations}")
                utils.print_benchmark_results("Tempo de Execução", {
                    'Tempo': metrics['time']})
                utils.print_benchmark_results(
                    "Uso de CPU", {'CPU': metrics['cpu']})
                utils.print_benchmark_results(
                    "Uso de Memória", {'Memória': metrics['memory']})

            # Preparar para decifração
            ciphertext = encrypt_func(message, public_key)

            # Benchmark de decifração
            if lib == "cryptography":
                decrypt_func = cryptography.decrypt
            else:
                decrypt_func = pycryptodome.decrypt

            utils.print_benchmark_header(
                "Decifração", key_size, lib, iterations_list)
            results = benchmark(
                decrypt_func,
                ciphertext,
                private_key,
                iterations_list=iterations_list,
                repetitions=repetitions
            )

            for iterations, metrics in results.items():
                print(f"\nIterações: {iterations}")
                utils.print_benchmark_results("Tempo de Execução", {
                    'Tempo': metrics['time']})
                utils.print_benchmark_results(
                    "Uso de CPU", {'CPU': metrics['cpu']})
                utils.print_benchmark_results(
                    "Uso de Memória", {'Memória': metrics['memory']})


if __name__ == "__main__":
    main()
