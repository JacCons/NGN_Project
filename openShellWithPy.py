import subprocess
import sys

class open_terminal:
    def __init__(self):
        match sys.platform:
            case "win32":
                echo_command = 'Write-Host Next Generation Networking Project\n\r'
                echo_command += 'Write-Host Password: vagrant'
                powershell_command = f"Start-Process powershell -ArgumentList '-Command \"{echo_command}; ssh -X -p 2222 vagrant@localhost\"'"

                subprocess.Popen(["powershell", "-Command", powershell_command])
            case "darwin":
                # subprocess.Popen(["open", "-a", "Terminal"])
                command = "echo \"Next Generation Networking Project\n\""
                command += "echo \"Password: vagrant\""
                command += "ssh -X -p 2222 vagrant@localhost"
                subprocess.Popen(["osascript", "-e", f'do shell script "{command}"'])
            case "linux":
                subprocess.Popen(["gnome-terminal"])

# open_terminal()


# import subprocess

# def run_powershell_command(command):
#     subprocess.Popen(["powershell", "-Command", command])

# command = "Write-Host 'Hello, world!'; echo ciao"
# run_powershell_command(command)