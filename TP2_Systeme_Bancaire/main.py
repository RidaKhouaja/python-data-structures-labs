"""
============================================================
  TP2 - Systeme Bancaire Simplifie
  Module : Fondamentaux des Structures de Donnees en Python
  Professeur : Y. FARHAOUI
  Etudiant   : Rida KHOUAJA
  Annee      : 2025/2026
============================================================
"""

import json
import os
from datetime import datetime

FICHIER_JSON = "comptes.json"


# ════════════════════════════════════════════════════════════
# UTILITAIRES : Chargement & Sauvegarde
# ════════════════════════════════════════════════════════════

def charger_comptes():
    """Charge la liste des comptes a partir du fichier."""
    if not os.path.exists(FICHIER_JSON):
        return []
    with open(FICHIER_JSON, "r", encoding="utf-8") as f:
        contenu = f.read().strip()
        if not contenu:
            return []
        return json.loads(contenu)


def sauvegarder_comptes(comptes):
    """Ecrire la liste des comptes dans le fichier."""
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(comptes, f, ensure_ascii=False, indent=4)


# ════════════════════════════════════════════════════════════
# UTILITAIRE : Trouver un compte par numero
# ════════════════════════════════════════════════════════════

def trouver_compte(comptes, numero):
    """Retourne le compte correspondant au numero, ou None."""
    for compte in comptes:
        if compte["numero"] == numero:
            return compte
    return None


# ════════════════════════════════════════════════════════════
# FONCTION 1 : Creer un compte
# ════════════════════════════════════════════════════════════

def creer_compte():
    """Cree un nouveau compte avec numero auto, titulaire et solde initial."""
    comptes = charger_comptes()

    print("\n--- Creation d'un nouveau compte ---")

    if comptes:
        dernier = int(comptes[-1]["numero"].replace("CPT", ""))
        nouveau_num = f"CPT{dernier + 1:03d}"
    else:
        nouveau_num = "CPT001"

    titulaire = input("Nom du titulaire : ").strip()
    if not titulaire:
        print("Erreur : Le nom ne peut pas etre vide.")
        return

    try:
        solde = float(input("Solde initial (MAD) : "))
        if solde < 0:
            print("Erreur : Le solde initial ne peut pas etre negatif.")
            return
    except ValueError:
        print("Erreur : Montant invalide.")
        return

    nouveau_compte = {
        "numero"    : nouveau_num,
        "titulaire" : titulaire,
        "solde"     : solde,
        "historique": [{
            "type"   : "Ouverture de compte",
            "montant": solde,
            "date"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }]
    }

    comptes.append(nouveau_compte)
    sauvegarder_comptes(comptes)

    print(f"\nCompte cree avec succes !")
    print(f"   Numero    : {nouveau_num}")
    print(f"   Titulaire : {titulaire}")
    print(f"   Solde     : {solde:.2f} MAD")


# ════════════════════════════════════════════════════════════
# FONCTION 2 : Depot
# ════════════════════════════════════════════════════════════

def deposer():
    """Ajoute un montant au solde d'un compte existant."""
    comptes = charger_comptes()

    print("\n--- Depot ---")
    numero = input("Numero de compte : ").strip().upper()

    compte = trouver_compte(comptes, numero)
    if not compte:
        print(f"Erreur : Compte {numero} introuvable.")
        return

    try:
        montant = float(input("Montant a deposer (MAD) : "))
        if montant <= 0:
            print("Erreur : Le montant doit etre positif.")
            return
    except ValueError:
        print("Erreur : Montant invalide.")
        return

    compte["solde"] += montant
    compte["historique"].append({
        "type"   : "Depot",
        "montant": montant,
        "date"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    sauvegarder_comptes(comptes)
    print(f"\nDepot de {montant:.2f} MAD effectue.")
    print(f"   Nouveau solde : {compte['solde']:.2f} MAD")


# ════════════════════════════════════════════════════════════
# FONCTION 3 : Retrait
# ════════════════════════════════════════════════════════════

def retirer():
    """Retire un montant. Contrainte : solde jamais negatif."""
    comptes = charger_comptes()

    print("\n--- Retrait ---")
    numero = input("Numero de compte : ").strip().upper()

    compte = trouver_compte(comptes, numero)
    if not compte:
        print(f"Erreur : Compte {numero} introuvable.")
        return

    try:
        montant = float(input("Montant a retirer (MAD) : "))
        if montant <= 0:
            print("Erreur : Le montant doit etre positif.")
            return
    except ValueError:
        print("Erreur : Montant invalide.")
        return

    if montant > compte["solde"]:
        print(f"Erreur : Solde insuffisant. Solde actuel : {compte['solde']:.2f} MAD")
        return

    compte["solde"] -= montant
    compte["historique"].append({
        "type"   : "Retrait",
        "montant": montant,
        "date"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    sauvegarder_comptes(comptes)
    print(f"\nRetrait de {montant:.2f} MAD effectue.")
    print(f"   Nouveau solde : {compte['solde']:.2f} MAD")


# ════════════════════════════════════════════════════════════
# FONCTION 4 : Virement
# ════════════════════════════════════════════════════════════

def virer():
    """Transfere un montant d'un compte source vers un compte destination."""
    comptes = charger_comptes()

    print("\n--- Virement ---")
    num_source = input("Numero du compte source      : ").strip().upper()
    num_dest   = input("Numero du compte destination : ").strip().upper()

    if num_source == num_dest:
        print("Erreur : Impossible de virer vers le meme compte.")
        return

    source = trouver_compte(comptes, num_source)
    dest   = trouver_compte(comptes, num_dest)

    if not source:
        print(f"Erreur : Compte source {num_source} introuvable.")
        return
    if not dest:
        print(f"Erreur : Compte destination {num_dest} introuvable.")
        return

    try:
        montant = float(input("Montant a virer (MAD) : "))
        if montant <= 0:
            print("Erreur : Le montant doit etre positif.")
            return
    except ValueError:
        print("Erreur : Montant invalide.")
        return

    if montant > source["solde"]:
        print(f"Erreur : Solde insuffisant. Solde source : {source['solde']:.2f} MAD")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    source["solde"] -= montant
    source["historique"].append({
        "type"   : f"Virement vers {num_dest}",
        "montant": montant,
        "date"   : timestamp
    })

    dest["solde"] += montant
    dest["historique"].append({
        "type"   : f"Virement recu de {num_source}",
        "montant": montant,
        "date"   : timestamp
    })

    sauvegarder_comptes(comptes)
    print(f"\nVirement de {montant:.2f} MAD effectue.")
    print(f"   {num_source} ({source['titulaire']}) --> {num_dest} ({dest['titulaire']})")


# ════════════════════════════════════════════════════════════
# FONCTION 5 : Consulter le solde
# ════════════════════════════════════════════════════════════

def consulter_solde():
    """Affiche le solde actuel et l'historique complet des operations."""
    comptes = charger_comptes()

    print("\n--- Consultation du solde ---")
    numero = input("Numero de compte : ").strip().upper()

    compte = trouver_compte(comptes, numero)
    if not compte:
        print(f"Erreur : Compte {numero} introuvable.")
        return

    print(f"\n{'='*48}")
    print(f"  Compte    : {compte['numero']}")
    print(f"  Titulaire : {compte['titulaire']}")
    print(f"  Solde     : {compte['solde']:.2f} MAD")
    print(f"{'-'*48}")
    print(f"  Historique des operations :")
    print(f"{'-'*48}")

    for op in compte["historique"]:
        print(f"  [{op['date']}]  {op['type']:<25} {op['montant']:>10.2f} MAD")

    print(f"{'='*48}")


# ════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ════════════════════════════════════════════════════════════

def menu():
    """Affiche le menu principal et gere la navigation."""
    while True:
        print("\n" + "="*45)
        print("     SYSTEME BANCAIRE SIMPLIFIE")
        print("="*45)
        print("  1. Creer un compte")
        print("  2. Depot")
        print("  3. Retrait")
        print("  4. Virement")
        print("  5. Consulter le solde")
        print("  0. Quitter")
        print("="*45)

        choix = input("  Votre choix : ").strip()

        if   choix == "1": creer_compte()
        elif choix == "2": deposer()
        elif choix == "3": retirer()
        elif choix == "4": virer()
        elif choix == "5": consulter_solde()
        elif choix == "0":
            print("\nAu revoir !\n")
            break
        else:
            print("Choix invalide. Veuillez reessayer.")


# ─── Point d'entree ─────────────────────────────────────
menu()