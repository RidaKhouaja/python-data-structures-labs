import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['axes.unicode_minus'] = False

DOSSIER_GRAPHES = "Graphiques"


# CRÉER LE DOSSIER DE GRAPHIQUES  

def creer_dossier_graphes():
    """Creer le dossier pour stockeer les ghraphiques ."""

    if not os.path.exists(DOSSIER_GRAPHES):
        os.makedirs(DOSSIER_GRAPHES)
        print(f"Dossier {DOSSIER_GRAPHES} CREER avec succes.")

#Graphique 1 _HISTOGRAMME : CA PAR PRODUIT

def graphique_ca_produit(df):
    """Histogramme du chiffre d'affaires par produit."""
    ca_par_produit = df.groupby('Produit')['Chiffre_Affaires'].sum()
    ca_par_produit = ca_par_produit.sort_values(ascending=False)

    couleurs = ['#1F4E79', '#4472C4', '#ED7D31', '#548235']

    fig, ax = plt.subplots(figsize=(10, 6))

    barres = ax.bar(
        ca_par_produit.index,
        ca_par_produit.values,
        color=couleurs,
        edgecolor='white',
        linewidth=1.5
    )
     # Valeurs sur les barres
    for barre in barres:
        hauteur = barre.get_height()
        ax.text(
            barre.get_x() + barre.get_width() / 2,
            hauteur + 500,
            f'{hauteur:,.0f} DH',
            ha='center', va='bottom',
            fontsize=10, fontweight='bold',
            color='#1F4E79'
        )
        ax.set_title(
        "Chiffre d'Affaires par Produit",
        fontsize=16, fontweight='bold', color='#1F4E79', pad=20
    )
    ax.set_xlabel("Produit", fontsize=12)
    ax.set_ylabel("Chiffre d'Affaires (DH)", fontsize=12)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    chemin = os.path.join(DOSSIER_GRAPHES, 'ca_par_produit.png')
    plt.savefig(chemin, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Graphique sauvegarde : {chemin}")

    # ============================================================
# GRAPHIQUE 2 — COURBE : ÉVOLUTION CA PAR MOIS
# ============================================================
def graphique_evolution_mois(df):
    """Courbe de l'évolution du CA par mois."""
    ca_par_mois = df.groupby('Mois')['Chiffre_Affaires'].sum()

    mois_noms = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jun']

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        mois_noms,
        ca_par_mois.values,
        color='#1F4E79',
        linewidth=2.5,
        marker='o',
        markersize=8,
        markerfacecolor='#ED7D31',
        markeredgecolor='white',
        markeredgewidth=2
    )

    # Remplissage sous la courbe
    ax.fill_between(
        mois_noms,
        ca_par_mois.values,
        alpha=0.15,
        color='#4472C4'
    )

    # Valeurs sur les points
    for i, (mois, valeur) in enumerate(zip(mois_noms, ca_par_mois.values)):
        ax.annotate(
            f'{valeur:,.0f}',
            (mois, valeur),
            textcoords="offset points",
            xytext=(0, 12),
            ha='center',
            fontsize=9,
            fontweight='bold',
            color='#1F4E79'
        )

    ax.set_title(
        "Evolution du Chiffre d'Affaires par Mois",
        fontsize=16, fontweight='bold', color='#1F4E79', pad=20
    )
    ax.set_xlabel("Mois", fontsize=12)
    ax.set_ylabel("Chiffre d'Affaires (DH)", fontsize=12)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    ax.grid(alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    chemin = os.path.join(DOSSIER_GRAPHES, 'evolution_mois.png')
    plt.savefig(chemin, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Graphique sauvegarde : {chemin}")



# ============================================================
# GRAPHIQUE 3 — DIAGRAMME CIRCULAIRE : RÉPARTITION VENTES
# ============================================================
def graphique_repartition_produits(df):
    """Diagramme circulaire de la répartition des ventes."""
    ventes_par_produit = df.groupby('Produit')['Quantite'].sum()
    ventes_par_produit = ventes_par_produit.sort_values(ascending=False)

    couleurs   = ['#1F4E79', '#4472C4', '#ED7D31', '#548235']
    explode    = [0.05] * len(ventes_par_produit)

    fig, ax = plt.subplots(figsize=(9, 7))

    wedges, texts, autotexts = ax.pie(
        ventes_par_produit.values,
        labels=ventes_par_produit.index,
        colors=couleurs,
        explode=explode,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.75,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )

    # Style des textes
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title(
        "Repartition des Ventes par Produit (Quantite)",
        fontsize=16, fontweight='bold', color='#1F4E79', pad=20
    )

    # Légende
    ax.legend(
        wedges,
        [f"{p} ({q} unites)" for p, q in
         zip(ventes_par_produit.index, ventes_par_produit.values)],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
        fontsize=10
    )

    plt.tight_layout()
    chemin = os.path.join(DOSSIER_GRAPHES, 'repartition_produits.png')
    plt.savefig(chemin, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Graphique sauvegarde : {chemin}")

# ============================================================
# GRAPHIQUE 4 — TOP 5 VENTES
# ============================================================
def graphique_top5(df):
    """Histogramme horizontal du top 5 des ventes."""
    df_top5 = df.nlargest(5, 'Chiffre_Affaires').copy()
    df_top5['Label'] = df_top5['Produit'] + '\n' + df_top5['Date'].dt.strftime('%d/%m/%Y')

    fig, ax = plt.subplots(figsize=(10, 6))

    couleurs = ['#1F4E79', '#4472C4', '#ED7D31', '#548235', '#C00000']

    barres = ax.barh(
        df_top5['Label'],
        df_top5['Chiffre_Affaires'],
        color=couleurs,
        edgecolor='white',
        linewidth=1.5,
        height=0.6
    )

    # Valeurs sur les barres
    for barre in barres:
        largeur = barre.get_width()
        ax.text(
            largeur + 200,
            barre.get_y() + barre.get_height() / 2,
            f'{largeur:,.0f} DH',
            ha='left', va='center',
            fontsize=10, fontweight='bold',
            color='#1F4E79'
        )

    ax.set_title(
        "Top 5 des Meilleures Ventes",
        fontsize=16, fontweight='bold', color='#1F4E79', pad=20
    )
    ax.set_xlabel("Chiffre d'Affaires (DH)", fontsize=12)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    ax.grid(axis='x', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis()

    plt.tight_layout()
    chemin = os.path.join(DOSSIER_GRAPHES, 'top5_ventes.png')
    plt.savefig(chemin, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Graphique sauvegarde : {chemin}")
