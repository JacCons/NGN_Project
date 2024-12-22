import subprocess
import sys
import paramiko 


# localhost credentials: vagrant@localhost:2222
hostname = "localhost" 
username = "vagrant" 
password = "vagrant" 
port = 2222
simple_switch_custom_name = "NGN_simple_switch_custom.py"

class myClass:
    
    def start_controller():
        
        print("\nStarting ryu-manager...\n")
        
        # Create an SSH client instance 
        client = paramiko.SSHClient() 
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        
        # Connect to the server 
        try:
            client.connect(hostname, username=username, password=password, port=port)
            print("Connected to the server")
        except Exception as e:
            print(f"Error connecting to the server: {e}")
            return
        
        client.exec_command("sudo mn -c \n sudo su \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_13.py", timeout=10)
        print("Command executed")

        # client.exec_command("sudo mn -c \n sudo su \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_stp_13.py", timeout=10)
        # print("Command executed")

        
        # try:
        #     command = (
        #         "sudo mn -c \n"
        #         f"sudo cp /media/sf_shared_NGN_Project/simple_switch_stp_13.py /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/{simple_switch_custom_name} \n"
        #         "cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n"
        #         f"ryu-manager {simple_switch_custom_name}"
        #     )
        #     # stdin, stdout, stderr = client.exec_command(f"sudo mn -c \n sudo su \n sudo cp /media/sf_shared_NGN_Project/simple_switch_stp_13.py /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/NGN_simple_switch_custom.py \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager NGN_simple_switch_custom.py", timeout=20)
        #     # stdin, stdout, stderr = client.exec_command(f"sudo mn -c \n sudo su \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_13.py", timeout=20)

        #     # client.exec_command(f"ryu-manager {simple_switch_custom_name}", timeout=20)
        #     # client.exec_command(f"cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager {simple_switch_custom_name}", timeout=20)

        #     # stdin, stdout, stderr = client.exec_command("sudo mn -c \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_13.py", timeout=10)

            
            
        #     print("Command executed")
        # except Exception as e:
        #     print(f"Error executing command: {e}")
        #     return
        
        # # Read output in a non-blocking way
        # stdout.channel.settimeout(2)
        # stderr.channel.settimeout(2)

        # try:
        #     stdout_output = stdout.read()
        #     stderr_output = stderr.read()
        # except Exception as e:
        #     print(f"Error reading output: {e}")
        #     stdout_output = ""
        #     stderr_output = ""

        # if stderr_output:
        #     print(f"\nstderr:\n{stderr_output.decode()}")
        # if stdout_output:
        #     print(f"\nstdout:\n{stdout_output.decode()}")

        print("Ryu-manager started\n")

    def windows_open_terminal_and_insert_password():

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
