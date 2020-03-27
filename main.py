import os
# local modules
import remoteConnect
import localConnect
import interface
import programFunctions


def main():
    while True:
        try:
            os.system("clear")
            interface.banner()
            interface.choice_1()
            choice = int(input("Choice:"))

            # Remote/ssh to logs
            if choice == 1:
                remoteConnect.ssh_connect()
                programFunctions.enter_continue()
            # Local logs
            if choice == 2:
                localConnect.local_logfiles()
                programFunctions.enter_continue()
            # View database
            if choice == 3:
                programFunctions.view_database()
                programFunctions.enter_continue()
            # Delete database
            if choice == 4:
                programFunctions.delete_database()
                programFunctions.enter_continue()
            # Sort/view database sub-menu
            if choice == 5:
                programFunctions.sort_main_choice()
            # Print to file
            if choice == 6:
                programFunctions.print_to_file()
                programFunctions.enter_continue()
            # Quit
            if choice == 7:
                break
        except:
            print()
            print("*** Entry ERROR. Try again... ***")
            programFunctions.enter_continue()

    os.system("clear")
    print("--------------------------------------------------")
    print(" Goodbye, and I'll miss you most of all scarecrow.")
    print("--------------------------------------------------")
    print()


if __name__ == "__main__":
    main()
