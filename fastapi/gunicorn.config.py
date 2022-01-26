from multiprocessing import cpu_count

workers = cpu_count()
bind = "0.0.0.0:8001"
keepalive = 120
errorlog = "-"
loglevel = "error"
