import tkinter
import tkinter.messagebox
import customtkinter
from openShellWithPy import myClass
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
import os
import time
import requests

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Titles of services buttons
service_date = "Date"
service_date_time = "Date and Time"
lucky_number = "Lucky Number"
daily_quote = "Daily Quote"
two_steps_service = "2 Steps Service"

Directories = {
    'serv1': 'Servers/server1.txt',
    'serv2': 'Servers/server2.txt',
    'serv3': 'Servers/server3.txt',
    'serv4': 'Servers/server4.txt',
}

class App(customtkinter.CTk):
    
    myClass

    def __init__(self):
        super().__init__()

        # Inizialization services configuration: all services are off
        with open(Directories["serv1"], "w") as f:
            f.write("off")
        with open(Directories["serv2"], "w") as f: 
            f.write("off")
        with open(Directories["serv3"], "w") as f:
            f.write("off")
        with open(Directories["serv4"], "w") as f:  
            f.write("off") 
    
        # Window configuration
        self.title("NGN Project")
        self.geometry(f"{1100}x{600}")
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # SIDEBAR ON THE LEFT

        # Structure
        self.sidebar_framesx = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_framesx.grid(row=0, column=0, rowspan=4, sticky="nsew") 
        self.sidebar_framesx.grid_rowconfigure(7, weight=1)

        # Title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_framesx, text="Create network", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        # Frame for the number of hosts (consists of a label and an entry)
        self.host_frame = customtkinter.CTkFrame(self.sidebar_framesx)
        self.host_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.numhost = customtkinter.CTkLabel(master=self.host_frame, text="Number of hosts:", font=customtkinter.CTkFont(size=15))
        self.numhost.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.entrynumhost = customtkinter.CTkEntry(master=self.host_frame)
        self.entrynumhost.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Frame for the number of switches (consists of a label and an entry)
        self.switch_frame = customtkinter.CTkFrame(self.sidebar_framesx)
        self.switch_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.numswitch = customtkinter.CTkLabel(master=self.switch_frame, text="Number of switches:", font=customtkinter.CTkFont(size=15))
        self.numswitch.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.entrynumswitch = customtkinter.CTkEntry(master=self.switch_frame)
        self.entrynumswitch.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Create Topology Button 
        self.create_button = customtkinter.CTkButton(self.sidebar_framesx, text="CREATE topology", font=customtkinter.CTkFont(size=15, weight="bold"), height=40 , command = self.create_button_event)
        self.create_button.grid(row=7, column=0, padx=20, pady=20, sticky="sew") # row=7 to push the button to the bottom
        self.create_button.focus_set()

        # STATUS BOX
        self.statusbox = customtkinter.CTkTextbox(self, height=65)
        self.statusbox.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.statusbox.insert("end", "Questa status box ora è in modalità solo lettura") 
        self.statusbox.configure(state="disabled")  # Status box is read-only

        # NETWORK'S ARCHITECTURE
        self.center_frame = customtkinter.CTkFrame(self)
        self.center_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.networkarch = customtkinter.CTkLabel(self.center_frame, text="Network's architecture:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.networkarch.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    
        # Adjustments to fit the image to the frame
        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)

        # SIDEBAR ON THE RIGHT (SERVICES)

        # Structure
        self.sidebar_framedx = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_framedx.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_framedx.grid_rowconfigure(6, weight=1)
        
        # Title
        self.services_label = customtkinter.CTkLabel(self.sidebar_framedx, text="Services", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.services_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")
        
        # Buttons for the services
        self.service1_button = customtkinter.CTkButton(self.sidebar_framedx, text=service_date, font=customtkinter.CTkFont(size=15, weight="bold"), height=40 , command=lambda: self.event_services(self.service1_button, "Service selected:"))
        self.service1_button.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.service1_button.configure(fg_color="#c74c3c")

        self.service2_button = customtkinter.CTkButton(self.sidebar_framedx, text=lucky_number, font=customtkinter.CTkFont(size=15, weight="bold"), height=40 , command=lambda: self.event_services(self.service2_button, "Service selected:"))
        self.service2_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.service2_button.configure(fg_color="#c74c3c")

        self.service3_button = customtkinter.CTkButton(self.sidebar_framedx, text= daily_quote, font=customtkinter.CTkFont(size=15, weight="bold"), height=40 , command=lambda:self.event_services(self.service3_button, "Service selected:"))
        self.service3_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.service3_button.configure(fg_color="#c74c3c")        

        self.service4_button = customtkinter.CTkButton(self.sidebar_framedx, text= two_steps_service, font=customtkinter.CTkFont(size=15, weight="bold"), height=40 , command=lambda:self.event_services(self.service4_button, "Service selected:"))
        self.service4_button.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.service4_button.configure(state = "disabled")
        self.service4_button.configure(fg_color="#c74c3c")
        
        # Button to remove all flows
        self.remove_all_flows = customtkinter.CTkButton(self.sidebar_framedx, text="REMOVE all flows", font=customtkinter.CTkFont(size=15, weight="bold"), height=40 , command=lambda: self.event_services(self.remove_all_flows, "Button selected:"))
        self.remove_all_flows.grid(row=6, column=0, padx=20, pady=(20, 20), sticky="s")

        # Initial button configuration: disabled
        self.service1_button.configure(state = "disabled")
        self.service2_button.configure(state = "disabled")
        self.service3_button.configure(state = "disabled")
        self.remove_all_flows.configure(state = "disabled")
        

    # Function to delete all flows
    def delete_all_flows(self):
        try:
            response = requests.post('http://127.0.0.1:8080/simpleswitch/delete_flood_flows')
            if response.status_code == 200:
                tkinter.messagebox.showinfo("Success", "All flows deleted successfully")
            else:
                tkinter.messagebox.showerror("Error", "Failed to delete flows")
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to delete flows: {e}")


    # Function to manage the services
    def event_services(self, button, string):
        button_name = button.cget("text")
        self.statusbox.configure(state="normal")
        self.statusbox.delete("1.0", "end")
        self.statusbox.insert("end", f"{string} {button_name}\n")

        if button_name == service_date: # Selected service: Date
            try:
                with open(Directories["serv1"], "r") as f:
                    if f.read() == "on":                        
                        with open(Directories["serv1"], "w") as fi:                            
                            fi.write("off")
                            self.service1_button.configure(text=service_date, fg_color="#c74c3c")
                        with open(Directories["serv4"], "w") as fii:   
                            fii.write("off")           
                            self.service4_button.configure(state = "disabled")
                            self.service4_button.configure(fg_color="#c74c3c")  
                    else:
                        with open(Directories["serv1"], "w") as fi:
                            fi.write("on")
                            self.service1_button.configure(fg_color="#3f964b")
                            self.service4_button.configure(state = "normal")
            except:
                print("Error")
        if button_name == lucky_number: # Selected service: Lucky Number
            try:
                with open(Directories["serv2"], "r") as f:
                    if f.read() == "on":
                        with open(Directories["serv2"], "w") as fi:
                            fi.write("off")
                            self.service2_button.configure(fg_color="#c74c3c")
                    else:
                        with open(Directories["serv2"], "w") as fi:
                            fi.write("on")
                            self.service2_button.configure(fg_color="#3f964b")
            except:
                print("Error")
        if button_name ==  daily_quote: # Selected service: Daily Quote
            try:

                with open(Directories["serv3"], "r") as f:
                    if f.read() == "on":
                        with open(Directories["serv3"], "w") as fi:
                            fi.write("off")
                            self.service3_button.configure(fg_color="#c74c3c")
                    else:
                        with open(Directories["serv3"], "w") as fi:
                            fi.write("on")
                            self.service3_button.configure(fg_color="#3f964b")
            except:
                print("Error")   
        if button_name ==  two_steps_service: # Selected service: 2 Steps Service -> Date and Time
            try:
                with open(Directories["serv1"], "r") as f:
                    variable = f.read()
                
                if variable == "on":
                    with open(Directories["serv4"], "r") as fii:
                        var = fii.read()
                        if var == "on":
                            with open(Directories["serv4"], "w") as a:
                                a.write("off")
                                self.service4_button.configure(fg_color="#c74c3c")
                                self.service1_button.configure(text=service_date)
                        elif var == "off":
                            with open(Directories["serv4"], "w") as b:
                                b.write("on")
                                self.service4_button.configure(fg_color="#3f964b")
                                self.service1_button.configure(text=service_date_time)
                else:                    
                    with open(Directories["serv4"], "w") as fi: 
                        fi.write("off")    
                        self.service4_button.configure(state = "disabled")   
                        self.service4_button.configure(fg_color="#c74c3c") 
                
            except:
                print("Error")
        if button_name == "REMOVE all flows": # Selected button: Remove all flows
            self.delete_all_flows()
             

    # Function to create the network topology, the file "topology_generator.py" is executed
    def create_button_event(self):
        global numhost
        global numswitch

        try:
            numhost = int(self.entrynumhost.get())

            # Check if the number of hosts is at least 7
            if(numhost < 7):
                tkinter.messagebox.showinfo("Error", "Number of hosts must be at least 7")
                return

            numswitch = int(self.entrynumswitch.get())

            with open("topology_parameters.txt", "w") as f: # Write the number of hosts and switches in a file
                f.write(str(numhost))
                f.write("\n")
                f.write(str(numswitch))

            # Enable the services buttons
            self.service1_button.configure(state = "normal")
            self.service2_button.configure(state = "normal")
            self.service3_button.configure(state = "normal")
            self.remove_all_flows.configure(state = "normal")

            print("topology_parameters.txt created...")
            self.statusbox.configure(state="normal")
            self.statusbox.delete("1.0", "end")
            self.statusbox.insert("end", f"Number of hosts: {numhost}\nNumber of switches: {numswitch}\n")
            myClass.start_mininet()
        except ValueError:
            self.statusbox.configure(state="normal")
            self.statusbox.delete("1.0", "end")
            self.statusbox.insert("end", f"Error: Insert number of hosts and number of switches\n")
        
        time.sleep(7)

        # Display the network architecture

        image_path = "img/graph.png"

        if os.path.exists(image_path):
            print("L'immagine 'graph.png' esiste.")
            fig = Figure(dpi=200)
            ax = fig.add_subplot(111)
            img = mpimg.imread(image_path)
            ax.imshow(img)
            ax.axis('off')

            canvas = FigureCanvasTkAgg(fig, master=self.center_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=1, column=0, sticky="nsew")
            canvas.draw()
        else: 
            print("L'immagine 'graph.png' non esiste.")

    
    # Function to change the scaling of the widgets
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()
