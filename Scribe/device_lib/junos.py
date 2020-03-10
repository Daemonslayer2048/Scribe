import paramiko
import time

##############################################
# Definitions
def ssh_connection(host, user, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=password)
        return ssh
    except Exception as e:
        print("Connection Failed")
        print(e)


def ssh_command(shell, command):
    shell.send(command + "\n")
    time.sleep(0.5)
    std_out = shell.recv(102400).decode("ascii")
    return std_out


def clean_config(config):
    config = str("\n".join(config.split("\n")[5:-4]))
    return config


def get_config(device):
    ssh = ssh_connection(device.Device.ip, device.Device.user, device.Device.password)
    shell = ssh.invoke_shell()
    config = ssh_command(shell, "show configuration | no-more | display set")
    ssh_command(shell, "exit")
    config = clean_config(config)
    return config
