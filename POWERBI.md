# Connexion Power BI à MACROBUS

## 1. Créer les vues Power BI dans MySQL

```bash
mysql -u root -p MacroBus_Production < powerbi_views.sql
```

Cela crée 7 vues optimisées pour Power BI :
- `Ventes_Complete` — toutes les ventes avec toutes les dimensions
- `Ventes_Par_Commercial` — CA par vendeur
- `Ventes_Par_Mois` — CA par mois
- `Ventes_Par_Categorie` — CA par catégorie
- `Ventes_Par_Territoire` — CA par pays
- `Top_Vehicules` — classement des modèles
- `KPIs_Globaux` — indicateurs clés

## 2. Ouvrir avec Power BI Desktop

**Option A** — Fichier .pbids :
Double-cliquer sur `MacroBus.pbids` → entrer le mot de passe MySQL.

**Option B** — Manuellement :
1. Power BI Desktop → **Obtenir des données** → **MySQL**
2. Serveur : `localhost:3306`
3. Base de données : `MacroBus_Production`
4. Mode : **Importer** (recommandé)
5. Sélectionner les vues `Ventes_*` et `Top_Vehicules`

## 3. Créer les visuels

### Page 1 — Tableau de bord
- **Carte** : CA total (KPIs_Globaux.ca_total)
- **Carte** : Nb commandes
- **Carte** : Panier moyen
- **Histogramme** : CA par mois (Ventes_Par_Mois)
- **Barre** : CA par pays (Ventes_Par_Territoire)

### Page 2 — Analyse commerciale
- **Tableau** : Ventes_Par_Commercial
- **Barre** : Top 10 commerciaux par CA
- **Treemap** : CA par filiale

### Page 3 — Analyse produits
- **Barre** : Top_Vehicules
- **Donut** : CA par catégorie (Ventes_Par_Categorie)
- **Matrice** : Ventes_Complete (année × catégorie)

## 4. Schéma du modèle de données

Si vous importez les tables directement (sans vues) :

```
Dim_Temps (date_complete) ──┐
                            ├── Fact_Ventes (date_complete)
Dim_Vehicule (id_vehicule) ─┤
                            ├── Fact_Ventes (id_vehicule)
Dim_Commercial (id_commercial) ─┤
                                ├── Fact_Ventes (id_commercial)
Dim_Commande (id_commande) ─────┘
```

Power BI détecte automatiquement les relations si vous importez les tables du star schema.

## 5. Rafraîchissement

- **Manuel** : Accueil → Actualiser
- **Automatique** : Power BI Service → Planifier l'actualisation (nécessite une passerelle MySQL)
