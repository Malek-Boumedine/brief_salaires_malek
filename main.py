import func_calc

fichier = "employes_data.json"


donnees = func_calc.importation_json(fichier)
filiales = func_calc.departements(donnees)
all_salaires = func_calc.salaire_mensuel_tout(donnees, filiales)

# export des salaires en CSV :
func_calc.save_salaires_to_csv(donnees, filiales, "export/employes_data_salaires.csv")

# export des stats en CSV : 
func_calc.save_stats_to_csv(donnees, filiales, "export/stats.csv")

# afficher les résultats
# func_calc.afficher_resultats(all_salaires, filiales)






