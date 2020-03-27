import paramiko
import os
import shutil
import getpass
import socket
import interface
import logparsingFunctions


# Function called when connecting to a remote host.
# Uses SSH/SFTP, copies fail2ban log files to local
# machine that ran script, reads files, parses, inserts
# database, then deletes the temp file location.

def ssh_connect():
    os.system('clear')
    interface.banner()
    print("-REMOTE SERVER CONNECTION-")
    print()
    while True:
        try:
            # Check for valid IP's by using socket module
            host_ip = input("Enter IP address:")
            socket.inet_aton(host_ip)
            break
        except socket.error:
            print("*** Not a valid IP, try again ***")
    while True:
        try:
            port = input("Enter SSH port(ENTER for DEFAULT:22):")
            if not port:
                port = 22
                print("-DEFAULT port 22 used-")
                break
            else:
                port = int(port)
                break
        except:
            print("*** PORT entry ERROR, try again ***")
    user = input("Enter USER name:")
    # Uses getpass module to hide password entry in terminal
    password = getpass.getpass(prompt="PASSWORD for {}@{}:{}:".format(user, host_ip, port), stream=None)
    print()
    try:
        # uses Paramiko module for SSH/SFTP to remote hosts
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host_ip, port, user, password)

        sftp = client.open_sftp()
        sftp.get('/var/log/fail2ban.log', "/home/boron/test")

        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('ls /var/log')
        ssh_list = ssh_stdout.read().decode("utf-8")

        lines = ssh_list.split("\n")
        # Creates temp folder on host for reading files
        os.mkdir("/tmp/fail2ban")
        for line in lines:
            if "fail2ban" in line:
                sftp.get('/var/log/' + line, "/tmp/fail2ban/" + line)

        dir_listing, directory = logparsingFunctions.get_directory_location_remote()
        logparsingFunctions.add_files_to_db(dir_listing, directory, host_ip)

        # Deletes temp folder after reading files
        shutil.rmtree("/tmp/fail2ban")
        sftp.close()
        client.close()
    except:
        print()
        print("*** SSH Connection ERROR. Try again ***")
