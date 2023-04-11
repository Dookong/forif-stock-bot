import time
import psutil
from helper.utils import MessageSender

cpus = []
for i in range(5):
    cpus.append(psutil.cpu_percent(1))
    
memory = psutil.virtual_memory()
disk = psutil.disk_usage(psutil.disk_partitions()[0].mountpoint)


message = f'''
서버시간: {time.strftime('%Y-%m-%d %H:%M:%S')}
CPU 사용률: {sum(cpus) // len(cpus)}%
RAM 사용률: {round(memory.used / memory.total * 100, 1)}%
'''

sender = MessageSender()
sender.send(message)