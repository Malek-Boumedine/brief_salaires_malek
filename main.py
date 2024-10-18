import func_calc

fichier = "employes_data_test.json"


donnees = func_calc.importation_json(fichier)
filiales = func_calc.list_filiales(donnees)
all_salaires = func_calc.salaire_mensuel_tout(donnees, filiales)

# export des salaires en CSV :
func_calc.save_salaires_to_csv(donnees, filiales, "employes_data_salaires.csv")

# export des stats en CSV : 
func_calc.save_stats_to_csv(donnees, filiales, "stats.csv")

# afficher les résultats
func_calc.afficher_resultats(all_salaires, filiales)






