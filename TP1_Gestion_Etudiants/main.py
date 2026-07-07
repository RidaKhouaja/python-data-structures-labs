import json 
import os 
import sys 

FICHIER_JSON = "etudiants.json"
FICHIER_EXPORT = "etudiants_export.txt"

# chargement et sauvegarde des données 
def charger_etudiants():
    """ charge les étudiants depuis le fichier JSON . """
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_etudiants(etudiants):
     """ sauvegarde les étudiants dans le fichier JSON . """
     with open(FICHIER_JSON,"w",encoding = "utf-8") as f :
          json.dump(etudiants,f , indent = 4 , ensure_ascii= False)


 

 # ============================================================
# AJOUTER UN ÉTUDIANT
# ============================================================
def ajouter_etudiant(etudiants):
    """Ajoute un nouvel étudiant à la liste."""
    print("\n AJOUTER UN ÉTUDIANT")
    print("-" * 30)
    
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    
    # Vérification que le nom n'est pas vide
    if not nom or not prenom:
        print(" Erreur : Nom et prénom obligatoires!")
        return
    
    # Saisie des notes
    matieres = ["Maths", "Physique", "Informatique", "Anglais", "Français"]
    notes = {}
    
    print("\n Entrez les notes (0-20) :")
    for matiere in matieres:
        while True:
            try:
                note = float(input(f"  {matiere} : "))
                if 0 <= note <= 20:
                    notes[matiere] = note
                    break
                else:
                    print("  Note doit être entre 0 et 20!")
            except ValueError:
                print("  Entrez un nombre valide!")
    
    # Calcul de la moyenne
    moyenne = sum(notes.values()) / len(notes)
    
    # Création de l'étudiant
    etudiant = {
        "nom": nom,
        "prenom": prenom,
        "notes": notes,
        "moyenne": round(moyenne, 2)
    }
    
    etudiants.append(etudiant)
    sauvegarder_etudiants(etudiants)
    
    print(f"\n Étudiant {prenom} {nom} ajouté avec succès!")
    print(f" Moyenne : {moyenne:.2f}/20")

           

    
# ============================================================
# AFFICHER TOUS LES ÉTUDIANTS
# ============================================================
def afficher_etudiants(etudiants):
    """Affiche la liste de tous les étudiants."""
    print("\n LISTE DES ÉTUDIANTS")
    print("-" * 50)
    
    if not etudiants:
        print(" Aucun étudiant enregistré!")
        return
    
    for i, etudiant in enumerate(etudiants, 1):
        print(f"\n Étudiant N°{i}")
        print(f"   Nom    : {etudiant['nom']} {etudiant['prenom']}")
        print(f"   Notes  :")
        for matiere, note in etudiant['notes'].items():
            print(f"      . {matiere} : {note}/20")
        print(f"   Moyenne: {etudiant['moyenne']}/20")
        print("-" * 50)

# ============================================================
# RECHERCHER UN ÉTUDIANT
# ============================================================
def rechercher_etudiant(etudiants):
    """Recherche un étudiant par nom ou prénom."""
    print("\n RECHERCHER UN ÉTUDIANT")
    print("-" * 30)
    
    if not etudiants:
        print(" Aucun étudiant enregistré!")
        return
    
    recherche = input("Entrez le nom ou prénom : ").strip().lower()
    
    # Recherche dans la liste
    resultats = [
        e for e in etudiants
        if recherche in e['nom'].lower() 
        or recherche in e['prenom'].lower()
    ]
    
    if not resultats:
        print(f" Aucun étudiant trouvé pour '{recherche}'!")
        return
    
    print(f"\n {len(resultats)} étudiant(s) trouvé(s) :")
    print("-" * 50)
    
    for etudiant in resultats:
        print(f"\n {etudiant['prenom']} {etudiant['nom']}")
        print(f"   Notes  :")
        for matiere, note in etudiant['notes'].items():
            print(f"      • {matiere} : {note}/20")
        print(f"   Moyenne: {etudiant['moyenne']}/20")
        print("-" * 50)

        # ============================================================
# MODIFIER UN ÉTUDIANT
# ============================================================
def modifier_etudiant(etudiants):
    """Modifie les informations d'un étudiant existant."""
    print("\n MODIFIER UN ÉTUDIANT")
    print("-" * 30)
    
    if not etudiants:
        print(" Aucun étudiant enregistré!")
        return
    
    # Afficher la liste pour choisir
    for i, e in enumerate(etudiants, 1):
        print(f"  {i}. {e['prenom']} {e['nom']} — Moyenne: {e['moyenne']}/20")
    
    # Choisir l'étudiant à modifier
    while True:
        try:
            choix = int(input("\nNuméro de l'étudiant à modifier : "))
            if 1 <= choix <= len(etudiants):
                break
            else:
                print(f" Entrez un numéro entre 1 et {len(etudiants)}!")
        except ValueError:
            print(" Entrez un numéro valide!")
    
    etudiant = etudiants[choix - 1]
    print(f"\n Modification de : {etudiant['prenom']} {etudiant['nom']}")
    print("(Appuyez sur Entrée pour garder l'ancienne valeur)")
    
    # Modifier nom et prénom
    nouveau_nom = input(f"Nouveau nom [{etudiant['nom']}] : ").strip()
    nouveau_prenom = input(f"Nouveau prénom [{etudiant['prenom']}] : ").strip()
    
    if nouveau_nom:
        etudiant['nom'] = nouveau_nom
    if nouveau_prenom:
        etudiant['prenom'] = nouveau_prenom
    
    # Modifier les notes
    print("\n Modifier les notes (Entrée = garder ancienne note) :")
    matieres = ["Maths", "Physique", "Informatique", "Anglais", "Français"]
    
    for matiere in matieres:
        ancienne_note = etudiant['notes'].get(matiere, 0)
        while True:
            try:
                saisie = input(f"  {matiere} [{ancienne_note}] : ").strip()
                if saisie == "":
                    break  # Garder ancienne note
                note = float(saisie)
                if 0 <= note <= 20:
                    etudiant['notes'][matiere] = note
                    break
                else:
                    print("   Note doit être entre 0 et 20!")
            except ValueError:
                print("   Entrez un nombre valide!")
    
    # Recalculer la moyenne
    etudiant['moyenne'] = round(
        sum(etudiant['notes'].values()) / len(etudiant['notes']), 2
    )
    
    sauvegarder_etudiants(etudiants)
    print(f"\n Étudiant modifié avec succès!")
    print(f"Nouvelle moyenne : {etudiant['moyenne']}/20")


# ============================================================
# SUPPRIMER UN ÉTUDIANT
# ============================================================
def supprimer_etudiant(etudiants):
    """Supprime un étudiant de la liste."""
    print("\n SUPPRIMER UN ÉTUDIANT")
    print("-" * 30)
    
    if not etudiants:
        print(" Aucun étudiant enregistré!")
        return
    
    # Afficher la liste pour choisir
    for i, e in enumerate(etudiants, 1):
        print(f"  {i}. {e['prenom']} {e['nom']} — Moyenne: {e['moyenne']}/20")
    
    # Choisir l'étudiant à supprimer
    while True:
        try:
            choix = int(input("\n Numéro de l'étudiant à supprimer : "))
            if 1 <= choix <= len(etudiants):
                break
            else:
                print(f" Entrez un numéro entre 1 et {len(etudiants)}!")
        except ValueError:
            print(" Entrez un numéro valide!")
    
    etudiant = etudiants[choix - 1]
    
    # Confirmation avant suppression
    confirmation = input(
        f"\n Confirmer suppression de {etudiant['prenom']} {etudiant['nom']} ? (oui/non) : "
    ).strip().lower()
    
    if confirmation == "oui":
        etudiants.pop(choix - 1)
        sauvegarder_etudiants(etudiants)
        print(f" Étudiant supprimé avec succès!")
    else:
        print(" Suppression annulée!")

 # ============================================================
# CALCULER LA MOYENNE GÉNÉRALE
# ============================================================
def moyenne_generale(etudiants):
    """Calcule et affiche la moyenne générale de la classe."""
    print("\n MOYENNE GÉNÉRALE DE LA CLASSE")
    print("-" * 30)
    
    if not etudiants:
        print(" Aucun étudiant enregistré!")
        return
    
    total = sum(e['moyenne'] for e in etudiants)
    moyenne = total / len(etudiants)
    
    print(f" Nombre d'étudiants : {len(etudiants)}")
    print(f" Moyenne générale   : {moyenne:.2f}/20")
    
    # Statistiques supplémentaires
    meilleur = max(etudiants, key=lambda e: e['moyenne'])
    faible   = min(etudiants, key=lambda e: e['moyenne'])
    
    print(f"🥇 Meilleur étudiant  : {meilleur['prenom']} {meilleur['nom']} ({meilleur['moyenne']}/20)")
    print(f"📉 Étudiant faible    : {faible['prenom']} {faible['nom']} ({faible['moyenne']}/20)")


# ============================================================
# AFFICHER LE CLASSEMENT
# ============================================================
def afficher_classement(etudiants):
    """Affiche le classement des étudiants par moyenne décroissante."""
    print("\n🏆 CLASSEMENT DES ÉTUDIANTS")
    print("-" * 50)
    
    if not etudiants:
        print("❌ Aucun étudiant enregistré!")
        return
    
    # Trier par moyenne décroissante
    classement = sorted(etudiants, key=lambda e: e['moyenne'], reverse=True)
    
    medailles = {1: "🥇", 2: "🥈", 3: "🥉"}
    
    for rang, etudiant in enumerate(classement, 1):
        medaille = medailles.get(rang, "   ")
        
        # Mention selon la moyenne
        moyenne = etudiant['moyenne']
        if moyenne >= 16:
            mention = "✨ Très Bien"
        elif moyenne >= 14:
            mention = "👍 Bien"
        elif moyenne >= 12:
            mention = "👌 Assez Bien"
        elif moyenne >= 10:
            mention = "✅ Passable"
        else:
            mention = "❌ Insuffisant"
        
        print(f"{medaille} Rang {rang:2} | {etudiant['prenom']} {etudiant['nom']:15} | "
              f"{etudiant['moyenne']:5.2f}/20 | {mention}")
    
    print("-" * 50)


# ============================================================
# EXPORTER LES RÉSULTATS
# ============================================================
def exporter_resultats(etudiants):
    """Exporte les résultats dans un fichier texte."""
    print("\n💾 EXPORT DES RÉSULTATS")
    print("-" * 30)
    
    if not etudiants:
        print("❌ Aucun étudiant enregistré!")
        return
    
    classement = sorted(etudiants, key=lambda e: e['moyenne'], reverse=True)
    
    with open(FICHIER_EXPORT, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("       RÉSULTATS - GESTION DES ÉTUDIANTS\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Nombre total d'étudiants : {len(etudiants)}\n")
        total = sum(e['moyenne'] for e in etudiants)
        f.write(f"Moyenne générale classe  : {total/len(etudiants):.2f}/20\n")
        f.write("\n" + "-" * 60 + "\n")
        f.write("CLASSEMENT\n")
        f.write("-" * 60 + "\n\n")
        
        for rang, etudiant in enumerate(classement, 1):
            f.write(f"Rang {rang} — {etudiant['prenom']} {etudiant['nom']}\n")
            f.write(f"  Notes :\n")
            for matiere, note in etudiant['notes'].items():
                f.write(f"    • {matiere} : {note}/20\n")
            f.write(f"  Moyenne : {etudiant['moyenne']}/20\n\n")
        
        f.write("=" * 60 + "\n")
        f.write("FIN DU RAPPORT\n")
        f.write("=" * 60 + "\n")
    
    print(f"✅ Résultats exportés dans '{FICHIER_EXPORT}' avec succès!")


    # ============================================================
# MENU PRINCIPAL
# ============================================================
def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 50)
    print("       🎓 GESTION DES ÉTUDIANTS 🎓")
    print("=" * 50)
    print("  1️⃣  Ajouter un étudiant")
    print("  2️⃣  Afficher tous les étudiants")
    print("  3️⃣  Rechercher un étudiant")
    print("  4️⃣  Modifier un étudiant")
    print("  5️⃣  Supprimer un étudiant")
    print("  6️⃣  Moyenne générale de la classe")
    print("  7️⃣  Classement des étudiants")
    print("  8️⃣  Exporter les résultats")
    print("  0️⃣  Quitter")
    print("=" * 50)


def main():
    """Fonction principale — point d'entrée du programme."""
    print("\n🚀 Bienvenue dans le système de Gestion des Étudiants!")
    
    # Charger les données au démarrage
    etudiants = charger_etudiants()
    print(f"📂 {len(etudiants)} étudiant(s) chargé(s) depuis la base de données.")
    
    while True:
        afficher_menu()
        
        choix = input("\n👉 Votre choix : ").strip()
        
        if choix == "1":
            ajouter_etudiant(etudiants)
        elif choix == "2":
            afficher_etudiants(etudiants)
        elif choix == "3":
            rechercher_etudiant(etudiants)
        elif choix == "4":
            modifier_etudiant(etudiants)
        elif choix == "5":
            supprimer_etudiant(etudiants)
        elif choix == "6":
            moyenne_generale(etudiants)
        elif choix == "7":
            afficher_classement(etudiants)
        elif choix == "8":
            exporter_resultats(etudiants)
        elif choix == "0":
            print("\n👋 Au revoir! À bientôt!")
            break
        else:
            print("\n❌ Choix invalide! Entrez un numéro entre 0 et 8.")




# ============================================================
# POINT D'ENTRÉE
# ============================================================
if __name__ == "__main__":
    print("Programme démarré...")
    # input("Appuyez sur Entrée pour continuer...") # Tu peux décommenter si besoin
    main()