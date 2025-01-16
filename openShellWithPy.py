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
        try:
            # Comando da eseguire in un nuovo terminale
            command = (
                "sudo mn -c && sudo su -c "
                "\"sudo cp /media/sf_NGN_Project/simple_switch_stp_13.py /home/vagrant/comnetsemu_dependencies/ryu-v4.34/ryu/ryu/app/NGN_simple_switch_custom.py &&"
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


    def start_mininet(): 
        try:
            # Comando da eseguire in un nuovo terminale
            command = (
                "sudo python3 /media/sf_NGN_Project/topology_generator.py --arp"
            )
            
            # Apri un nuovo terminale ed esegui il comando
            subprocess.Popen(
                ["xterm", "-e", f"{command}; bash"]
            )
            print("Mininet started in a new terminal")
        except Exception as e:
            print(f"Error: {e}")

myClass.start_controller()
