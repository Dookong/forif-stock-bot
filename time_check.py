import time

time_info = time.gmtime()

m_hour = time_info.tm_hour
m_min = time_info.tm_min

print(f"{m_hour}시 {m_min}분")
