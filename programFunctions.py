import os
# local modules
from Sqlite3Class import *
import interface


# Function to print Column header for terminal views
def print_header():
    print("[#]  "
          "[HOST_IP]      [DATE]        [TIME]"
          "      [MESSAGE]       [SERVICE]"
          " [BAN]    [OFFENDER_IP]")


# Choice function on main.py to VIEW DATABASE based on db ENTRY#
def view_database():
    os.system("clear")
    interface.banner()
    print()
    db = Sqlite3()
    print_header()
    for row in db.view_db():
        print(row)


def enter_continue():
    print()
    input("Press Enter to continue...")


# Choice function on main.py to print DATABASE to FILE
def print_to_file():
    os.system("clear")
    interface.banner()
    print()
    file_name = str(input("Enter NAME of file to print database to:"))
    print()
    print_header()
    db = Sqlite3()
    for row in db.view_db():
        with open(file_name, 'a') as file:
            print(row)
            file.write(str(row) + "\n")
    print()
    print("Database written to file: {}".format(file_name))


# Choice function on main.py for SORT/VIEW options of DATABASE
def sort_main_choice():
    while True:
        try:
            os.system("clear")
            interface.banner()
            interface.sort_view()
            sort = sort_db()
            if sort == "back":
                break
            print_header()
            db = Sqlite3()
            rows = db.view_sort(sort)
            for row in rows:
                print(row)
            enter_continue()
        except:
            print("Input ERROR, try again")
        break


# Choice function on main.py to DELETE database and confirm
def delete_database():
    answer = str(input("Are you sure you want to delete fail2ban.db?(y/N):"))
    if answer == "y" or answer == "Y":
        os.system("rm fail2ban.db")
        print("fail2ban.db DELETED")
    else:
        print("fail2ban.db NOT deleted")


# SORTING methods that RETURNS the variable SORT to the
# view_sort() method in Sqlite3Class.py
def sort_db():
    answer = int(input("Enter database SORTING method to view:"))
    print()
    if answer == 1:
        sort = "SELECT * FROM fail2ban_table ORDER BY host ASC"
    if answer == 2:
        sort = "SELECT * FROM fail2ban_table ORDER BY date ASC"
    if answer == 3:
        sort = "SELECT * FROM fail2ban_table ORDER BY time ASC"
    if answer == 4:
        sort = "SELECT * FROM fail2ban_table ORDER BY message ASC"
    if answer == 5:
        sort = "SELECT * FROM fail2ban_table ORDER BY service ASC"
    if answer == 6:
        sort = "SELECT * FROM fail2ban_table ORDER BY ban_status ASC"
    if answer == 7:
        sort = "SELECT * FROM fail2ban_table ORDER BY ip ASC"
    if answer == 8:
        sort = "back"
    return sort
