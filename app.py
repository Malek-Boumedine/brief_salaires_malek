import tkinter as tk
from tkinter import ttk
import func_calc



"""
- petite interface avec plusieurs boutons
    - bouton "afficher résultats" tous les résultats 
    - bouton "affiche stats"
    - bouton "filtrer" avec liste des filiales a coté, pour filtrer sur la filiale qu'on veut
    - bouton "exporter salaires en csv"      -> fenetre qui permet de choisir l'endroit ou on enregistre
    - bouton ""exporter stats en csv"        -> fenetre qui permet de choisir l'endroit ou on enregistre
    - bouton quitter
"""

# fenetre = tk.Tk()
# fenetre.title("Salaires employés & Statistiques")
# fenetre.geometry("150x250")


# afficher_salaires = tk.Button(fenetre, text ="Afficher salaires", command = quit)
# afficher_salaires.pack()

# afficher_stats = tk.Button(fenetre, text ="Afficher les statistiques", command = quit)
# afficher_stats.pack()

# filtrer = tk.Button(fenetre, text ="Filtrer", command = quit)
# filtrer.pack()

# export_salaires = tk.Button(fenetre, text ="exporter les salaires en csv", command = quit)
# export_salaires.pack()

# export_stats = tk.Button(fenetre, text ="exporter les statistiques en csv", command = quit)
# export_stats.pack()

# quitter = tk.Button(fenetre, text ="Quitter!", command = quit)
# quitter.pack()


fenetre = tk.Tk()
fenetre.title("Salaires employés & Statistiques")
fenetre.geometry("250x300")

button_width = 25
button_height = 2

afficher_salaires = tk.Button(fenetre, text="Afficher salaires", command=quit, width=button_width, height=button_height)
afficher_salaires.grid(row=0, column=0, pady=5, padx=10)

afficher_stats = tk.Button(fenetre, text="Afficher les statistiques", command=quit, width=button_width, height=button_height)
afficher_stats.grid(row=1, column=0, pady=5, padx=10)

filtrer = tk.Button(fenetre, text="Filtrer", command=quit, width=button_width, height=button_height)
filtrer.grid(row=2, column=0, pady=5, padx=10)

export_salaires = tk.Button(fenetre, text="Exporter les salaires en CSV", command=quit, width=button_width, height=button_height)
export_salaires.grid(row=3, column=0, pady=5, padx=10)

export_stats = tk.Button(fenetre, text="Exporter les statistiques en CSV", command=quit, width=button_width, height=button_height)
export_stats.grid(row=4, column=0, pady=5, padx=10)

quitter = tk.Button(fenetre, text="Quitter!", command=quit, width=button_width, height=button_height)
quitter.grid(row=5, column=0, pady=5, padx=10)

fenetre.mainloop()