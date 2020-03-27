import os
import interface
import socket
# local module
import logparsingFunctions


# Function called when reading from local log files
# where program is run.

def local_logfiles():
    os.system("clear")
    interface.banner()
    print()
    host_ip = socket.gethostbyname(socket.gethostname())
    dir_listing, directory = logparsingFunctions.get_directory_location()
    logparsingFunctions.add_files_to_db(dir_listing, directory, host_ip)
