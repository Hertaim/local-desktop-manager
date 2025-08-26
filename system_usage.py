import psutil

def get_usage_data() -> dict:

    #TODO create an option for user to choose what storage (or all storages) he wants to use 
    
    storage = psutil.disk_usage('D:/')
    cpu = psutil.cpu_percent(1)
    ram = psutil.virtual_memory()

    usage_stats = {
        'ram_total' : f'{int(ram.total / (1024**3))} GB total',
        'ram_used' : int(ram.used / (1024**3)),
        'ram_percent' : f'{ram.percent}%',
        'cpu_percent' : f'{cpu}%',
        'storage_total' : f'{int(storage.total / (1024**3))} GB total',
        'storage_used' : int(storage.used / (1024**3)),
        'storage_percent' : f'{storage.percent}%'
    }
 
    return usage_stats

