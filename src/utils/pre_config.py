from src.services import cleanup_tasks
import os
import glob

path = "out"
log_path = f"src/resources/{path}"

def start(con):

    if os.path.isdir(log_path) == False:
        try:
            os.makedirs(log_path)
        except FileExistsError:
            print(f"pasta criada: {log_path}")

    files = glob.glob(os.path.join(log_path, "*"))
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            return 

    cleanup_tasks.cleaner(con)