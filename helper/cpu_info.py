import psutil

cpu = psutil.cpu_freq()
print(f"CPU속도: {cpu.current}")

cpu_core = psutil.cpu_count(logical=False)
print(f"CPU코어: {cpu_core}")

memory = psutil.virtual_memory()
print(f"램: {memory.total / (1024**3)}GB")

disk = psutil.disk_usage(psutil.disk_partitions()[0].mountpoint)
print(f"디스크: {disk.total / (1024**3)}GB")

