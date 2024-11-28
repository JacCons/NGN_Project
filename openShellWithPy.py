import subprocess
import sys
import paramiko 

# ssh -X -p 2222 vagrant@localhost
# sudo mn --topo single,3 --mac --switch=ovsk,protocols=OpenFlow13 --controller remote
# h1 ping -c 1 h2

# cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app
# ryu-manager simple_switch_13.py


# ! REMEMBER client.close() to close the SSH connection


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

        # Extecute the Ryu-controller with the simple_switch_13.py script
        client.exec_command("sudo mn -c \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_13.py", timeout=10) 
        # client.exec_command("sudo mn -c \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager simple_switch_13.py", timeout=10) 

        print("Ryu-manager started\n")
        #return client

    def start_mininet():
        
        print("Starting mininet...\n")

        # Create an SSH client instance 
        client = paramiko.SSHClient() 
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        
        # Connect to the server 
        client.connect(hostname, username=username, password=password, port=port) 

        # Create the mininet and ping
        stdin, stdout, stderr  = client.exec_command("sudo mn --topo single,3 --mac --switch=ovsk,protocols=OpenFlow13 --controller remote \n h1 ping -c 1 h2", timeout=10)

        # print("OUTPUT\n")
        # print(stdout.read())
        # print("ERROR\n")
        # print(stderr.read())

        print("Mininet started\n")
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

#open_terminal.start_controller()
myClass.start_controller()
#myClass.start_mininet()
myClass.open_terminal()

#
                   # do script "{command}"
                    #delay 1
                    #do script "{password}"  in front window 
                    #delay 1
                    #do script "sudo mn -c" in front window
                    #delay 1
                   # do script "{change_dir}"  in front window 
                    #delay 2

# import subprocess 

# def run_powershell_command(command):
#     subprocess.Popen(["powershell", "-Command", command])

# command = "Write-Host 'Hello, world!'; echo ciao"
# run_powershell_command(command)


#prevoiusly in darwin
# subprocess.Popen(["open", "-a", "Terminal"])
                #subprocess.Popen(["open", "-a", "Terminal"])
                # command = "echo \"Next Generation Networking Project\n\""
                # command += "echo \"Password: vagrant\""
                #command += "ssh -X -p 2222 vagrant@localhost"
                #subprocess.Popen(["osascript", "-e", f'do shell script "{command}"'])
                #print("Opening macOS Terminal for SSH interaction...\n")
                #subprocess.Popen(["open", "-a", "Terminal", "--args", "ssh", f"-p {port}", f"{username}@{hostname}"])