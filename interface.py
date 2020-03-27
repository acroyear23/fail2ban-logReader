# Basic ASCII interface module for fail2ban log reader
def banner():
    print("---------------------------------------------------")
    print("   Welcome to the Fail2ban Log Reader & Archiver")
    print("---------------------------------------------------")


def choice_1():
    print("Please select one of the following options:")
    print()
    print("(1)REMOTE/ssh to logs    (2)LOCAL logs")
    print("(3)VIEW database         (4)DELETE database")
    print("(5)SORT/VIEW options     (6)PRINT to file")
    print("(7)quit")
    print()


def sort_view():
    print()
    print("(1)HOST       (2)DATE       (3)TIME")
    print("(4)MESSAGE    (5)SERVICE    (6)BAN_STATUS")
    print("(7)OFFENDER IP              (8)back")
    print()
