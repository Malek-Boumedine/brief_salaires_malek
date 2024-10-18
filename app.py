import tkinter as tk
from tkinter import ttk, filedialog
import func_calc
import subprocess
import json


"""
- petite interface avec plusieurs boutons
    - bouton "afficher résultats & stats" tous les résultats    OK
    - bouton "filtrer" avec liste des filiales a coté, pour filtrer sur la filiale qu'on veut
    - bouton "exporter salaires en csv"      -> fenetre qui permet de choisir l'endroit ou on enregistre
    - bouton ""exporter stats en csv"        -> fenetre qui permet de choisir l'endroit ou on enregistre
    - bouton quitter        OK
"""

def save_salaires_csv() : 
    func_calc.save_salaires_to_csv(all_salaires, filiales, "export/employes_data_salaires.csv")
    
def save_stats_csv() : 
    func_calc.save_stats_to_csv(all_salaires, filiales, "export/stats.csv")

    

fichier = "employes_data.json"
donnees = func_calc.importation_json(fichier)
filiales = func_calc.departements(donnees)
all_salaires = func_calc.salaire_mensuel_tout(donnees, filiales)

with open('temp_data.json', 'w') as f:
    json.dump({'all_salaires': all_salaires, 'filiales': filiales}, f)
  

def afficher_all_terminal():
    subprocess.run(['gnome-terminal', '--', 'bash', '-c', 'python3 -c "import json; import func_calc; data = json.load(open(\'temp_data.json\')); func_calc.afficher_resultats(data[\'all_salaires\'], data[\'filiales\'])"; exec bash'])


def afficher_filiale_terminal(filiale):
    
    subprocess.run(['gnome-terminal', '--', 'bash', '-c', 'python3 -c "import json; import func_calc; data = json.load(open(\'temp_data.json\')); func_calc.afficher_resultats(data[\'all_salaires\'], data[\'{filiales}\'])"; exec bash'])
    
    # subprocess.run(['gnome-terminal', '--', 'bash', '-c',
    # f'python3 -c "import json; import func_calc; '
    # f'data = json.load(open(\'temp_data.json\')); '
    # f'func_calc.afficher_resultats(data[\'all_salaires\'], \'{filiale}\')"'])
    

def importer_fichier(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)

    
# ----------------------------------------------------------------

fenetre = tk.Tk()
fenetre.title("Salaires employés & Statistiques")
fenetre.geometry("250x350")

button_width = 25
button_height = 1

# OK
import_file = tk.Button(fenetre, text="importer un fichier", command=importer_fichier, width=button_width, height=button_height)
import_file.grid(row=0, column=0, pady=5, padx=10)

#OK
afficher_salaires = tk.Button(fenetre, text="Afficher salaires & statistiques", command=afficher_all_terminal, width=button_width, height=button_height)
afficher_salaires.grid(row=1, column=0, pady=5, padx=10)

#
labelChoix = tk.Label(fenetre, text = "FIltrer sur une filiale ")
labelChoix.grid(row=2, column=0, pady=5, padx=10)

#
liste_filiales = ttk.Combobox(fenetre, values=filiales)
filiale = liste_filiales.current(0)
liste_filiales.grid(row=3, column=0, pady=5, padx=10)

#
mafiliale = ["TechCorp"]
filtrer = tk.Button(fenetre,text="Filtrer", command=afficher_filiale_terminal(mafiliale), width=button_width, height=button_height)
filtrer.grid(row=4, column=0, pady=5, padx=10)

# OK
export_salaires = tk.Button(fenetre, text="Exporter les salaires en CSV", command=save_salaires_csv, width=button_width, height=button_height)
export_salaires.grid(row=5, column=0, pady=5, padx=10)

# OK
export_stats = tk.Button(fenetre, text="Exporter les statistiques en CSV", command=save_stats_csv, width=button_width, height=button_height)
export_stats.grid(row=6, column=0, pady=5, padx=10)

# OK
quitter = tk.Button(fenetre, text="Quitter", command=quit, width=button_width, height=button_height)
quitter.grid(row=7, column=0, pady=5, padx=10)



fenetre.mainloop()
