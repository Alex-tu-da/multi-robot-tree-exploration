from concurrent.futures import ThreadPoolExecutor

def worker(n):
    print(f"Starte Worker {n}")
    return n * n

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(worker, range(5)))

print(results)  # [0, 1, 4, 9, 16]
