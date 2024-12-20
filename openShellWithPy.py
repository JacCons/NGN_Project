import subprocess
import sys
import paramiko 


# localhost credentials: vagrant@localhost:2222
hostname = "localhost" 
username = "vagrant" 
password = "vagrant" 
port = 2222

class myClass:
    
    def start_controller():
        
        print("Starting ryu-manager...\n")
        
        # Create an SSH client instance 
        client = paramiko.SSHClient() 
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        
        # Connect to the server 
        client.connect(hostname, username=username, password=password, port=port) 

        #Extecute the Ryu-controller with the simple_switch_13.py script
        stdin, stdout, stderr = client.exec_command("sudo mn -c \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_13.py", timeout=10) 

        # Read output in a non-blocking way
        stdout.channel.settimeout(2)
        stderr.channel.settimeout(2)

        try:
            stdout_output = stdout.read()
            stderr_output = stderr.read()
        except Exception as e:
            print(f"Error reading output: {e}")
            stdout_output = ""
            stderr_output = ""

        if stderr_output:
            print(stderr_output.decode())
        if stdout_output:
            print(stdout_output.decode())

        # stdin, stdout, stderr = client.exec_command("sudo mn -c \n cd /home \n ryu-manager simple_switch_13.py", timeout=10) 

        # # Read output in a non-blocking way
        # stdout.channel.settimeout(2)
        # stderr.channel.settimeout(2)

        # try:
        #     stdout_output = stdout.read()
        #     stderr_output = stderr.read()
        # except Exception as e:
        #     print(f"Error reading output: {e}\n")
        #     stdout_output = ""
        #     stderr_output = ""

        # if stderr_output:
        #     print(stderr_output.decode())
        # if stdout_output:
        #     print(stdout_output.decode())

        # print("Ryu-manager started\n")
        #return client

    def open_terminal_with_vagrant_console():

        echo_command = 'Write-Host Next Generation Networking Project\n\r'
        echo_command += 'Write-Host Password: vagrant'
        powershell_command = f"Start-Process powershell -ArgumentList '-Command \"ssh -X -p 2222 vagrant@localhost\"'"

        process = subprocess.Popen(["powershell", "-Command", powershell_command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # command = f"powershell -Command Start-Process powershell -ArgumentList '-Command  \"ssh -X -p {port} {username}@{hostname}\""

        # # Create a subprocess to run the PowerShell command
        # process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Send the password to the subprocess's standard input
        process.stdin.write(password.encode() + b'\n')
        process.stdin.flush()

        # Read the output and errors from the subprocess
        output, error = process.communicate()

        # Print the output and errors
        print(output.decode())
        print(error.decode())
        
        

      
    def open_terminal():
      # if(self.string_attr == "topology"):
        match sys.platform:
            case "win32":
                echo_command = 'Write-Host Next Generation Networking Project\n\r'
                echo_command += 'Write-Host Password: vagrant'
                powershell_command = f"Start-Process powershell -ArgumentList '-Command \"{echo_command}; ssh -X -p 2222 vagrant@localhost\"'"

                subprocess.Popen(["powershell", "-Command", powershell_command])
            case "darwin":
                
                print("Opening macOS Terminal for SSH interaction...\n")
                command = f'ssh -X -p {port} {username}@{hostname}'
                #change_dir = "cd /media/sf_NGN_Project \n ryu-manager simple_switch_13.py"
                change_dir = "cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_13.py"
                # Usando AppleScript per eseguire il comando SSH in una nuova finestra
                applescript = f'''                    
                    tell application "Terminal"
                    do script "{command}"
                    delay 1
                    do script "{password}" in front window
                    activate
                end tell'''

                subprocess.Popen(["osascript", "-e", applescript])      
            
            case "linux":
                subprocess.Popen(["gnome-terminal"])

myClass.start_controller()
myClass.open_terminal()
