from time import time_ns
def metrics(func):    
    def proc_time():
        start = time_ns()
        func()
        return time_ns() - start
    
    return proc_time