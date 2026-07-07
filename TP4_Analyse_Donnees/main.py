from analyse import *
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib 
import os

# fix encodage Windows 
matplotlib.rcParams['axes.unicode_minus'] = False

# FICHIERS 

FICHIER_CSV = "Ventes.csv"
DOSSIER_GRAPHES = "Graphiques"


# CHAREGEMENT DES DONNEES 


    
def charger_donnees():
    """Charge et prépare les données depuis le fichier CSV."""
    if not os.path.exists(FICHIER_CSV):
        print(f"Erreur : fichier '{FICHIER_CSV}' introuvable!")
        return None

    df = pd.read_csv(FICHIER_CSV)
    df['Date']            = pd.to_datetime(df['Date'])
    df['Mois']            = df['Date'].dt.month
    df['Mois_Nom']        = df['Date'].dt.strftime('%B')
    df['Chiffre_Affaires'] = df['Quantite'] * df['Prix']

    print("Donnees chargees avec succes!")
    print(f"  Nombre de lignes : {len(df)}")
    print(f"  Periode          : {df['Date'].min().date()} -> {df['Date'].max().date()}")
    print(f"  Produits         : {', '.join(df['Produit'].unique())}")

    return df

# TRAITEMENTS 

def chiffre_affaires_total(df):
    """calculer le chiffre d'affaires total ."""

    total = df['chiffre_affaires'].sum()
    print(f"chiffre d'affaires total est : {total:.0f} DH")
    return total 

def produit_plus_vendu(df):
    """Trouve le produit le plus vendu en quantité."""
    ventes_par_produit = df.groupby('Produit')['Quantite'].sum()
    produit_top        = ventes_par_produit.idxmax()
    quantite_top       = ventes_par_produit.max()

    print(f"\nProduit le plus vendu : {produit_top} ({quantite_top} unites)")
    return ventes_par_produit

def mois_plus_rentable(df):
    """Trouve le mois le plus rentable."""
    ca_par_mois  = df.groupby('Mois_Nom')['Chiffre_Affaires'].sum()
    mois_top     = ca_par_mois.idxmax()
    ca_top       = ca_par_mois.max()

    print(f"\nMois le plus rentable : {mois_top} ({ca_top:,.0f} DH)")
    return ca_par_mois

def top5_ventes(df):
    """Affiche le top 5 des meilleures ventes."""
    df_top5 = df.nlargest(5, 'Chiffre_Affaires')[
        ['Date', 'Produit', 'Quantite', 'Prix', 'Chiffre_Affaires']
    ]

    print("\nTop 5 des meilleures ventes :")
    print("-" * 55)
    for i, row in df_top5.iterrows():
        print(f"  {row['Produit']:15} | "
              f"Qte: {row['Quantite']:3} | "
              f"Prix: {row['Prix']:6} DH | "
              f"CA: {row['Chiffre_Affaires']:8,.0f} DH")
    print("-" * 55)

    return df_top5




# ============================================================
# MENU PRINCIPAL
# ============================================================
def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 55)
    print("     ANALYSE DE DONNEES ET TABLEAUX DE BORD")
    print("=" * 55)
    print("  1. Charger et afficher les donnees")
    print("  2. Chiffre d'affaires total")
    print("  3. Produit le plus vendu")
    print("  4. Mois le plus rentable")
    print("  5. Top 5 des meilleures ventes")
    print("  6. Graphique - CA par produit (histogramme)")
    print("  7. Graphique - Evolution CA par mois (courbe)")
    print("  8. Graphique - Repartition produits (circulaire)")
    print("  9. Graphique - Top 5 ventes (barres horizontales)")
    print("  10. Generer TOUS les graphiques")
    print("  0. Quitter")
    print("=" * 55)


def main():
    """Fonction principale."""
    print("\n" + "=" * 55)
    print("   Bienvenue dans l'outil d'Analyse de Donnees")
    print("=" * 55)

    # Créer dossier graphiques
    creer_dossier_graphes()

    # Charger les données une seule fois
    df = charger_donnees()

    if df is None:
        print("Impossible de charger les donnees. Verifiez le fichier CSV.")
        return

    while True:
        afficher_menu()
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            print("\nAPERCU DES DONNEES")
            print("-" * 55)
            print(df.to_string(index=False))
            print(f"\nTotal lignes : {len(df)}")

        elif choix == "2":
            chiffre_affaires_total(df)

        elif choix == "3":
            produit_plus_vendu(df)

        elif choix == "4":
            mois_plus_rentable(df)

        elif choix == "5":
            top5_ventes(df)

        elif choix == "6":
            print("\nGeneration histogramme CA par produit...")
            graphique_ca_produit(df)

        elif choix == "7":
            print("\nGeneration courbe evolution CA par mois...")
            graphique_evolution_mois(df)

        elif choix == "8":
            print("\nGeneration diagramme circulaire...")
            graphique_repartition_produits(df)

        elif choix == "9":
            print("\nGeneration top 5 ventes...")
            graphique_top5(df)

        elif choix == "10":
            print("\nGeneration de tous les graphiques...")
            graphique_ca_produit(df)
            graphique_evolution_mois(df)
            graphique_repartition_produits(df)
            graphique_top5(df)
            print("\nTous les graphiques generes dans le dossier 'graphiques'!")

        elif choix == "0":
            print("\nAu revoir!")
            break

        else:
            print("\nChoix invalide! Entrez un numero entre 0 et 10.")


# ============================================================
# POINT D'ENTREE
# ============================================================
main()