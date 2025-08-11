from src.services import cleanup_tasks
import os
import glob

path = "out"
log_path = f"src/resources/{path}"
json_path = f"src/json/string_connection.json"

def start(con):

    if os.path.isdir(log_path) == False:
        try:
            os.makedirs(log_path)
        except FileExistsError as e:
            return f"Erro: {e}"

    files = glob.glob(os.path.join(log_path, "*"))

    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            return f"Erro: {e}"

    cleanup_tasks.cleaner(con)

def  init():
    if os.path.isdir(json_path) == False:
        try:
            os.makedirs(json_path)
        except FileExistsError as e:
            return f"Erro: {e}"
    
    files = glob.glob(os.path.join(json_path, "*"))
