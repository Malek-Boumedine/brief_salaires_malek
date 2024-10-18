import tkinter as tk
from tkinter import ttk, filedialog
import func_calc
import json
import os

####################################################################

def importer_fichier():
    
    global fichier, donnees, filiales, all_salaires, nom_fichier
    fichier = filedialog.askopenfilename(title="Sélectionner un fichier", filetypes=[("Fichiers JSON", "*.json")])
    nom_fichier = os.path.basename(fichier)
    with open(fichier, 'r') as f:
        donnees = json.load(f)
    filiales = func_calc.list_filiales(donnees)
    all_salaires = func_calc.salaire_mensuel_tout(donnees, filiales)
    with open('.temp_data.json', 'w') as temp_file:
        json.dump({'all_salaires': all_salaires, 'filiales': filiales}, temp_file)
    label_file.config(text=nom_fichier)
    liste_filiales.config(values=filiales)
    
def supprimer_fichier_temp():
    try:
        os.remove('.temp_data.json')
    except FileNotFoundError:
        print("Fichier temporaire introuvable.")
  
####################################################################

fichier = "employes_data_test.json"
donnees = func_calc.importation_json(fichier)
filiales = func_calc.list_filiales(donnees)
all_salaires = func_calc.salaire_mensuel_tout(donnees, filiales)


###############################################################################################
    
def afficher_all_tk():
    
    with open('.temp_data.json') as f:
        data = json.load(f)

    fenetre_affichage = tk.Toplevel(fenetre)
    fenetre_affichage.geometry("700x800")
    fenetre_affichage.title("Salaires")

    # Crée un Treeview
    tree = ttk.Treeview(fenetre_affichage, columns=("Nom", "Poste", "Salaire Mensuel", "Filiale"), show='headings')
    tree.heading("Nom", text="Nom")
    tree.heading("Poste", text="Poste")
    tree.heading("Salaire Mensuel", text="Salaire Mensuel")
    tree.heading("Filiale", text="Filiale")

    tree.column("Nom", width=150)
    tree.column("Poste", width=150)
    tree.column("Salaire Mensuel", width=150)
    tree.column("Filiale", width=150)

    scrollbar = ttk.Scrollbar(fenetre_affichage, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    for filiale, employes in data['all_salaires'].items():
        for employe in employes:
            nom = employe.get('name', 'N/A')
            poste = employe.get('job', 'N/A')
            salaire_mensuel = employe.get('salaire_mensuel', 0)
            tree.insert("", "end", values=(nom, poste, f"{salaire_mensuel:.2f} €", filiale))

    tree.pack(side=tk.LEFT, expand=True, fill='both', pady=10, padx=10)
    scrollbar.pack(side=tk.RIGHT, fill='y')

###############################################################################################

def afficher_filiale_tk(filiale):
    
    with open('.temp_data.json') as f:
        data = json.load(f)

    fenetre_affichage = tk.Toplevel(fenetre)
    fenetre_affichage.geometry("600x500")
    fenetre_affichage.title(f"Salaires - {filiale}")

    tree = ttk.Treeview(fenetre_affichage, columns=("Nom", "Poste", "Salaire Mensuel"), show='headings')
    tree.heading("Nom", text="Nom")
    tree.heading("Poste", text="Poste")
    tree.heading("Salaire Mensuel", text="Salaire Mensuel")

    tree.column("Nom", width=200)
    tree.column("Poste", width=200)
    tree.column("Salaire Mensuel", width=200)

    for employe in data['all_salaires'][filiale] :
        nom = employe.get('name', 'N/A')
        poste = employe.get('job', 'N/A')
        salaire_mensuel = employe.get('salaire_mensuel', 0)
        tree.insert("", "end", values=(nom, poste, f"{salaire_mensuel:.2f} €"))

    tree.pack(expand=True, fill='both', pady=10, padx=10)

###############################################################################################

def afficher_statistiques():
    
    fenetre_stats = tk.Toplevel(fenetre)
    fenetre_stats.geometry("600x200")
    fenetre_stats.title("Statistiques des Salaires")

    tree = ttk.Treeview(fenetre_stats, columns=("Filiale", "Salaire Moyen", "Salaire Max", "Salaire Min"), show='headings')
    tree.heading("Filiale", text="Filiale")
    tree.heading("Salaire Moyen", text="Salaire Moyen")
    tree.heading("Salaire Max", text="Salaire Max")
    tree.heading("Salaire Min", text="Salaire Min")

    tree.column("Filiale", width=150)
    tree.column("Salaire Moyen", width=150)
    tree.column("Salaire Max", width=150)
    tree.column("Salaire Min", width=150)

    for filiale in filiales:
        salaire_moyen, salaire_max, salaire_min = func_calc.stats_filiale(all_salaires, filiale)
        tree.insert("", "end", values=(filiale, f"{salaire_moyen:.2f} €", f"{salaire_max:.2f} €", f"{salaire_min:.2f} €"))

    moyen_global, maximal_global, minimal_global = func_calc.stats_globales(all_salaires, filiales)
    tree.insert("", "end", values=("Global", f"{moyen_global:.2f} €", f"{maximal_global:.2f} €", f"{minimal_global:.2f} €"))

    tree.pack(expand=True, fill='both', pady=10, padx=10)


###############################################################################################

def afficher_statistiques_filiale(filiale):

    fenetre_stats_filiale = tk.Toplevel(fenetre)
    fenetre_stats_filiale.geometry("400x120")
    fenetre_stats_filiale.title(f"Statistiques - {filiale}")

    tree = ttk.Treeview(fenetre_stats_filiale, columns=("Statistique", "Valeur"), show='headings')
    tree.heading("Statistique", text="Statistique")
    tree.heading("Valeur", text="Valeur")

    tree.column("Statistique", width=200)
    tree.column("Valeur", width=200)

    salaire_moyen, salaire_max, salaire_min = func_calc.stats_filiale(all_salaires, filiale)

    tree.insert("", "end", values=("Salaire Moyen", f"{salaire_moyen:.2f} €"))
    tree.insert("", "end", values=("Salaire Max", f"{salaire_max:.2f} €"))
    tree.insert("", "end", values=("Salaire Min", f"{salaire_min:.2f} €"))

    tree.pack(expand=True, fill='both', pady=10, padx=10)


###############################################################################################

def save_salaires_csv():
    
    fichier_csv = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
    if fichier_csv:
        func_calc.save_salaires_to_csv(all_salaires, filiales, fichier_csv)
        tk.messagebox.showinfo("Exportation réussie", "Le fichier a été exporté avec succès.")    

def save_stats_csv():
    
    fichier_csv = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
    if fichier_csv:
        func_calc.save_stats_to_csv(all_salaires, filiales, fichier_csv)
        tk.messagebox.showinfo("Exportation réussie", "Le fichier a été exporté avec succès.")
    
###############################################################################################

def close_window():
    
    sortie = tk.Toplevel()
    sortie.title("Confirmation")

    areyousure = tk.Label(sortie, text="Voulez-vous vraiment quitter ?")
    areyousure.grid(column=0, row=0)

    def quitter():
        supprimer_fichier_temp()
        fenetre.destroy()
    
    ExitYes = tk.Button(sortie, text="Oui", command = quitter)
    ExitYes.grid(column=1, row=0)

    ExitNo = tk.Button(sortie, text="Non", command = sortie.destroy)
    ExitNo.grid(column=2, row=0)
    
    sortie.mainloop()

###############################################################################################

fenetre = tk.Tk()
fenetre.title("Salaires employés & Statistiques")
fenetre.geometry("250x390")

button_width = 25
button_height = 1


# bouton pour afficher le nom du fichier
nom_fichier = ""
label_file = tk.Label(fenetre, text = nom_fichier)
label_file.grid(row=0, column=0, pady=5, padx=10)

# bouton pour importer le fichier
import_file = tk.Button(fenetre, text="importer un fichier", command=importer_fichier, width=button_width, height=button_height)
import_file.grid(row=1, column=0, pady=5, padx=10)

# bouton pour afficher tous les salaires
afficher_salaires = tk.Button(fenetre, text="Afficher salaires", command=afficher_all_tk, width=button_width, height=button_height)
afficher_salaires.grid(row=2, column=0, pady=5, padx=10)

# bouton pour afficher toutes les stats 
afficher_stats = tk.Button(fenetre, text="Afficher statistiques", command=afficher_statistiques, width=button_width, height=button_height)
afficher_stats.grid(row=3, column=0, pady=5, padx=10)

# texte filtrer sur une filiale
labelChoix = tk.Label(fenetre, text = "FIltrer sur une filiale ")
labelChoix.grid(row=4, column=0, pady=5, padx=10)

# liste deroulante contenant toutes les filiales
liste_filiales = ttk.Combobox(fenetre, values=filiales, state='readonly')
liste_filiales.grid(row=5, column=0, pady=5, padx=10)
filiale = liste_filiales.current(0)

# Frame pour contenir les 2 boutons de filtre
button_frame = tk.Frame(fenetre)
button_frame.grid(row=6, column=0, columnspan=2, pady=1, padx=1)

# Bouton pour filtrer les salaires
filtrer_salaires = tk.Button(button_frame, text="Salaires", command=lambda: afficher_filiale_tk(liste_filiales.get()), width=10, height=1)
filtrer_salaires.pack(side=tk.LEFT, padx=4)

# Bouton pour filtrer les statistiques
filtrer_stats = tk.Button(button_frame, text="Statistiques", command=lambda: afficher_statistiques_filiale(liste_filiales.get()), width=10, height=1)
filtrer_stats.pack(side=tk.LEFT, padx=4)

# bouton pour exporter les salaires en csv
export_salaires = tk.Button(fenetre, text="Exporter les salaires en CSV", command=save_salaires_csv, width=button_width, height=button_height)
export_salaires.grid(row=7, column=0, pady=5, padx=10)

# bouton pour exporter les stats en csv
export_stats = tk.Button(fenetre, text="Exporter les statistiques en CSV", command=save_stats_csv, width=button_width, height=button_height)
export_stats.grid(row=8, column=0, pady=5, padx=10)

# bouton pour quitter
quitter = tk.Button(fenetre, text="Quitter", command=close_window, width=button_width, height=button_height)
quitter.grid(row=9, column=0, pady=5, padx=10)


fenetre.mainloop()