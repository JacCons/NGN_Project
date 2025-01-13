import subprocess 
import time
import os


# localhost credentials: vagrant@localhost:2222
hostname = "localhost" 
username = "vagrant" 
password = "vagrant" 
port = 2222
simple_switch_custom_name = "NGN_simple_switch_custom.py"

class myClass:
    
    def start_controller():
        
        # print("Starting Ryu-manager...\n")
        # # Create an SSH client instance 
        # client = paramiko.SSHClient() 
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                
        # # Connect to the server 
        # try:
        #     client.connect(hostname, username=username, password=password, port=port)
        #     print("Connected to the server")
        # except Exception as e:
        #     print(f"Error connecting to the server: {e}")
        #     return
        
        # #stdin, stdout, stderr = client.exec_command(f"sudo mn -c \n sudo su \n sudo cp /media/sf_shared_NGN_Project/simple_switch_stp_13.py /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/NGN_simple_switch_custom.py \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/ \n sudo ryu-manager NGN_simple_switch_custom.py", timeout=20)
   
        # stdin, stdout, stderr = client.exec_command("cd /media/sf_NGN_Project \n cp ./simple_switch_stp_13.py /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/NGN_simple_switch_custom.py ")
        # print("Output cp:", stdout.read().decode())
        # print("Errori cp:", stderr.read().decode())
        # client.exec_command("sudo mn -c \n sudo su \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app \n ryu-manager NGN_simple_switch_custom.py", timeout=10)
        # print("Command executed")
        # print("Ryu-manager started\n")
        # try:
        #     # Comando da eseguire in background
        #     command = (
        #         "sudo mn -c && sudo su -c "
        #         "\"cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app && "
        #         "ryu-manager NGN_simple_switch_custom.py\" > /path/to/logfile.log 2>&1 &"
        #     )
        #     # Esegui il comando
        #     subprocess.Popen(command, shell=True)
        #     print("Command executed")
        #     print("Ryu-manager started\n")
        # except Exception as e:
        #     print(f"Error: {e}")

        # try:
        #     # Comando da eseguire in background con screen
        #     command = (
        #         "screen -dmS ryu_manager bash -c "
        #         "\"cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app && "
        #         "ryu-manager NGN_simple_switch_custom.py\""
                

        #     )

        #     # Esegui il comando
        #     subprocess.Popen(command, shell=True)
        #     print("Ryu-manager started in screen session\n")
        #     time.sleep(3)
        # except Exception as e:
        #     print(f"Error: {e}")
        



        try:
            # Comando da eseguire in un nuovo terminale
            command = (
                "sudo mn -c && sudo su -c "
                "\"sudo cp /media/sf_NGN_Project/simple_switch_stp_13.py /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/NGN_simple_switch_custom.py \n cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/ \n sudo ryu-manager NGN_simple_switch_custom.py &&"
                "cd /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app && "
                "ryu-manager NGN_simple_switch_custom.py\""
            )
            
            # Apri un nuovo terminale ed esegui il comando
            subprocess.Popen(
                ["xterm", "-e", f"{command}; bash"]
            )
            print("Command executed in a new terminal")
            print("Ryu-manager started\n")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(3)


    # def open_terminal(): 
    #     try:
    #         # Comando da eseguire in un nuovo terminale
    #         command = (
    #             "sudo python3 /media/sf_NGN_Project/topology_generator.py"
    #         )
            
    #         # Apri un nuovo terminale ed esegui il comando
    #         subprocess.Popen(
    #             ["xterm", "-e", f"{command}; bash"]
    #         )
    #         print("Mininet started in a new terminal")
    #     except Exception as e:
    #         print(f"Error: {e}")

    def start_mininet(): 
        try:
            # Comando da eseguire in un nuovo terminale
            command = (
                "sudo python3 /media/sf_NGN_Project/topology_generator.py"
            )
            
            # Apri un nuovo terminale ed esegui il comando
            subprocess.Popen(
                ["xterm", "-e", f"{command}; bash"]
            )
            print("Mininet started in a new terminal")
        except Exception as e:
            print(f"Error: {e}")

        

myClass.start_controller()
# myClass.open_terminal()
