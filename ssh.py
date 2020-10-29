import sys
print(sys.version_info, '\n')
import paramiko

host = "192.168.0.168"
port = 22
username = "ethan"

file = open('password.txt', 'r')
password = file.read().strip()
file.close()
'''
client = None
try:
    client = SSHClient()
    client.load_system_host_keys()
    client.connect('ssh.example.com')
    stdin, stdout, stderr = client.exec_command('ls -l')
finally:
    if client:
        client.close()
'''        
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

stdin, stdout, stderr = ssh.exec_command('ls')
lines = stdout.readlines()
for line in lines:
    print(line, end='')
print()
print('end')

stdout.close()
stdin.close()
stderr.close()
ssh.close()



#from paramiko import SSHClient
#ssh = SSHClient()
#ssh.load_system_host_keys()
#ssh.connect('user@server:path')
