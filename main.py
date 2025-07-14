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
            messages.terminalCleaning()
            executeInsert()
            
        elif selectOptions == '2':
            messages.terminalCleaning()
            executeUpdate()

        elif selectOptions == '0':
            messages.terminalCleaning()
            break
        else:
            messages.terminalCleaning()