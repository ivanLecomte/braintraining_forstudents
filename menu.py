"""
Ivan Lecomte
Projet DBPY
le 05.12.23
"""
import tkinter as tk
from tkinter import ttk
import geo01, info02, info05, database, results
import datetime
import tkinter.messagebox as messagebox
from tkinter import StringVar
from tkinter.ttk import Combobox
import hashlib


window = tk.Tk()
window_width = 1200
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
window.title("Entraînement cérébral")
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color
window.configure(bg=hex_color)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

def connect_user_window():
    login_window_width = 400
    login_window_height = 200
    login_window = tk.Toplevel(window)
    login_window.title("Connexion")
    login_window.geometry(f'{login_window_width}x{login_window_height}+{center_x}+{center_y}')

    # Déplacer la déclaration des Entry ici
    entry_username = tk.Entry(login_window, width=30)
    entry_username.grid(row=0, column=1, padx=10, pady=10)
    label_username = tk.Label(login_window, text="Nom d'utilisateur:")
    label_username.grid(row=0, column=0, padx=10, pady=10)

    entry_password = tk.Entry(login_window, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)
    label_password = tk.Label(login_window, text="Mot de passe:")
    label_password.grid(row=1, column=0, padx=10, pady=10)

    user_suername = entry_username.get()
    user_password = entry_password.get()

    btn_cancel = tk.Button(login_window, text="Annuler", command=login_window.destroy)
    btn_cancel.grid(row=2, column=0, pady=10)
    btn_login = tk.Button(login_window, text="Connexion", command=lambda: database.log_user(user_suername, user_password))
    btn_login.grid(row=2, column=1, pady=10)
    btn_new_acc = tk.Button(login_window, text="Créer un compte", command=lambda: create_account_window())
    btn_new_acc.grid(row=3, column=0, pady=10)


def create_account_window():
    new_acc_window_width = 400
    new_acc_window_height = 200
    new_acc_window = tk.Toplevel(window)
    new_acc_window.title("Créer un nouveau compte")
    new_acc_window.geometry(f'{new_acc_window_width}x{new_acc_window_height}+{center_x}+{400}')

    # Déplacer la déclaration des Entry ici
    entry_username = tk.Entry(new_acc_window, width=30)
    entry_username.grid(row=0, column=1, padx=10, pady=10)
    label_username = tk.Label(new_acc_window, text="Nom d'utilisateur:")
    label_username.grid(row=0, column=0, padx=10, pady=10)

    entry_password = tk.Entry(new_acc_window, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)
    label_password = tk.Label(new_acc_window, text="Mot de passe:")
    label_password.grid(row=1, column=0, padx=10, pady=10)

    user_suername = entry_username.get()
    user_password = entry_password.get()

    btn_cancel = tk.Button(new_acc_window, text="Annuler", command=new_acc_window.destroy)
    btn_cancel.grid(row=2, column=0, pady=10)
    btn_login = tk.Button(new_acc_window, text="Créer", command=lambda: database.insert_new_acc_data(user_suername, user_password))
    btn_login.grid(row=2, column=1, pady=10)
    print(user_suername, user_password)

a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None]  # Label (with images) array
a_image = [None, None, None]  # Images array
a_title = [None, None, None]  # Array of title (ex: GEO01)

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02, "info05": info05.open_window_info_05}

def exercise(event, exer):
    dict_games[exer](window)


def quit(event):
    window.destroy()

lbl_title = tk.Label(window, text="MENU D'ENTRAÎNEMENT", font=("Arial", 15))
lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

for ex in range(len(a_exercise)):
    a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")
    albl_image[ex] = tk.Label(window, image=a_image[ex])
    albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)
    albl_image[ex].bind("<Button-1>", lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))

btn_display = tk.Button(window, text="Afficher les résultats", font=("Arial", 15), command=lambda: results.display_result(window))
btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)

btn_display = tk.Button(window, text="Se connecter", font=("Arial", 15), command=lambda: connect_user_window())
btn_display.grid(row=0, column=2, sticky="NE", padx=20, pady=20)


window.mainloop()