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
    config = str("\n".join(config.split("\n")[1:-2]))
    return config


def get_config(device):
    ssh = ssh_connection(device["ip"], device["username"], device["password"])
    if device["enable"] is not None:
        shell = ssh_enable(ssh, device["enable"])
    else:
        shell = ssh.invoke_shell()
    ssh_command(shell, "configure")
    config = ssh_command(shell, "show | no-more")
    ssh_command(shell, "exit")
    ssh_command(shell, "exit")
    config = clean_config(config)
    return config
