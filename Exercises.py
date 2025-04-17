import customtkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import random
import sqlite3

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

numeri = "0123456789"
segni = "!@#$%^&*()"


def crea_db():
    conn = sqlite3.connect("utenti.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

crea_db()

def sign_up():
    window = customtkinter.CTk()
    window.title("Registrazione")
    
    frame = customtkinter.CTkFrame(master=window)
    frame.pack(padx=30, pady=50)
    
    label = customtkinter.CTkLabel(master=frame, text="Crea un account", font=("Arial", 16))
    label.pack(padx=10, pady=10)                  
    
    gmail = customtkinter.CTkEntry(master=frame, placeholder_text="Inserisci la gmail")
    gmail.pack(padx=10, pady=2)
    
    password = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password.pack(padx=10, pady=4)
    
    def mostra_password():
        if password.cget("show") == "*":
            password.configure(show="")
        else:
            password.configure(show="*")
    
    checkbox_mostra = customtkinter.CTkCheckBox(master=frame, text="Mostra password?", command=mostra_password)
    checkbox_mostra.pack(padx=3, pady=3)
    
    def registrati():
        email_inserita = gmail.get()
        password_inserita = password.get()
        
        if not email_inserita or not password_inserita:
            messagebox.showerror("Errore", "Compila tutti i campi!")
            return
        
        if "@" not in email_inserita or (".com" not in email_inserita and ".it" not in email_inserita):
            messagebox.showerror("Errore", "Email non valida! Usa '@' e '.com' o '.it'")
            return
        
        if len(password_inserita) <= 5:
            messagebox.showwarning("Password debole", "La password deve essere più lunga di 5 caratteri")
            return
        
        if (not any(car in numeri for car in password_inserita) and( not any(car in segni for car in password_inserita))):
            messagebox.showwarning("Password debole", "Aggiungi numeri e caratteri speciali")
            return

        try:
            conn = sqlite3.connect("utenti.db")
            c = conn.cursor()
            c.execute("INSERT INTO utenti (email, password) VALUES (?, ?)", (email_inserita, password_inserita))
            conn.commit()
            conn.close()
            messagebox.showinfo("Successo", "Registrazione completata!")
            window.destroy()
            accedi()
        except sqlite3.IntegrityError:
            messagebox.showerror("Errore", "Email già registrata!")

    btn_registrati = customtkinter.CTkButton(master=frame, text="REGISTRATI", command=registrati)
    btn_registrati.pack(padx=20, pady=10)
    
    window.mainloop()

def accedi():
    microsoft = customtkinter.CTk()
    microsoft.title("Accesso")
    
    frame = customtkinter.CTkFrame(master=microsoft)
    frame.pack(padx=20, pady=10)
    
    label = customtkinter.CTkLabel(master=frame, text="Accedi all'account",font=("Arial",16))
    label.pack(padx=20, pady=7)
    
    entry_email = customtkinter.CTkEntry(master=frame, placeholder_text="Email")
    entry_email.pack(padx=20, pady=4)
    
    entry_password = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    entry_password.pack(padx=20, pady=4)
    
    def mostra_password():
        if entry_password.cget("show") == "*":
            entry_password.configure(show="")
        else:
            entry_password.configure(show="*")
    
    checkbox_mostra = customtkinter.CTkCheckBox(master=frame, text="Mostra password?", command=mostra_password)
    checkbox_mostra.pack(padx=20, pady=2)
    
    def verifica_accesso():
        email_inserita = entry_email.get()
        password_inserita = entry_password.get()
        
        conn = sqlite3.connect("utenti.db")
        c = conn.cursor()
        c.execute("SELECT * FROM utenti WHERE email=? AND password=?", (email_inserita, password_inserita))
        result = c.fetchone()
        conn.close()
        
        if result:
            messagebox.showinfo("Accesso riuscito", "Benvenuto!")
            microsoft.destroy()
            show_app()
        else:
            messagebox.showerror("Errore", "Email o password errati!")

    btn_accedi = customtkinter.CTkButton(master=frame, text="ACCEDI", command=verifica_accesso)
    btn_accedi.pack(padx=20, pady=10)
    
    microsoft.mainloop()

def show_app():
    window = customtkinter.CTk()
    window.title("App")
    numeri = ("1234567890!£$%&/()=?^*é°ç:;_,.-+€[]@#")

    def impostazioni():
        if (text.get() =="")or(cognome.get()==""):
            messagebox.showerror(title="Credenziali",message="Seleziona il tuo nome e cognome") 
            return
        if (any(i in numeri for i in text.get())or(any (i in numeri for i in cognome.get()))):
            messagebox.showwarning(title="Caratteri",message="Non utilizzare numeri o caratteri speciali.")
            return
        if report.get("1.0", "end-1c").strip() == "":
            messagebox.showwarning(title="Messaggio", message="Per favore scrivi un messaggio prima di inviare.")
            return
        else:
            messagebox.showinfo(title="Report completato",message="Il report è stato inviato con successo.")
            text.delete(0,END)
            cognome.delete(0,END)
            report.delete("1.0",END)

    def delete():
        report.delete("1.0",END)

    frame = customtkinter.CTkFrame(master=window, width=350, height=320)
    frame.pack(padx=50, pady=50)

    text = customtkinter.CTkEntry(master=frame, placeholder_text="Nome", width=100)
    text.grid(row=0, column=0, padx=10, pady=10)

    cognome = customtkinter.CTkEntry(master=frame, placeholder_text="Cognome", width=100)
    cognome.grid(row=0, column=1, padx=10, pady=10)

    professioni = {"Designer", "Software Engineer", "Data-Scientist"}
    x = StringVar(value="Scegli")
    professione = customtkinter.CTkOptionMenu(master=frame, variable=x, values=[str(i) for i in professioni])
    professione.grid(row=0, column=2, padx=10, pady=10)

    info_bot= customtkinter.CTkButton(master=frame,text="?",width=10,height=5,command=bot)
    info_bot.grid(row=0,column=3,padx=10,pady=10)

    label = customtkinter.CTkLabel(master=frame, text="Scrivi un messaggio")
    label.grid(row=1, column=0, columnspan=3, padx=150, pady=(10, 0), sticky="WE")

    report = customtkinter.CTkTextbox(master=frame, height=150, width=250)
    report.grid(row=2, column=0,columnspan=3, padx=(20,10), pady=(0,10),sticky="WE")
    cancel = customtkinter.CTkButton(master=frame,text="🗑️",height=5,width=5,bg_color="black",fg_color="black",command=delete)
    cancel.grid(row=2,column=2,columnspan=4,padx=10,pady=10,sticky="SE")
    button = customtkinter.CTkButton(master=frame,text="Invio",command= impostazioni)
    button.grid(row=3,column=0,columnspan=3,padx=180,pady=20)

    def modalita():
        mode = customtkinter.get_appearance_mode()
        if mode == "Dark":
            customtkinter.set_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")

    made= customtkinter.CTkSwitch(master=frame,text="",width=10,command=modalita)
    made.grid(row=3,column=0,columnspan=2,padx=10,pady=20)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    window.mainloop()

def bot():
    custom_responses = {
        "chi ti ha creato": "Sono stato creato da Salvatore Naro! 😊",
        "chi sei": "Sono Chat-B Assistant, il tuo assistente virtuale personale",
        "ciao": "Ciao! Come posso aiutarti oggi?",
        "salve": "Salve! Sono qui per assisterti",
        "grazie": "Di nulla! È un piacere aiutarti 😊",
        "come stai": "Sto benissimo, grazie per avermelo chiesto!",
        "cosa ti occupi": "Mi occupo a rispondere alle domande di questo software 😊",
        "cose sto software": "Sono Chat-B Assistant,questo sofware si occupa delle ricerche ai per chat-b",
        "assistenza": "Quale il tuo problema,spiega.",
        "come va": "Sto benissimo, grazie per avermelo chiesto!"
    }

    bad_words = ["stupido", "idiota", "cretino", "fess", "coglione", "vaffanculo"]

    def contains_bad_word(message):
        """Controlla se il messaggio contiene parole volgari"""
        msg_lower = message.lower()
        return any(bad_word in msg_lower for bad_word in bad_words)

    def get_response(message):
        if contains_bad_word(message):
            return None
        
        msg_lower = message.lower()
        for key in custom_responses:
            if key in msg_lower:
                return custom_responses[key]
        
        random_responses = [
            "Interessante! Dimmi di più...",
            "Potresti riformulare la domanda?",
            "Posso aiutarti con altro?",
            "Sto ancora imparando, chiedimi qualcos'altro"
        ]
        return random.choice(random_responses)

    def update_chat(text, sender):
        chat_area.configure(state="normal")
        
        if sender == "Tu":
            chat_area.insert("end", f"Tu: {text}\n", "user")
        else:
            chat_area.insert("end", f"Bot: {text}\n", "bot")
        
        chat_area.see("end")
        chat_area.configure(state="disabled")

    def send_message(event=None):
        message = entry.get().strip()
        if not message:
            return
        
        if contains_bad_word(message):
            update_chat("Per favore mantieni un linguaggio educato.", "Bot")
            entry.delete(0, "end")
            return
        
        update_chat(message, "Tu")
        entry.delete(0, "end")
        
        response = get_response(message)
        if response:
            update_chat(response, "Bot")
        else:
            update_chat("Non posso rispondere a questo messaggio.", "Bot")

    def clear_chat():
        chat_area.configure(state="normal")
        chat_area.delete("1.0", "end")
        chat_area.configure(state="disabled")

    def show_help():
        help_window = customtkinter.CTkToplevel(app)
        help_window.title("Domande disponibili")
        help_window.geometry("400x300")
        help_window.resizable(False, False)
        
        help_text = "Ecco cosa posso rispondere:\n\n" + "\n".join(f"• {key.capitalize()}" for key in custom_responses)
        
        help_label = customtkinter.CTkLabel(help_window, text=help_text, 
                                font=("Segoe UI", 14), 
                                justify="left",
                                wraplength=380)
        help_label.pack(padx=20, pady=20, fill="both", expand=True)
        
        close_btn = customtkinter.CTkButton(help_window, text="Chiudi", 
                                command=help_window.destroy)
        close_btn.pack(pady=(0, 10),padx=20)

    app = customtkinter.CTk()
    app.title("🤖 Chat-B Assistant")
    app.geometry("850x900")
    app.minsize(750, 800)

    BG_COLOR = "#2b2b2b"
    USER_COLOR = "#3a3a3a"
    BOT_COLOR = "#1f1f1f"
    USER_TEXT_COLOR = "#f8f9fa" 
    BOT_TEXT_COLOR = "#4cc9f0"   

    main_frame = customtkinter.CTkFrame(app, fg_color=BG_COLOR)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    chat_area = customtkinter.CTkTextbox(main_frame, wrap="word", state="disabled",
                            fg_color=BOT_COLOR, font=("Segoe UI", 14), 
                            border_width=1, border_color="#3a3a3a")
    chat_area.pack(fill="both", expand=True, padx=5, pady=(0, 15))

    chat_area.tag_config("user", foreground=USER_TEXT_COLOR)
    chat_area.tag_config("bot", foreground=BOT_TEXT_COLOR)

    input_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
    input_frame.pack(fill="x", pady=(0, 10))

    entry = customtkinter.CTkEntry(input_frame, placeholder_text="Scrivi il tuo messaggio...",
                        fg_color=USER_COLOR, text_color=USER_TEXT_COLOR, 
                        font=("Segoe UI", 14), border_width=1,
                        border_color="#3a3a3a")
    entry.pack(side="left", fill="x", expand=True, padx=10)

    clear_btn = customtkinter.CTkButton(input_frame, text="🗑️", width=50,
                            fg_color="#d00000", hover_color="#9d0208",
                            font=("Segoe UI", 14))
    clear_btn.pack(side="right", padx=(0, 5))

    send_btn = customtkinter.CTkButton(input_frame, text="↑", width=50,
                            fg_color="#4361ee", hover_color="#3a0ca3",
                            font=("Segoe UI", 12, "bold"))
    send_btn.pack(side="right", padx=(5, 5))

    help_btn = customtkinter.CTkButton(input_frame, text="?", width=50,
                            fg_color="#7209b7", hover_color="#560bad",
                            font=("Segoe UI", 14, "bold"),
                            command=show_help) 
    help_btn.pack(side="right", padx=(5, 5))

    send_btn.configure(command=send_message)
    clear_btn.configure(command=clear_chat)
    entry.bind("<Return>", send_message)

    app.mainloop()
def app():
    numeri = "0123456789"
    segni = "!@#$%^&*()"


    def crea_db():
        conn = sqlite3.connect("utenti.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS utenti (
                email TEXT PRIMARY KEY,
                password TEXT
            )
        ''')
        conn.commit()
        conn.close()

    crea_db()

    def sign_up():
        window = customtkinter.CTk()
        window.title("Registrazione")
        
        frame = customtkinter.CTkFrame(master=window)
        frame.pack(padx=30, pady=50)
        
        label = customtkinter.CTkLabel(master=frame, text="Crea un account", font=("Arial", 16))
        label.pack(padx=10, pady=10)                  
        
        gmail = customtkinter.CTkEntry(master=frame, placeholder_text="Inserisci la gmail")
        gmail.pack(padx=10, pady=2)
        
        password = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
        password.pack(padx=10, pady=4)
        
        def mostra_password():
            if password.cget("show") == "*":
                password.configure(show="")
            else:
                password.configure(show="*")
        
        checkbox_mostra = customtkinter.CTkCheckBox(master=frame, text="Mostra password?", command=mostra_password)
        checkbox_mostra.pack(padx=3, pady=3)
        
        def registrati():
            email_inserita = gmail.get()
            password_inserita = password.get()
            
            if not email_inserita or not password_inserita:
                messagebox.showerror("Errore", "Compila tutti i campi!")
                return
            
            if "@" not in email_inserita or (".com" not in email_inserita and ".it" not in email_inserita):
                messagebox.showerror("Errore", "Email non valida! Usa '@' e '.com' o '.it'")
                return
            
            if len(password_inserita) <= 5:
                messagebox.showwarning("Password debole", "La password deve essere più lunga di 5 caratteri")
                return
            
            if (not any(car in numeri for car in password_inserita) and( not any(car in segni for car in password_inserita))):
                messagebox.showwarning("Password debole", "Aggiungi numeri e caratteri speciali")
                return

            try:
                conn = sqlite3.connect("utenti.db")
                c = conn.cursor()
                c.execute("INSERT INTO utenti (email, password) VALUES (?, ?)", (email_inserita, password_inserita))
                conn.commit()
                conn.close()
                messagebox.showinfo("Successo", "Registrazione completata!")
                window.destroy()
                accedi()
            except sqlite3.IntegrityError:
                messagebox.showerror("Errore", "Email già registrata!")

        btn_registrati = customtkinter.CTkButton(master=frame, text="REGISTRATI", command=registrati)
        btn_registrati.pack(padx=20, pady=10)
        
        window.mainloop()

    def accedi():
        microsoft = customtkinter.CTk()
        microsoft.title("Accesso")
        
        frame = customtkinter.CTkFrame(master=microsoft)
        frame.pack(padx=20, pady=10)
        
        label = customtkinter.CTkLabel(master=frame, text="Accedi all'account",font=("Arial",16))
        label.pack(padx=20, pady=7)
        
        entry_email = customtkinter.CTkEntry(master=frame, placeholder_text="Email")
        entry_email.pack(padx=20, pady=4)
        
        entry_password = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
        entry_password.pack(padx=20, pady=4)
        
        def mostra_password():
            if entry_password.cget("show") == "*":
                entry_password.configure(show="")
            else:
                entry_password.configure(show="*")
        
        checkbox_mostra = customtkinter.CTkCheckBox(master=frame, text="Mostra password?", command=mostra_password)
        checkbox_mostra.pack(padx=20, pady=2)
        
        def verifica_accesso():
            email_inserita = entry_email.get()
            password_inserita = entry_password.get()
            
            conn = sqlite3.connect("utenti.db")
            c = conn.cursor()
            c.execute("SELECT * FROM utenti WHERE email=? AND password=?", (email_inserita, password_inserita))
            result = c.fetchone()
            conn.close()
            
            if result:
                messagebox.showinfo("Accesso riuscito", "Benvenuto!")
                microsoft.destroy()
                entro()
            else:
                messagebox.showerror("Errore", "Email o password errati!")

        btn_accedi = customtkinter.CTkButton(master=frame, text="ACCEDI", command=verifica_accesso)
        btn_accedi.pack(padx=20, pady=10)
        
        microsoft.mainloop()

    def entro():
        number = "0123456789!!£$%€&/()=?^*-:.;,ç°@#[]<>"
        
        welcome_window = customtkinter.CTk()
        welcome_window.title("Benvenuto")
        
        
        nome_val = ""
        cognome_val = ""
        giorno_val = ""
        mese_val = ""
        anno_val = ""
        sesso_val = -1
        
    
        def date(*args):
            selected_date = f"{giorno.get()}/{mese.get()}/{year_var.get()}"
            date_label.configure(text=f"Data selezionata: {selected_date}")
        
        def sex():
            sesso = {0: "Maschio", 1: "Femmina"}
            sexx.configure(text=f"Il tuo sesso è: {sesso[sesso_var.get()]}")
        
        def verificare():
            nonlocal nome_val, cognome_val, giorno_val, mese_val, anno_val, sesso_val
            
        
            if nome.get() == "" or any(i in number for i in nome.get()):
                messagebox.showerror("Errore", "Inserisci il nome senza numeri o segni")
                return
            
            
            if cognome.get() == "" or any(i in number for i in cognome.get()):
                messagebox.showerror("Errore", "Inserisci il cognome senza numeri o segni")
                return
            
            
            try:
                if int(year_var.get()) >= 2007:
                    messagebox.showerror("Errore", "Devi essere maggiorenne")
                    return
            except ValueError:
                messagebox.showerror("Errore", "Anno non valido")
                return
            
            
            if sesso_var.get() not in (0, 1):
                messagebox.showerror("Errore", "Seleziona il sesso")
                return
            
            
            nome_val = nome.get()
            cognome_val = cognome.get()
            giorno_val = giorno.get()
            mese_val = mese.get()
            anno_val = year_var.get()
            sesso_val = sesso_var.get()
            
            welcome_window.destroy()
            show_sito()
        
        def show_sito():
            newwindow = customtkinter.CTk()
            newwindow.title("Benvenuto")
            
            customtkinter.CTkLabel(
                master=newwindow,
                text=f"Benvenuto {nome_val} {cognome_val}",
                font=("Arial", 16)
            ).pack(pady=20)
            
            customtkinter.CTkLabel(
                master=newwindow,
                text=f"Nato il: {giorno_val}/{mese_val}/{anno_val}\nSesso: {'Maschio' if sesso_val == 0 else 'Femmina'}",
                font=("Arial", 14)
            ).pack(pady=10)
            
            newwindow.mainloop()
        
        
        frime = customtkinter.CTkFrame(master=welcome_window)
        frime.pack(padx=50, pady=50)

        
        customtkinter.CTkLabel(master=frime, text="Nome?").pack(padx=10, pady=5)
        nome = customtkinter.CTkEntry(master=frime, placeholder_text="Inserisci nome", font=("Arial", 16))
        nome.pack(padx=10, pady=3)

        
        customtkinter.CTkLabel(master=frime, text="Cognome?").pack(padx=10, pady=5)
        cognome = customtkinter.CTkEntry(master=frime, placeholder_text="Inserisci cognome", font=("Arial", 16))
        cognome.pack(padx=10, pady=3)

    
        customtkinter.CTkLabel(master=frime, text="Giorno").pack(padx=10, pady=2)
        giorno = customtkinter.StringVar(value="1")
        day = customtkinter.CTkOptionMenu(master=frime, variable=giorno, 
                            values=[str(i) for i in range(1, 32)], command=date)
        day.pack(padx=10, pady=2)

        customtkinter.CTkLabel(master=frime, text="Mese").pack(padx=10, pady=3)
        mese = customtkinter.StringVar(value="1")
        mase = customtkinter.CTkOptionMenu(master=frime, variable=mese, 
                                values=[str(i) for i in range(1, 13)], command=date)
        mase.pack(padx=10, pady=2)

        customtkinter.CTkLabel(master=frime, text="Anno").pack(padx=10, pady=3)
        year_var = customtkinter.StringVar(value=str(1955))
        year_menu = customtkinter.CTkOptionMenu(master=frime, variable=year_var, 
                                    values=[str(i) for i in range(1955, datetime.now().year + 1)], 
                                    command=date)
        year_menu.pack(padx=10, pady=2)

        date_label = customtkinter.CTkLabel(master=frime, text="Data selezionata: ")
        date_label.pack(pady=20)

        
        customtkinter.CTkLabel(master=frime, text="Inserisci il sesso:").pack(padx=10, pady=3)
        sesso_var = customtkinter.IntVar(value=-1)
        
        for text, value in [("Maschio", 0), ("Femmina", 1)]:
            customtkinter.CTkRadioButton(master=frime, variable=sesso_var, 
                            value=value, text=text, command=sex).pack(padx=10, pady=2, anchor="w")

        sexx = customtkinter.CTkLabel(master=frime, text="Il tuo sesso è: ")
        sexx.pack(padx=10, pady=2)

        customtkinter.CTkButton(master=frime, text="Conferma", command=verificare).pack(padx=10, pady=20)

        welcome_window.mainloop()
        
    

    root = customtkinter.CTk()
    root.title("Account")
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(padx=30, pady=50)
    label = customtkinter.CTkLabel(master=frame, text="Hai un account?")
    label.pack(padx=20, pady=20)
    btn_frame = customtkinter.CTkFrame(master=frame)
    btn_frame.pack(padx=10, pady=10)
    btn_registrati = customtkinter.CTkButton(master=btn_frame, text="Registrati", command=sign_up)
    btn_registrati.pack(side=LEFT, padx=10)
    btn_accedi = customtkinter.CTkButton(master=btn_frame, text="Accedi", command=accedi)
    btn_accedi.pack(side=RIGHT, padx=10)
    root.mainloop()

root = customtkinter.CTk()
root.title("Account")
frame = customtkinter.CTkFrame(master=root)
frame.pack(padx=30, pady=50)
label = customtkinter.CTkLabel(master=frame, text="Hai un account?")
label.pack(padx=20, pady=20)
btn_frame = customtkinter.CTkFrame(master=frame)
btn_frame.pack(padx=10, pady=10)
btn_registrati = customtkinter.CTkButton(master=btn_frame, text="Registrati", command=sign_up)
btn_registrati.pack(side=LEFT, padx=10)
btn_accedi = customtkinter.CTkButton(master=btn_frame, text="Accedi", command=accedi)
btn_accedi.pack(side=LEFT, padx=10)
secondary_app = customtkinter.CTkButton(master=btn_frame,text="Secondary app", command= app)
secondary_app.pack(side=RIGHT, padx=10)
root.mainloop()