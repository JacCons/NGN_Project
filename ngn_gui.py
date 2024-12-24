import tkinter
import tkinter.messagebox
import customtkinter
import subprocess
from openShellWithPy import myClass

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue" !!!


class App(customtkinter.CTk):
    
    myClass.start_controller()
    myClass.open_terminal()

    def __init__(self):
        super().__init__()
    
        #Configurazione della finestra
        self.title("NGN Project")
        self.geometry(f"{1100}x{600}")


        #Configurazione a griglia della finestra
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        #Barra laterale "Create a new network"
        self.sidebar_framesx = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_framesx.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_framesx.grid_rowconfigure(6, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_framesx, text="Create a new network", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # *** Topologia Custom, da togliere le segeunti righe ***
        # self.topo_frame = customtkinter.CTkFrame(self.sidebar_framesx)
        # self.topo_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        # self.sidebar_topo = customtkinter.CTkLabel(self.topo_frame, text="Topos:")
        # self.sidebar_topo.grid(row=0, column=0, padx=20, pady=(10,0))
        # self.sidebar_entrytopo = customtkinter.CTkOptionMenu(self.topo_frame, values=["Single", "Linear", "Tree", "Torus"])
        # self.sidebar_entrytopo.grid(row=1, column=0, padx=20, pady=(10,10))

        self.host_frame = customtkinter.CTkFrame(self.sidebar_framesx)
        self.host_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.sidebar_numhost = customtkinter.CTkLabel(master=self.host_frame, text="Number of hosts:")
        self.sidebar_numhost.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.sidebar_entrynumhost = customtkinter.CTkEntry(master=self.host_frame)
        self.sidebar_entrynumhost.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.switch_frame = customtkinter.CTkFrame(self.sidebar_framesx)
        self.switch_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.sidebar_numswitch = customtkinter.CTkLabel(master=self.switch_frame, text="Number of switches:")
        self.sidebar_numswitch.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.sidebar_entrynumswitch = customtkinter.CTkEntry(master=self.switch_frame)
        self.sidebar_entrynumswitch.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # *** Topologia Custom, da togliere le segeunti righe  e la funzione associata create_button_event() sotto***
        # self.create_button = customtkinter.CTkButton(self.sidebar_framesx, text="CREATE", font=customtkinter.CTkFont(size=15, weight="bold"), command = self.create_button_event)
        # self.create_button.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

        #Status Box
        self.statusbox = customtkinter.CTkTextbox(self, height=200)
        self.statusbox.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Imposta la textbox come sola lettura
        self.statusbox.configure(state="normal")  # Cambia lo stato a 'normal'
        self.statusbox.insert("end", "Questa status box ora è in modalità solo lettura")  # Inserisci il testo
        self.statusbox.configure(state="disabled")  # Reimposta lo stato a 'disabled'

        #self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        #self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


        #Architettura di rete
        self.networkarch = customtkinter.CTkLabel(self, text="Network's architecture:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.networkarch.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nw")

        #Servizi
        self.sidebar_framedx = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_framedx.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_framedx.grid_rowconfigure(6, weight=1)

        self.services_label = customtkinter.CTkLabel(self.sidebar_framedx, text="Services", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.services_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        self.service1_button = customtkinter.CTkButton(self.sidebar_framedx, text="DATA E ORA", font=customtkinter.CTkFont(size=15, weight="bold"), height=40)
        self.service1_button.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.service2_button = customtkinter.CTkButton(self.sidebar_framedx, text="NUMERO FORTUNATO", font=customtkinter.CTkFont(size=15, weight="bold"), height=40)
        self.service2_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.service3_button = customtkinter.CTkButton(self.sidebar_framedx, text="FRASE DEL GIORNO", font=customtkinter.CTkFont(size=15, weight="bold"), height=40)
        self.service3_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.service4_button = customtkinter.CTkButton(self.sidebar_framedx, text="GIRA LA RUOTA!", font=customtkinter.CTkFont(size=15, weight="bold"), height=40)
        self.service4_button.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.stopall_button = customtkinter.CTkButton(self.sidebar_framedx, text="STOP ALL SERVICES", font=customtkinter.CTkFont(size=15, weight="bold"), height=40)
        self.stopall_button.grid(row=6, column=0, padx=20, pady=(20, 20), sticky="s")
       
        #self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        # self.checkbox_3.configure(state="disabled")
        # self.checkbox_1.select()
        # self.scrollable_frame_switches[0].select()
        # self.scrollable_frame_switches[4].select()
        # self.radio_button_3.configure(state="disabled")
        #self.appearance_mode_optionemenu.set("Dark")
        #self.scaling_optionemenu.set("100%")
        # self.optionmenu_1.set("CTkOptionmenu")
        # self.combobox_1.set("CTkComboBox")
        # self.slider_1.configure(command=self.progressbar_2.set)
        # self.slider_2.configure(command=self.progressbar_3.set)
        # self.progressbar_1.configure(mode="indeterminnate")
        # self.progressbar_1.start()
        self.statusbox.insert("0.0", "Status Box\n\n")
        # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        # self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    # def create_button_event(self):
    #     topo = self.sidebar_entrytopo.get()
    #     flags = "--mac --switch=ovsk,protocols=OpenFlow13 --controller=remote"
    #     match topo:
    #         case "Single":
    #             print(f"sudo mn --topo {topo},{self.sidebar_entrynumhost.get()} {flags}")
    #         case "Linear":
    #             print(f"sudo mn --topo {topo},{self.sidebar_entrynumswitch.get()},{self.sidebar_entrynumhost.get()} {flags}")
    #         #case "Reversed":
    #             #print(f"sudo mn --topo {topo},{self.sidebar_entrynumhost.get()} {flags}")
    #         case "Tree":
    #             print(f"sudo mn --topo {topo},{self.sidebar_entrynumswitch.get()},{self.sidebar_entrynumhost.get()} {flags}")
    #         case "Torus":
    #             print(f"sudo mn --topo {topo},{self.sidebar_entrynumswitch.get()},{self.sidebar_entrynumhost.get()} {flags}")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
