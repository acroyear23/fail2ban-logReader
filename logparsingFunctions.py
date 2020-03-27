from os import listdir
import gzip
import re
# local modules
import programFunctions
from Sqlite3Class import *


def get_directory_location():
    # Get fail2ban Log directory, DEFAULT is /var/log
    while True:
        try:
            print("Location of Fail2ban logs-")
            fail2ban_location = str(input("(ENTER for /var/log default):"))
            if fail2ban_location == "":
                fail2ban_location = "/var/log"
                print()
                break
            else:
                print()
                break
        except:
            print("Try again")

    return listdir(fail2ban_location), fail2ban_location


def get_directory_location_remote():
    # Remote logs are copied to local machine
    # in /temp/fail2ban and read from there
    fail2ban_location = "/tmp/fail2ban"
    return listdir(fail2ban_location), fail2ban_location


# --------- TEMP FILE CREATION ADD TO DB (below)--------

def add_files_to_db(dir_listing, directory, host_ip):
    temp_file = create_temp(dir_listing, directory)
    temp_file = split_temp_file(temp_file)
    temp_file = parse_ips(temp_file)
    temp_file = prepare_for_db(temp_file, host_ip)

    db = Sqlite3()
    db.insert_db(temp_file)
    programFunctions.print_header()
    for row in db.view_db():
        print(row)

# --------- TEMP FILE CREATION ADD TO DB (above)-------


# ----------TEMP FILE PARSING FUNCTIONS(begin)---------

def create_temp(dir_listing, dir):
    # Loops for looking at the files in directory and making sure only
    # fail2ban.log* files are used. Then differentiates between the
    # plain text files and those that are gzipped.
    temp_file = []
    for x, file in enumerate(dir_listing):
        if "fail2ban.log" in dir_listing[x] and "gz" in dir_listing[x]:
            with gzip.open(dir + "/" + dir_listing[x], 'r') as filegz:
                for line in filegz:
                    # Removes the printed 'b' and \n from un-gzipped files
                    line = line.decode("utf-8")
                    # Strips trailing whitespace and appends
                    temp_file.append(line.rstrip())
        if "fail2ban.log" in dir_listing[x] and "gz" not in dir_listing[x]:
            with open(dir + "/" + dir_listing[x], 'r') as filelog:
                for line in filelog:
                    # Strips trailing whitespace and appends
                    temp_file.append(line.rstrip())
    return temp_file


def split_temp_file(temp_file):
    # Separate out date(0),time(1),message(3)service(4), and IP/Ban
    # info(5-7) from temp_file then creates a new temp file
    temp_fileX = []
    for lineX in temp_file:
        newline = lineX.split()
        # fail2ban logs separated by multi-spaces.
        # Ip lands at index [7]
        if len(newline) >= 8:
            temp_line = newline[0] + "," + \
                        newline[1] + "," + \
                        newline[3] + "'" + \
                        newline[4] + "," + \
                        newline[5] + "," + \
                        newline[6] + "," + \
                        newline[7]
            temp_fileX.append(temp_line)
    return temp_fileX


def parse_ips(temp_file):
    # Regex function for  IP check in line ([] = no IP in line)
    temp_fileX = []
    for line in temp_file:
        if (re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)) != []:
            temp_fileX.append(line)
    return temp_fileX


# ----------TEMP FILE PARSING FUNCTIONS(end)----------

def prepare_for_db(temp_file, host_ip):
    # Prepares temp_file for insertion into database
    # by parsing IP lines only files and designating proper
    # columns for database. Adds host_ip to appended line.
    # (host_ip,date,time,message,service,ban status,ip)
    temp_filex = []
    for line in temp_file:
        if "already" in line:
            date, time, x, info, service, ip, ban_status = line.split(",")
            temp_filex.append(host_ip + "," +
                              date + "," +
                              time + "," +
                              info + "," +
                              service + "," +
                              ban_status + "," +
                              ip)
        else:
            date, time, x, info, service, ban_status, ip = line.split(",")
            temp_filex.append(host_ip + "," +
                              date + "," +
                              time + "," +
                              info + "," +
                              service + "," +
                              ban_status + "," +
                              ip)
    return temp_filex
