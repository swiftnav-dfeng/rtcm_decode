class BaseDriver:
    def __init__(self):
        pass

    def read(self, bytes: int):
        # read num of bytes
        pass
    
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'exc_type {exc_type} exc_val {exc_val} exc_tb {exc_tb}' )