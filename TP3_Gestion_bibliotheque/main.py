import json 
import os 
from datetime import datetime 

#fichier de données 

FICHIER_JSON = "bibliotheque.json"

#charegement et sauvergarde des données 

def charger_bibliotheque():
    """Charge les livres depuis le fichier JSON."""
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            if not contenu:
                return []
            return json.loads(contenu)
    return []
 

def sauvegarder_bibliotheque(livres):

    """Sauvegarde les livres dans la fichier JSON."""
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(livres , f , indent=4 , ensure_ascii=False)


# ============================================================
# AJOUTER UN LIVRE
# ============================================================
def ajouter_livre(livres):
    """Ajoute un nouveau livre à la bibliothèque."""
    print("\n AJOUTER UN LIVRE")
    print("-" * 40)

    # Saisie ISBN
    while True:
        isbn = input("ISBN : ").strip()
        if not isbn:
            print(" L'ISBN est obligatoire!")
            continue
        # Vérifier si l'ISBN existe déjà
        if any(l['isbn'] == isbn for l in livres):
            #la fonction any() s'arrete si trouve un true  :
            print(f" Un livre avec l'ISBN '{isbn}' existe déjà!")
            continue
        break

    # Saisie titre
    while True:
        titre = input("Titre : ").strip()
        if not titre:
            print(" Le titre est obligatoire!")
        else:
            break

    # Saisie auteur
    while True:
        auteur = input("Auteur : ").strip()
        if not auteur:
            print(" L'auteur est obligatoire!")
        else:
            break

    # Création du livre
    livre = {
        "isbn"       : isbn,
        "titre"      : titre,
        "auteur"     : auteur,
        "disponible" : True,
        "emprunts"   : []
    }

    livres.append(livre)
    sauvegarder_bibliotheque(livres)

    print(f"\n Livre '{titre}' ajouté avec succès!")
    print(f"   ISBN   : {isbn}")
    print(f"   Auteur : {auteur}")
    print(f"   Statut : Disponible")

# ============================================================
# AFFICHER TOUS LES LIVRES
# ============================================================


def afficher_livres(livres):
    """Affiche tous les livres de la bibliothéque ."""
    print("\n LISTE DES LIVRES")
    print("-" * 40)

    if not livres :
        print("Aucun livre dans la bibliothéque .")
        return 
    
    for i, livre in enumerate(livres , 1) :
        statut = "Disponible" if livre['disponible'] else "Emprunté"

        print(f"\n Livre N° {i}")
        print(f"   ISBN   : {livre['isbn']}")
        print(f"Titre : {livre['titre']}")
        print(f"   Auteur : {livre['auteur']}")
        print(f"   Statut : {statut}")
        if not livre['disponible'] and livre['emprunts']:
            dernier = livre['emprunts'][-1]
            print(f" Emprunté par : {dernier['nom']}")
            print(f" date emprunt : {dernier['date_emprunt']}")
        print("-"*60)
        
# ============================================================
# RECHERCHE MULTICRITÈRE
# ============================================================
def rechercher_livre(livres):
    """Recherche un livre par titre, auteur ou ISBN."""
    print("\n RECHERCHE DE LIVRE")
    print("-" * 40)

    if not livres:
        print(" Aucun livre enregistré!")
        return

    print("Critères de recherche :")
    print("  1. Par titre")
    print("  2. Par auteur")
    print("  3. Par ISBN")
    print("  4. Livres disponibles uniquement")
    print("  5. Livres empruntés uniquement")

    choix = input("\nVotre choix : ").strip()

    if choix == "1":
        terme = input("Titre à rechercher : ").strip().lower()
        resultats = [l for l in livres if terme in l['titre'].lower()]
        critere = f"titre contenant '{terme}'"

    elif choix == "2":
        terme = input("Auteur à rechercher : ").strip().lower()
        resultats = [l for l in livres if terme in l['auteur'].lower()]
        critere = f"auteur contenant '{terme}'"

    elif choix == "3":
        terme = input("ISBN à rechercher : ").strip()
        resultats = [l for l in livres if terme in l['isbn']]
        critere = f"ISBN '{terme}'"

    elif choix == "4":
        resultats = [l for l in livres if l['disponible']]
        critere = "livres disponibles"

    elif choix == "5":
        resultats = [l for l in livres if not l['disponible']]
        critere = "livres empruntés"

    else:
        print(" Choix invalide!")
        return

    # Affichage des résultats
    if not resultats:
        print(f"\n Aucun livre trouvé pour : {critere}")
        return

    print(f"\n {len(resultats)} livre(s) trouvé(s) pour : {critere}")
    print("-" * 60)

    for livre in resultats:
        statut = " Disponible" if livre['disponible'] else "❌ Emprunté"
        print(f"\n {livre['titre']}")
        print(f"   ISBN    : {livre['isbn']}")
        print(f"   Auteur  : {livre['auteur']}")
        print(f"   Statut  : {statut}")
        print("-" * 60)

# ============================================================
# EMPRUNTER UN LIVRE
# ============================================================
def emprunter_livre(livres):
    """Enregistre l'emprunt d'un livre."""
    print("\n EMPRUNTER UN LIVRE")
    print("-" * 40)

    if not livres:
        print(" Aucun livre enregistré!")
        return

    # Afficher uniquement les livres disponibles
    disponibles = [l for l in livres if l['disponible']]

    if not disponibles:
        print(" Aucun livre disponible actuellement!")
        return

    print(f" {len(disponibles)} livre(s) disponible(s) :\n")
    for i, livre in enumerate(disponibles, 1):
        print(f"  {i}. [{livre['isbn']}] {livre['titre']} — {livre['auteur']}")

    # Choisir le livre
    while True:
        try:
            choix = int(input("\nNuméro du livre à emprunter : "))
            if 1 <= choix <= len(disponibles):
                break
            else:
                print(f" Entrez un numéro entre 1 et {len(disponibles)}!")
        except ValueError:
            print(" Entrez un numéro valide!")

    livre_choisi = disponibles[choix - 1]

    # Saisie du nom de l'emprunteur
    while True:
        emprunteur = input("Nom de l'emprunteur : ").strip()
        if not emprunteur:
            print(" Le nom est obligatoire!")
        else:
            break

    # Enregistrement de l'emprunt
    date_aujourd_hui = datetime.now().strftime("%Y-%m-%d")

    emprunt = {
        "emprunteur"  : emprunteur,
        "date_emprunt": date_aujourd_hui,
        "date_retour" : None
    }

    # Trouver le livre dans la liste principale et le mettre à jour
    for livre in livres:
        if livre['isbn'] == livre_choisi['isbn']:
            livre['disponible'] = False
            livre['emprunts'].append(emprunt)
            break

    sauvegarder_bibliotheque(livres)

    print(f"\n Livre emprunté avec succès!")
    print(f"   Titre       : {livre_choisi['titre']}")
    print(f"   Emprunteur  : {emprunteur}")
    print(f"   Date        : {date_aujourd_hui}")


# ============================================================
# RETOURNER UN LIVRE
# ============================================================
def retourner_livre(livres):
    """Enregistre le retour d'un livre emprunté."""
    print("\n RETOURNER UN LIVRE")
    print("-" * 40)

    if not livres:
        print(" Aucun livre enregistré!")
        return

    # Afficher uniquement les livres empruntés
    empruntes = [l for l in livres if not l['disponible']]

    if not empruntes:
        print(" Aucun livre emprunté actuellement!")
        return

    print(f" {len(empruntes)} livre(s) emprunté(s) :\n")
    for i, livre in enumerate(empruntes, 1):
        dernier = livre['emprunts'][-1]
        print(f"  {i}. [{livre['isbn']}] {livre['titre']}")
        print(f"      Emprunté par : {dernier['emprunteur']}")
        print(f"      Date emprunt : {dernier['date_emprunt']}")

    # Choisir le livre à retourner
    while True:
        try:
            choix = int(input("\nNuméro du livre à retourner : "))
            if 1 <= choix <= len(empruntes):
                break
            else:
                print(f" Entrez un numéro entre 1 et {len(empruntes)}!")
        except ValueError:
            print(" Entrez un numéro valide!")

    livre_choisi = empruntes[choix - 1]

    # Enregistrement du retour
    date_retour = datetime.now().strftime("%Y-%m-%d")

    for livre in livres:
        if livre['isbn'] == livre_choisi['isbn']:
            livre['disponible'] = True
            livre['emprunts'][-1]['date_retour'] = date_retour
            break

    sauvegarder_bibliotheque(livres)

    dernier_emprunt = livre_choisi['emprunts'][-1]
    print(f"\n Livre retourné avec succès!")
    print(f"   Titre       : {livre_choisi['titre']}")
    print(f"   Emprunteur  : {dernier_emprunt['emprunteur']}")
    print(f"   Date retour : {date_retour}")

# ============================================================
# STATISTIQUES
# ============================================================
def afficher_statistiques(livres):
    """Affiche les statistiques de la bibliothèque."""
    print("\n STATISTIQUES DE LA BIBLIOTHÈQUE")
    print("=" * 50)

    if not livres:
        print(" Aucun livre enregistré!")
        return

    # ---- Statistiques générales ----
    total_livres      = len(livres)
    total_disponibles = sum(1 for l in livres if l['disponible'])
    total_empruntes   = sum(1 for l in livres if not l['disponible'])
    total_emprunts    = sum(len(l['emprunts']) for l in livres)

    print(f"\n GÉNÉRAL")
    print(f"   Total livres       : {total_livres}")
    print(f"   Livres disponibles : {total_disponibles}")
    print(f"   Livres empruntés   : {total_empruntes}")
    print(f"   Total emprunts     : {total_emprunts}")

    # ---- Livre le plus emprunté ----
    if total_emprunts > 0:
        print(f"\n LIVRE LE PLUS EMPRUNTÉ")
        livre_populaire = max(livres, key=lambda l: len(l['emprunts']))
        print(f"   Titre  : {livre_populaire['titre']}")
        print(f"   Auteur : {livre_populaire['auteur']}")
        print(f"   Nombre d'emprunts : {len(livre_populaire['emprunts'])}")

    # ---- Auteur le plus représenté ----
    if livres:
        print(f"\n  AUTEUR LE PLUS REPRÉSENTÉ")
        auteurs = {}
        for livre in livres:
            auteur = livre['auteur']
            auteurs[auteur] = auteurs.get(auteur, 0) + 1

        auteur_top = max(auteurs, key=auteurs.get)
        print(f"   Auteur : {auteur_top}")
        print(f"   Nombre de livres : {auteurs[auteur_top]}")

    # ---- Historique des emprunteurs ----
    if total_emprunts > 0:
        print(f"\n EMPRUNTEURS LES PLUS ACTIFS")
        emprunteurs = {}
        for livre in livres:
            for emprunt in livre['emprunts']:
                nom = emprunt['emprunteur']
                emprunteurs[nom] = emprunteurs.get(nom, 0) + 1

        # Trier par nombre d'emprunts décroissant
        classement = sorted(
            emprunteurs.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for rang, (nom, nb) in enumerate(classement[:5], 1):
            print(f"   {rang}. {nom} — {nb} emprunt(s)")

    # ---- Taux de disponibilité ----
    taux = (total_disponibles / total_livres) * 100
    print(f"\n TAUX DE DISPONIBILITÉ")
    print(f"   {taux:.1f}% des livres sont disponibles")

    # Barre de progression visuelle
    barre = int(taux / 5)
    print(f"   [{'█' * barre}{'░' * (20 - barre)}] {taux:.1f}%")

    print("\n" + "=" * 50)

    # ============================================================
# MENU PRINCIPAL
# ============================================================
def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 55)
    print("        📚 GESTION DE LA BIBLIOTHÈQUE 📚")
    print("=" * 55)
    print("  1. Ajouter un livre")
    print("  2. Afficher tous les livres")
    print("  3. Rechercher un livre")
    print("  4. Emprunter un livre")
    print("  5. Retourner un livre")
    print("  6. Statistiques")
    print("  0. Quitter")
    print("=" * 55)


def main():
    """Fonction principale — point d'entrée du programme."""
    print("\n" + "=" * 55)
    print("   Bienvenue dans le systeme de Gestion Bibliotheque")
    print("=" * 55)

    # Charger les données au démarrage
    livres = charger_bibliotheque()
    print(f"   {len(livres)} livre(s) charge(s) depuis la base de donnees.")

    while True:
        afficher_menu()

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            ajouter_livre(livres)
        elif choix == "2":
            afficher_livres(livres)
        elif choix == "3":
            rechercher_livre(livres)
        elif choix == "4":
            emprunter_livre(livres)
        elif choix == "5":
            retourner_livre(livres)
        elif choix == "6":
            afficher_statistiques(livres)
        elif choix == "0":
            print("\nAu revoir! A bientot!")
            break
        else:
            print("\nChoix invalide! Entrez un numero entre 0 et 6.")


# ============================================================
# POINT D'ENTREE
# ============================================================
# Point d'entrée
if __name__ == "__main__":
    main()