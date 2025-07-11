from src.db.connection import get_connection, user
from src.services.data_processor import executeInsert
from src.services.update import executeUpdate
from src.utils import messages
import sys
import os
import msvcrt


if get_connection():
    while True:
        messages.homeMenu(user)
        selectOptions = msvcrt.getch().decode()

        if selectOptions == '1':
            os.system('cls')
            executeInsert()
            
        elif selectOptions == '2':
            os.system('cls')
            executeUpdate()

        elif selectOptions == '0':
            os.system('cls')
            break
        else:
            os.system('cls')