import json
import csv


fichier = "employes_data.json"


# 1 - importer le fichier json et récupérer les données
# fonction d'importation du fichier json

def importation_json(chemin:str) -> dict : 
    
    """
    prend en entrée le chemin du fichier json contenant les données à traiter

    Args:
        chemin (str): chemin vers le fichier json (chemin absolu ouu relatif)

    Returns:
        dict: retourne un dictionnaire de données contenant des paires clé : valeur où la clé représente le nom du département, et les valeurs la liste des employés 
    """
    with open(chemin) as file : 
        return json.load(file)


## 2 - récupérer les différentes filiales de notre jeu de données

def departements(donnees:dict) -> list :
    
    """
    prend en entrée un dictionaire contenant des paires clé : valeur où la clé représente le nom du département, et les valeurs la liste des employés 

    Args:
        donnees (dict): dictionnaire de données

    Returns:
        list: retourne une liste des différents départements  
    """
    return list(donnees.keys())


## 3 - Ajouter à chaque employé la clé valeur "salaire_mensuel : valeur"

"""

Si l'employé a un contrat à temps plein et qu'il n'a pas travaillé toutes ses heures pour des raisons non justifiées (par exemple, absence non autorisée), l'employeur peut déduire les heures non travaillées du salaire.

Si l'absence est justifiée (maladie, congé autorisé, etc.), il peut y avoir des dispositions spécifiques pour le maintien du salaire ou des compensations, selon la législation du travail ou la convention collective.

#### --> je pars du principe que le salarié a travaillé le nombre d'heures qu'on a dans le tableau, et s'il a travaillé moins que ce qu'il a dans son contrat c'est parcequ'il na pas justifié ces heures ou il n'a pas travaillé 

"""

def add_salaire_mensuel_filiale(salaries : list) -> list: 
    
    """
    Fonction qui prend en entrès une liste de dictionnaires, ou chaque dictionnaire contiens les données de chaque salarié 
    cette fonction a pour but de calculer le salaire mensuel de chaque salarié, en prenant en compte les heures supplémentaires qui sont rémunérées 1.5 x le taux horaire de base
    Ensuite une paire clé : valeur correspondant au salaire_mensuel est ajoutée au dictionnaire de chaque salarié

    Args:
        salaries (list): liste de dictionnaires de données de salariés

    Returns:
        list : retourne une liste contenant les dictionnaires avec la nouvelle clé : valeur salaire_mensuel
    """
    for salarie in salaries : 
        
        hourly_rate = salarie["hourly_rate"]
        weekly_hours_worked = salarie["weekly_hours_worked"]
        contract_hours = salarie["contract_hours"]

        if weekly_hours_worked >= contract_hours : 
            salaire_base = hourly_rate * contract_hours * 4
            salaire_h_sup = (weekly_hours_worked - contract_hours) * hourly_rate * 1.5 * 4
            salaire_mensuel = salaire_base + salaire_h_sup
        else : 
            salaire_mensuel = hourly_rate * weekly_hours_worked * 4
        salarie["salaire_mensuel"] = salaire_mensuel
        
    # ajouter ici la fonction de tri
    salaries.sort(key= lambda x : x["salaire_mensuel"], reverse=True)
    
    return salaries


# on ajoute le salaire mensuel à tous les salariés en bouclant sur toutes les filières

def salaire_mensuel_tout(donnees : dict, depts : list) -> dict : 
    
    """
    cette fonction permet de calculer tous les salaires mensuels de tous les employes

    Args:
        donnees (dict): ici on doit utiliser les données qu'on a importé avec la fonction importation_json()
        depts (list): liste des filiales qu'on récupére avec la méthode departements()

    Returns:
        dict: retourne les données avec une nouvelle paire clé : valeur correspondant au salaire mensuel pour chaque salarié
    """
    
    for i in range(len(depts)) : 
        add_salaire_mensuel_filiale(donnees[depts[i]])
        
    return donnees

# donnees_avec_salaires_mensuels = salaire_mensuel_tout()


## 4 - calcul des statistiques d'une filiale : 

def stats_filiale(all_salaires : dict, filiale : str) -> tuple : 
    
    """
    cette fonction permet d'avoir les statistiques d'une filiale qu'on donne en paramètre

    Args:
        filiale (string): nom de la filière pour laquelle on veut calculer les statistiques
        all_data : toutes les données avec la nouvelle paire clé valeur salaire_mensuel, données récupéreées avec la méthode salaire_mensuel_tout()

    Returns:
        tuple : retourne un tuple contenant 3 valeurs :  
            salaire_moyen : salaire moyen de la filiale
            salaire_max : salaire maximal de la filiale
            salaire_min : salaire minimal de la filiale
    """
    
    donnees_filiale = all_salaires[filiale]
    
    salaires = []
    for salarie in donnees_filiale : 
        salaires.append(salarie["salaire_mensuel"])
    
    salaire_moyen = round(sum(salaires) / len(salaires),2)
    salaire_max = round(max(salaires),2)
    salaire_min = round(min(salaires),2)
    
    return salaire_moyen, salaire_max, salaire_min

# stats_filiale("TechCorp")


## 5 - calcul des statistiques globales : 


def stats_globales(all_salaires : dict ,filiales : list) : 
    
    """
    fonction qui calcule les statistiques globales retourne un tuple de 3 valeurs : salaire moyen, salaire maximal et salaire minimal de  de toutes l'entreprise
    
    Args:
        all_salaires (dict): toutes les données de notre jeu de données, contenant la nouvelle clé valeur "salaire_mensuel", qu'on récupére avec la fonction salaire_mensuel_tout()
        filiales (list): liste de toutes les filiales, on les récupére avec la méthode departements()



    Returns:
        moyen_global : salaire moyen dans toute l'entreprise
        maximal_global : salaire maximal dans toute l'entreprise
        minimal_global : salaire minimal dans toute l'entreprise
    """
    
    data = all_salaires
    filiales = departements(data)
    
    salaires_moyens = []
    salaires_max = []
    salaires_min = []
    
    for dep in filiales : 
        salaires_moyens.append(stats_filiale(all_salaires, dep)[0])
        salaires_max.append(stats_filiale(all_salaires, dep)[1])
        salaires_min.append(stats_filiale(all_salaires, dep)[2])
        
    moyen_global = round(sum(salaires_moyens) / len(salaires_moyens),2)
    maximal_global = round(max(salaires_max),2)
    minimal_global = round(min(salaires_max),2)
    
    return moyen_global, maximal_global, minimal_global

# stats_globales()


## 6 - Affichage des résultats :

def afficher_resultats(all_salaires : dict, filiales : list) : 

    """
    fonction qui permet d'afficher les résultats dans la console
    
    Args:
        all_salaires (dict): toutes les données de notre jeu de données, contenant la nouvelle clé valeur "salaire_mensuel", qu'on récupére avec la fonction salaire_mensuel_tout()
        filiales : liste des filiales du jeu de données, récupéres avec la méthode departements()
    
    """
    
    for fil_key, fil_values in all_salaires.items() : 
        print (f"Entreprise : {fil_key} \n")
        # print(f"Nom \t   |  Job  Salaire mensuel")
        
        for salarie in fil_values :
            print(f"{salarie["name"]:10} |  {salarie["job"]:20} |  Salaire mensuel : {salarie["salaire_mensuel"]:.2f} €")
            # print(f"{salarie["name"]} \t\t | {salarie["job"]} \t\t | Salaire mensuel : {salarie["salaire_mensuel"]} ")
        
        print("\n================================================================\n")
        print(f"Statistiques des salariès pour la filiale {fil_key}")
        print(f"Salaire moyen : {stats_filiale(all_salaires, fil_key)[0]:.2f} €")
        print(f"Salaire le plus élevé : {stats_filiale(all_salaires, fil_key)[1]:.2f} €")
        print(f"Salaire le plus bas : {stats_filiale(all_salaires, fil_key)[2]:.2f} €\n")
        print("================================================================\n")
    print(f"Statistiques globales pour l'ensemble l'entreprise")
    print(f"Salaire moyen : {stats_globales(all_salaires, filiales)[0]:.2f} €")
    print(f"Salaire le plus élevé : {stats_globales(all_salaires, filiales)[1]:.2f} €")
    print(f"Salaire le plus bas : {stats_globales(all_salaires, filiales)[2]:.2f} €\n")
    print("================================================================\n================================================================\n")
        

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------

# fonction de sauvegarde des salaires en CSV : 

def save_salaires_to_csv(data:dict, filiales:list, salaires_file_name:str) -> str: 
    
    """
    fonction qui prend en parametres un dictionnaire de données, une liste de filiales et un nom de fichier et enregistre les données dans un fichier CSV

    Args:
        data (dict): toutes les données de notre jeu de données, contenant la nouvelle clé valeur "salaire_mensuel", qu'on récupére avec la fonction 
        filiales (list): liste de toutes les filiales, on les récupére avec la méthode departements()
        salaires_file_name (str): nom qu'on veut donner au fichier CSV dans lequel on stocke les salaires
    
    Returns:
        salaires_file_name (str) : retourne le nom du fichier en entrée
    """
    
    champs = list(data[filiales[0]][0].keys()) + ["Filiale"]
    
    with open(salaires_file_name, "w", newline='') as csv_file : 
        writer = csv.DictWriter(csv_file, fieldnames=champs, delimiter=";")
        
        writer.writeheader()
        for f in filiales :
            for employe in data[f] :
                employe_data = employe.copy()
                employe_data["Filiale"] = f
                writer.writerow(employe_data)
    
    return salaires_file_name

    
# fonction de sauvegarde des stats en CSV : 

def save_stats_to_csv(all_salaires : dict, filiales : list, stats_file_name : str) -> dict: 
    
    """
    fonction qui prend en parametres un dictionnaire de données, une liste de filiales et un nom de fichier et enregistre les données dans un fichier CSV

    Args:
        all_salaires (dict): toutes les données de notre jeu de données, contenant la nouvelle clé valeur "salaire_mensuel", qu'on récupére avec la fonction 
        filiales (list): liste de toutes les filiales, on les récupére avec la méthode departements()
        stats_file_name (str): nom qu'on veut donner au fichier CSV dans lequel on stocke les statistiques
    
    Returns:
        stats (dict) : retourne un dictionnaire contenant toutes les statistiques de l'entreprise
    """

    stats = {}
    
    for f in filiales : 
        cles = ["salaire_moyen", "salaire_maximal", "salaire_minimal"]
        donnees_stats = list(stats_filiale(all_salaires, f))
        dict = {}
        for key, value in zip(cles,donnees_stats) : 
            dict[key] = value
        stats[f] = dict    
    stat_gl = {}
    for key, value in zip(cles, list(stats_globales(all_salaires, filiales))) : 
        stat_gl[key] = value

    stats["global"] = stat_gl
    
    with open(stats_file_name, "w", newline='') as csv_file : 
        champs = ["entreprise", "salaire_moyen", "salaire_maximal", "salaire_minimal"]
        writer = csv.DictWriter(csv_file, fieldnames=champs, delimiter=";")
        writer.writeheader()
        for entr, stat in stats.items() : 
            dico = stat.copy()
            dico["entreprise"] = entr
            writer.writerow(dico)

    return stats
    
    
    