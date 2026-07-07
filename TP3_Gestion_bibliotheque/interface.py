import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from main import (charger_bibliotheque, sauvegarder_bibliotheque, ajouter_livre, afficher_statistiques)
                 
from datetime import datetime

# ============================================================
# COULEURS ET STYLE
# ============================================================
COULEURS = {
    "primary"    : "#1F4E79",
    "secondary"  : "#4472C4",
    "accent"     : "#ED7D31",
    "success"    : "#548235",
    "danger"     : "#C00000",
    "white"      : "#FFFFFF",
    "lightgray"  : "#F2F2F2",
    "darkgray"   : "#595959"
}

# ============================================================
# FENÊTRE PRINCIPALE
# ============================================================
class BibliothequeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Config fenêtre
        self.title("Gestion de la Bibliotheque")
        self.geometry("950x650")
        self.resizable(True, True)
        self.configure(bg=COULEURS["lightgray"])

        # Charger les données
        self.livres = charger_bibliotheque()

        # Construire l'interface
        self._creer_header()
        self._creer_sidebar()
        self._creer_zone_principale()
        self._creer_footer()

        # Afficher la page d'accueil
        self.afficher_accueil()

    # --------------------------------------------------------
    def _creer_header(self):
        """Crée la barre du haut."""
        header = tk.Frame(self, bg=COULEURS["primary"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="  Systeme de Gestion de la Bibliotheque",
            font=("Helvetica", 18, "bold"),
            bg=COULEURS["primary"],
            fg=COULEURS["white"]
        ).pack(side="left", padx=20, pady=15)

        # Nombre de livres (badge)
        self.lbl_total = tk.Label(
            header,
            text=f"  {len(self.livres)} livres  ",
            font=("Helvetica", 11),
            bg=COULEURS["accent"],
            fg=COULEURS["white"]
        )
        self.lbl_total.pack(side="right", padx=20, pady=20)

    # --------------------------------------------------------
    def _creer_sidebar(self):
        """Crée la barre latérale avec les boutons."""
        self.sidebar = tk.Frame(
            self, bg=COULEURS["primary"], width=200
        )
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="MENU",
            font=("Helvetica", 12, "bold"),
            bg=COULEURS["primary"],
            fg=COULEURS["accent"]
        ).pack(pady=(25, 10))

        # Boutons du menu
        boutons = [
            ("Accueil",           self.afficher_accueil),
            ("Tous les livres",   self.afficher_livres),
            ("Ajouter un livre",  self.form_ajouter),
            ("Emprunter",         self.form_emprunter),
            ("Retourner",         self.form_retourner),
            ("Rechercher",        self.form_rechercher),
            ("Statistiques",      self.afficher_stats),
            ("Quitter",           self.destroy),
        ]

        for texte, commande in boutons:
            btn = tk.Button(
                self.sidebar,
                text=texte,
                command=commande,
                font=("Helvetica", 11),
                bg=COULEURS["secondary"],
                fg=COULEURS["white"],
                activebackground=COULEURS["accent"],
                activeforeground=COULEURS["white"],
                relief="flat",
                cursor="hand2",
                width=18,
                pady=8
            )
            btn.pack(pady=4, padx=10)

    # --------------------------------------------------------
    def _creer_zone_principale(self):
        """Crée la zone centrale d'affichage."""
        self.zone = tk.Frame(self, bg=COULEURS["lightgray"])
        self.zone.pack(fill="both", expand=True, padx=15, pady=10)

    # --------------------------------------------------------
    def _creer_footer(self):
        """Crée le pied de page."""
        footer = tk.Frame(self, bg=COULEURS["primary"], height=30)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="FST Errachidia — 2025/2026 — Prof. Y. FARHAOUI",
            font=("Helvetica", 9),
            bg=COULEURS["primary"],
            fg=COULEURS["white"]
        ).pack(pady=5)

    # --------------------------------------------------------
    def _vider_zone(self):
        """Vide la zone principale."""
        for widget in self.zone.winfo_children():
            widget.destroy()

    # --------------------------------------------------------
    def _maj_badge(self):
        """Met à jour le badge du nombre de livres."""
        self.lbl_total.config(text=f"  {len(self.livres)} livres  ")

        # ============================================================
    # PAGE ACCUEIL
    # ============================================================
    def afficher_accueil(self):
        """Affiche la page d'accueil avec les statistiques rapides."""
        self._vider_zone()

        # Titre
        tk.Label(
            self.zone,
            text="Tableau de Bord",
            font=("Helvetica", 20, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=(20, 30))

        # Cartes statistiques
        frame_cartes = tk.Frame(self.zone, bg=COULEURS["lightgray"])
        frame_cartes.pack(pady=10)

        total      = len(self.livres)
        disponibles = sum(1 for l in self.livres if l['disponible'])
        empruntes  = total - disponibles
        total_emprunts = sum(len(l['emprunts']) for l in self.livres)

        cartes = [
            ("Total Livres",      total,          COULEURS["primary"]),
            ("Disponibles",       disponibles,    COULEURS["success"]),
            ("Empruntes",         empruntes,      COULEURS["danger"]),
            ("Total Emprunts",    total_emprunts, COULEURS["accent"]),
        ]

        for titre, valeur, couleur in cartes:
            carte = tk.Frame(
                frame_cartes,
                bg=couleur,
                width=160,
                height=100,
                relief="flat"
            )
            carte.pack(side="left", padx=12)
            carte.pack_propagate(False)

            tk.Label(
                carte,
                text=str(valeur),
                font=("Helvetica", 32, "bold"),
                bg=couleur,
                fg=COULEURS["white"]
            ).pack(pady=(15, 2))

            tk.Label(
                carte,
                text=titre,
                font=("Helvetica", 10),
                bg=couleur,
                fg=COULEURS["white"]
            ).pack()

        # Derniers livres ajoutés
        if self.livres:
            tk.Label(
                self.zone,
                text="Derniers livres ajoutés",
                font=("Helvetica", 14, "bold"),
                bg=COULEURS["lightgray"],
                fg=COULEURS["primary"]
            ).pack(pady=(30, 10))

            frame_derniers = tk.Frame(self.zone, bg=COULEURS["lightgray"])
            frame_derniers.pack()

            derniers = self.livres[-3:][::-1]
            for livre in derniers:
                statut_couleur = COULEURS["success"] if livre['disponible'] else COULEURS["danger"]
                statut_texte   = "Disponible" if livre['disponible'] else "Emprunte"

                ligne = tk.Frame(
                    frame_derniers,
                    bg=COULEURS["white"],
                    relief="flat"
                )
                ligne.pack(fill="x", pady=3, padx=20)

                tk.Label(
                    ligne,
                    text=f"  {livre['titre']}",
                    font=("Helvetica", 11, "bold"),
                    bg=COULEURS["white"],
                    fg=COULEURS["primary"],
                    width=35,
                    anchor="w"
                ).pack(side="left", padx=5, pady=8)

                tk.Label(
                    ligne,
                    text=livre['auteur'],
                    font=("Helvetica", 10),
                    bg=COULEURS["white"],
                    fg=COULEURS["darkgray"],
                    width=25,
                    anchor="w"
                ).pack(side="left")

                tk.Label(
                    ligne,
                    text=f"  {statut_texte}  ",
                    font=("Helvetica", 10, "bold"),
                    bg=statut_couleur,
                    fg=COULEURS["white"]
                ).pack(side="right", padx=10, pady=8)

    # ============================================================
    # PAGE LISTE DES LIVRES
    # ============================================================
    def afficher_livres(self):
        """Affiche tous les livres dans un tableau."""
        self._vider_zone()
        self.livres = charger_bibliotheque()

        tk.Label(
            self.zone,
            text="Catalogue des Livres",
            font=("Helvetica", 18, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=(15, 10))

        # Tableau avec scrollbar
        frame_tableau = tk.Frame(self.zone, bg=COULEURS["lightgray"])
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tableau)
        scrollbar.pack(side="right", fill="y")

        # Style du tableau
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=COULEURS["white"],
            foreground=COULEURS["darkgray"],
            rowheight=30,
            fieldbackground=COULEURS["white"],
            font=("Helvetica", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=COULEURS["primary"],
            foreground=COULEURS["white"],
            font=("Helvetica", 11, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", COULEURS["secondary"])]
        )

        # Créer le tableau
        colonnes = ("N°", "ISBN", "Titre", "Auteur", "Statut", "Emprunts")
        self.tableau = ttk.Treeview(
            frame_tableau,
            columns=colonnes,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        # Configurer les colonnes
        largeurs = [40, 150, 250, 180, 100, 80]
        for col, larg in zip(colonnes, largeurs):
            self.tableau.heading(col, text=col)
            self.tableau.column(col, width=larg, anchor="center")

        # Remplir le tableau
        for i, livre in enumerate(self.livres, 1):
            statut    = "Disponible" if livre['disponible'] else "Emprunte"
            nb_emprunts = len(livre['emprunts'])
            tag       = "dispo" if livre['disponible'] else "emprunte"

            self.tableau.insert(
                "", "end",
                values=(i, livre['isbn'], livre['titre'],
                        livre['auteur'], statut, nb_emprunts),
                tags=(tag,)
            )

        # Couleurs des lignes
        self.tableau.tag_configure("dispo",    background="#E8F5E9")
        self.tableau.tag_configure("emprunte", background="#FFEBEE")

        self.tableau.pack(fill="both", expand=True)
        scrollbar.config(command=self.tableau.yview)

        # Compteur
        tk.Label(
            self.zone,
            text=f"Total : {len(self.livres)} livre(s)",
            font=("Helvetica", 10, "italic"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["darkgray"]
        ).pack(pady=5)
        

        # ============================================================
    # FORMULAIRE AJOUTER
    # ============================================================
    def form_ajouter(self):
        """Formulaire d'ajout d'un livre."""
        self._vider_zone()

        tk.Label(
            self.zone,
            text="Ajouter un Livre",
            font=("Helvetica", 18, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=(20, 30))

        frame_form = tk.Frame(self.zone, bg=COULEURS["white"],
                              relief="flat", padx=30, pady=30)
        frame_form.pack(padx=50)

        champs = [("ISBN :", "isbn"),
                  ("Titre :", "titre"),
                  ("Auteur :", "auteur")]

        self.entries = {}

        for label, cle in champs:
            tk.Label(
                frame_form,
                text=label,
                font=("Helvetica", 11, "bold"),
                bg=COULEURS["white"],
                fg=COULEURS["primary"]
            ).pack(anchor="w", pady=(10, 2))

            entry = tk.Entry(
                frame_form,
                font=("Helvetica", 11),
                width=40,
                relief="solid",
                bd=1
            )
            entry.pack(ipady=6)
            self.entries[cle] = entry

        # Bouton Ajouter
        tk.Button(
            frame_form,
            text="Ajouter le livre",
            command=self._valider_ajouter,
            font=("Helvetica", 12, "bold"),
            bg=COULEURS["success"],
            fg=COULEURS["white"],
            relief="flat",
            cursor="hand2",
            pady=10,
            width=20
        ).pack(pady=(25, 5))

        # Bouton Annuler
        tk.Button(
            frame_form,
            text="Annuler",
            command=self.afficher_accueil,
            font=("Helvetica", 11),
            bg=COULEURS["danger"],
            fg=COULEURS["white"],
            relief="flat",
            cursor="hand2",
            pady=8,
            width=20
        ).pack(pady=5)

    def _valider_ajouter(self):
        """Valide et enregistre le nouveau livre."""
        isbn   = self.entries['isbn'].get().strip()
        titre  = self.entries['titre'].get().strip()
        auteur = self.entries['auteur'].get().strip()

        # Validations
        if not isbn or not titre or not auteur:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return

        if any(l['isbn'] == isbn for l in self.livres):
            messagebox.showerror("Erreur", f"L'ISBN '{isbn}' existe deja!")
            return

        # Créer le livre
        livre = {
            "isbn"       : isbn,
            "titre"      : titre,
            "auteur"     : auteur,
            "disponible" : True,
            "emprunts"   : []
        }

        self.livres.append(livre)
        sauvegarder_bibliotheque(self.livres)
        self._maj_badge()

        messagebox.showinfo("Succes", f"Livre '{titre}' ajoute avec succes!")
        self.afficher_livres()

    # ============================================================
    # FORMULAIRE EMPRUNTER
    # ============================================================
    def form_emprunter(self):
        """Formulaire d'emprunt d'un livre."""
        self._vider_zone()

        self.livres     = charger_bibliotheque()
        disponibles = [l for l in self.livres if l['disponible']]

        tk.Label(
            self.zone,
            text="Emprunter un Livre",
            font=("Helvetica", 18, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=(20, 10))

        if not disponibles:
            tk.Label(
                self.zone,
                text="Aucun livre disponible actuellement!",
                font=("Helvetica", 13),
                bg=COULEURS["lightgray"],
                fg=COULEURS["danger"]
            ).pack(pady=30)
            return

        frame_form = tk.Frame(self.zone, bg=COULEURS["white"],
                              relief="flat", padx=30, pady=20)
        frame_form.pack(padx=50, pady=10)

        # Liste déroulante des livres disponibles
        tk.Label(
            frame_form,
            text="Choisir un livre disponible :",
            font=("Helvetica", 11, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["primary"]
        ).pack(anchor="w", pady=(10, 4))

        titres_disponibles = [
            f"{l['titre']} — {l['auteur']}" for l in disponibles
        ]

        self.combo_livres = ttk.Combobox(
            frame_form,
            values=titres_disponibles,
            font=("Helvetica", 11),
            width=45,
            state="readonly"
        )
        self.combo_livres.pack(ipady=4)
        self.combo_livres.current(0)

        # Nom emprunteur
        tk.Label(
            frame_form,
            text="Nom de l'emprunteur :",
            font=("Helvetica", 11, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["primary"]
        ).pack(anchor="w", pady=(15, 4))

        self.entry_emprunteur = tk.Entry(
            frame_form,
            font=("Helvetica", 11),
            width=40,
            relief="solid",
            bd=1
        )
        self.entry_emprunteur.pack(ipady=6)

        # Boutons
        tk.Button(
            frame_form,
            text="Confirmer l'emprunt",
            command=lambda: self._valider_emprunt(disponibles),
            font=("Helvetica", 12, "bold"),
            bg=COULEURS["success"],
            fg=COULEURS["white"],
            relief="flat",
            cursor="hand2",
            pady=10,
            width=22
        ).pack(pady=(20, 5))

        tk.Button(
            frame_form,
            text="Annuler",
            command=self.afficher_accueil,
            font=("Helvetica", 11),
            bg=COULEURS["danger"],
            fg=COULEURS["white"],
            relief="flat",
            cursor="hand2",
            pady=8,
            width=22
        ).pack(pady=5)

    def _valider_emprunt(self, disponibles):
        """Valide et enregistre l'emprunt."""
        index      = self.combo_livres.current()
        emprunteur = self.entry_emprunteur.get().strip()

        if not emprunteur:
            messagebox.showerror("Erreur", "Le nom de l'emprunteur est obligatoire!")
            return

        livre_choisi = disponibles[index]
        date_aujourd_hui = datetime.now().strftime("%Y-%m-%d")

        for livre in self.livres:
            if livre['isbn'] == livre_choisi['isbn']:
                livre['disponible'] = False
                livre['emprunts'].append({
                    "emprunteur"   : emprunteur,
                    "date_emprunt" : date_aujourd_hui,
                    "date_retour"  : None
                })
                break

        sauvegarder_bibliotheque(self.livres)
        self._maj_badge()

        messagebox.showinfo(
            "Succes",
            f"Livre '{livre_choisi['titre']}'\nemprunte par {emprunteur}\nle {date_aujourd_hui}"
        )
        self.afficher_livres()

    # ============================================================
    # FORMULAIRE RETOURNER
    # ============================================================
    def form_retourner(self):
        """Formulaire de retour d'un livre."""
        self._vider_zone()

        self.livres  = charger_bibliotheque()
        empruntes = [l for l in self.livres if not l['disponible']]

        tk.Label(
            self.zone,
            text="Retourner un Livre",
            font=("Helvetica", 18, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=(20, 10))

        if not empruntes:
            tk.Label(
                self.zone,
                text="Aucun livre emprunte actuellement!",
                font=("Helvetica", 13),
                bg=COULEURS["lightgray"],
                fg=COULEURS["success"]
            ).pack(pady=30)
            return

        frame_form = tk.Frame(self.zone, bg=COULEURS["white"],
                              relief="flat", padx=30, pady=20)
        frame_form.pack(padx=50, pady=10)

        tk.Label(
            frame_form,
            text="Choisir le livre a retourner :",
            font=("Helvetica", 11, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["primary"]
        ).pack(anchor="w", pady=(10, 4))

        titres_empruntes = []
        for l in empruntes:
            dernier = l['emprunts'][-1]
            titres_empruntes.append(
                f"{l['titre']} — emprunte par {dernier['emprunteur']}"
            )

        self.combo_retour = ttk.Combobox(
            frame_form,
            values=titres_empruntes,
            font=("Helvetica", 11),
            width=50,
            state="readonly"
        )
        self.combo_retour.pack(ipady=4)
        self.combo_retour.current(0)

        tk.Button(
            frame_form,
            text="Confirmer le retour",
            command=lambda: self._valider_retour(empruntes),
            font=("Helvetica", 12, "bold"),
            bg=COULEURS["secondary"],
            fg=COULEURS["white"],
            relief="flat",
            cursor="hand2",
            pady=10,
            width=22
        ).pack(pady=(20, 5))

        tk.Button(
            frame_form,
            text="Annuler",
            command=self.afficher_accueil,
            font=("Helvetica", 11),
            bg=COULEURS["danger"],
            fg=COULEURS["white"],
            relief="flat",
            cursor="hand2",
            pady=8,
            width=22
        ).pack(pady=5)

    def _valider_retour(self, empruntes):
        """Valide et enregistre le retour."""
        index        = self.combo_retour.current()
        livre_choisi = empruntes[index]
        date_retour  = datetime.now().strftime("%Y-%m-%d")

        for livre in self.livres:
            if livre['isbn'] == livre_choisi['isbn']:
                livre['disponible']               = True
                livre['emprunts'][-1]['date_retour'] = date_retour
                break

        sauvegarder_bibliotheque(self.livres)
        self._maj_badge()

        messagebox.showinfo(
            "Succes",
            f"Livre '{livre_choisi['titre']}' retourne le {date_retour}"
        )
        self.afficher_livres()

    # ============================================================
    # FORMULAIRE RECHERCHER
    # ============================================================
    def form_rechercher(self):
        """Formulaire de recherche multicritère."""
        self._vider_zone()

        tk.Label(
            self.zone,
            text="Rechercher un Livre",
            font=("Helvetica", 18, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=(20, 15))

        frame_recherche = tk.Frame(self.zone, bg=COULEURS["white"],
                                   relief="flat", padx=20, pady=15)
        frame_recherche.pack(fill="x", padx=50)

        # Critère
        tk.Label(
            frame_recherche,
            text="Critere :",
            font=("Helvetica", 11, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["primary"]
        ).pack(side="left", padx=(0, 10))

        self.combo_critere = ttk.Combobox(
            frame_recherche,
            values=["Titre", "Auteur", "ISBN",
                    "Disponibles", "Empruntes"],
            font=("Helvetica", 11),
            width=15,
            state="readonly"
        )
        self.combo_critere.current(0)
        self.combo_critere.pack(side="left", padx=10, ipady=4)

        self.entry_recherche = tk.Entry(
            frame_recherche,
            font=("Helvetica", 11),
            width=25,
            relief="solid",
            bd=1
        )
        self.entry_recherche.pack(side="left", padx=10, ipady=4)

        tk.Button(
            frame_recherche,
            text="Rechercher",
            command=self._executer_recherche,
            font=("Helvetica", 11, "bold"),
            bg=COULEURS["secondary"],
            fg=COULEURS["white"],
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=4
        ).pack(side="left", padx=10)

        # Zone résultats
        self.frame_resultats = tk.Frame(
            self.zone, bg=COULEURS["lightgray"]
        )
        self.frame_resultats.pack(fill="both", expand=True,
                                  padx=50, pady=10)

    def _executer_recherche(self):
        """Exécute la recherche et affiche les résultats."""
        for w in self.frame_resultats.winfo_children():
            w.destroy()

        critere = self.combo_critere.get()
        terme   = self.entry_recherche.get().strip().lower()

        if critere == "Titre":
            resultats = [l for l in self.livres if terme in l['titre'].lower()]
        elif critere == "Auteur":
            resultats = [l for l in self.livres if terme in l['auteur'].lower()]
        elif critere == "ISBN":
            resultats = [l for l in self.livres if terme in l['isbn'].lower()]
        elif critere == "Disponibles":
            resultats = [l for l in self.livres if l['disponible']]
        else:
            resultats = [l for l in self.livres if not l['disponible']]

        tk.Label(
            self.frame_resultats,
            text=f"{len(resultats)} resultat(s) trouve(s)",
            font=("Helvetica", 12, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=10)

        for livre in resultats:
            statut_couleur = COULEURS["success"] if livre['disponible'] else COULEURS["danger"]
            statut_texte   = "Disponible" if livre['disponible'] else "Emprunte"

            ligne = tk.Frame(self.frame_resultats, bg=COULEURS["white"])
            ligne.pack(fill="x", pady=3)

            tk.Label(
                ligne,
                text=f"  {livre['titre']}",
                font=("Helvetica", 11, "bold"),
                bg=COULEURS["white"],
                fg=COULEURS["primary"],
                width=30,
                anchor="w"
            ).pack(side="left", padx=5, pady=8)

            tk.Label(
                ligne,
                text=livre['auteur'],
                font=("Helvetica", 10),
                bg=COULEURS["white"],
                fg=COULEURS["darkgray"],
                width=22,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                ligne,
                text=f"  {statut_texte}  ",
                font=("Helvetica", 10, "bold"),
                bg=statut_couleur,
                fg=COULEURS["white"]
            ).pack(side="right", padx=10, pady=8)

    # ============================================================
    # PAGE STATISTIQUES
    # ============================================================
    def afficher_stats(self):
        """Affiche les statistiques détaillées."""
        self._vider_zone()
        self.livres = charger_bibliotheque()

        tk.Label(
            self.zone,
            text="Statistiques de la Bibliotheque",
            font=("Helvetica", 18, "bold"),
            bg=COULEURS["lightgray"],
            fg=COULEURS["primary"]
        ).pack(pady=(20, 20))

        if not self.livres:
            tk.Label(
                self.zone,
                text="Aucun livre enregistre!",
                font=("Helvetica", 13),
                bg=COULEURS["lightgray"],
                fg=COULEURS["danger"]
            ).pack(pady=30)
            return

        total           = len(self.livres)
        disponibles     = sum(1 for l in self.livres if l['disponible'])
        empruntes       = total - disponibles
        total_emprunts  = sum(len(l['emprunts']) for l in self.livres)
        taux            = (disponibles / total * 100) if total > 0 else 0

        stats = [
            ("Total de livres",      total,         COULEURS["primary"]),
            ("Livres disponibles",   disponibles,   COULEURS["success"]),
            ("Livres empruntes",     empruntes,     COULEURS["danger"]),
            ("Total des emprunts",   total_emprunts,COULEURS["accent"]),
            ("Taux disponibilite",   f"{taux:.1f}%",COULEURS["secondary"]),
        ]

        frame_stats = tk.Frame(self.zone, bg=COULEURS["lightgray"])
        frame_stats.pack(pady=10)

        for i, (label, valeur, couleur) in enumerate(stats):
            ligne = tk.Frame(frame_stats, bg=COULEURS["white"])
            ligne.grid(row=i, column=0, sticky="ew",
                       pady=4, padx=20, ipadx=10, ipady=8)

            tk.Label(
                ligne,
                text=label,
                font=("Helvetica", 12),
                bg=COULEURS["white"],
                fg=COULEURS["darkgray"],
                width=25,
                anchor="w"
            ).pack(side="left", padx=15)

            tk.Label(
                ligne,
                text=str(valeur),
                font=("Helvetica", 13, "bold"),
                bg=couleur,
                fg=COULEURS["white"],
                width=10
            ).pack(side="right", padx=5, pady=4)

        # Livre le plus emprunté
        if total_emprunts > 0:
            populaire = max(self.livres, key=lambda l: len(l['emprunts']))
            tk.Label(
                self.zone,
                text=f"Livre le plus emprunte : {populaire['titre']} "
                     f"({len(populaire['emprunts'])} fois)",
                font=("Helvetica", 11, "italic"),
                bg=COULEURS["lightgray"],
                fg=COULEURS["accent"]
            ).pack(pady=15)


# ============================================================
# LANCEMENT
# ============================================================
if __name__ == "__main__":
    app = BibliothequeApp()
    app.mainloop()