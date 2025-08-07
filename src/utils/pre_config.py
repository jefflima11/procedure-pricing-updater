import os

path = "out"
log_path = f"src/resources/{path}"

def start():

    if os.path.isdir(log_path) == False:
        try:
            os.makedirs(log_path)
        except FileExistsError:
            print(f"pasta criada: {log_path}")
