import customtkinter as ctk

class SimpleGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurazione finestra principale
        self.title("Network GUI")
        self.geometry("800x400")

        # Layout principale: colonne
        self.grid_columnconfigure(0, weight=1)

        # Campi di testo con etichette
        self.label1 = ctk.CTkLabel(self, text="Campo 1:")
        self.label1.grid(row=0, column=0, pady=10, padx=10)
        self.entry1 = ctk.CTkEntry(self) #è il box in cui inserire il testo
        self.entry1.grid(row=1, column=0, pady=5, padx=10)

        self.label2 = ctk.CTkLabel(self, text="Campo 2:")
        self.label2.grid(row=2, column=0, pady=10, padx=10)
        self.entry2 = ctk.CTkEntry(self)
        self.entry2.grid(row=3, column=0, pady=5, padx=10)

        self.label3 = ctk.CTkLabel(self, text="Campo 3:")
        self.label3.grid(row=4, column=0, pady=10, padx=10)
        self.entry3 = ctk.CTkEntry(self)
        self.entry3.grid(row=5, column=0, pady=5, padx=10)

        # Pulsante di invio colorato
        self.submit_button = ctk.CTkButton(
            self,
            text="Invia",
            fg_color="#4CAF50",  # Colore verde
            text_color="white",
            command=self.on_submit
        )
        self.submit_button.grid(row=6, column=0, pady=20, padx=10)

    def on_submit(self):
        # Recupera valori dai campi di testo
        value1 = self.entry1.get()
        value2 = self.entry2.get()
        value3 = self.entry3.get()
        print(f"Campo 1: {value1}, Campo 2: {value2}, Campo 3: {value3}")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modalità di default: "Dark", "Light", "System"
    ctk.set_default_color_theme("blue")  # Tema colori: "blue", "dark-blue", "green"

    app = SimpleGUI()
    app.mainloop()


