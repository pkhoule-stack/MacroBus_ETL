-- ============================================================
-- Star Schema MACROBUS
-- Dimensions (dénormalisées) + Table de Faits
-- ============================================================

-- 1. Dimension Temps
CREATE TABLE IF NOT EXISTS Dim_Temps (
    date_complete DATE PRIMARY KEY,
    annee INT NOT NULL,
    mois INT NOT NULL,
    mois_nom VARCHAR(20) NOT NULL,
    trimestre INT NOT NULL,
    jour INT NOT NULL,
    jour_semaine INT NOT NULL,
    nom_jour VARCHAR(20) NOT NULL
);

-- 2. Dimension Produit (dénormalise Categorie)
CREATE TABLE IF NOT EXISTS Dim_Vehicule (
    id_vehicule INT PRIMARY KEY,
    code_vehicule VARCHAR(20) NOT NULL,
    nom_vehicule VARCHAR(100) NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    id_categorie INT,
    libelle_categorie VARCHAR(50)
);

-- 3. Dimension Commercial (dénormalise Filiale + Territoire)
CREATE TABLE IF NOT EXISTS Dim_Commercial (
    id_commercial INT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    id_filiale INT,
    nom_filiale VARCHAR(100),
    ville VARCHAR(50),
    id_territoire INT,
    nom_territoire VARCHAR(50),
    pays VARCHAR(50)
);

-- 4. Dimension Commande
CREATE TABLE IF NOT EXISTS Dim_Commande (
    id_commande INT PRIMARY KEY,
    numero_commande VARCHAR(20) NOT NULL
);

-- 5. Table de Faits Ventes
CREATE TABLE IF NOT EXISTS Fact_Ventes (
    id_vente INT PRIMARY KEY AUTO_INCREMENT,
    id_commande INT NOT NULL,
    id_vehicule INT NOT NULL,
    id_commercial INT NOT NULL,
    date_complete DATE NOT NULL,
    quantite INT NOT NULL,
    prix_facture DECIMAL(10,2) NOT NULL,
    montant_total DECIMAL(10,2) GENERATED ALWAYS AS (quantite * prix_facture) STORED,
    FOREIGN KEY (id_commande) REFERENCES Dim_Commande(id_commande),
    FOREIGN KEY (id_vehicule) REFERENCES Dim_Vehicule(id_vehicule),
    FOREIGN KEY (id_commercial) REFERENCES Dim_Commercial(id_commercial),
    FOREIGN KEY (date_complete) REFERENCES Dim_Temps(date_complete)
);

-- ============================================================
-- ETL : Alimentation du Star Schema
-- ============================================================

-- 1. Remplir Dim_Temps à partir des dates des commandes
INSERT IGNORE INTO Dim_Temps (date_complete, annee, mois, mois_nom, trimestre, jour, jour_semaine, nom_jour)
SELECT DISTINCT
    c.date_commande,
    YEAR(c.date_commande),
    MONTH(c.date_commande),
    CASE MONTH(c.date_commande)
        WHEN 1 THEN 'Janvier' WHEN 2 THEN 'Février' WHEN 3 THEN 'Mars'
        WHEN 4 THEN 'Avril' WHEN 5 THEN 'Mai' WHEN 6 THEN 'Juin'
        WHEN 7 THEN 'Juillet' WHEN 8 THEN 'Août' WHEN 9 THEN 'Septembre'
        WHEN 10 THEN 'Octobre' WHEN 11 THEN 'Novembre' WHEN 12 THEN 'Décembre'
    END,
    CEIL(MONTH(c.date_commande) / 3.0),
    DAY(c.date_commande),
    DAYOFWEEK(c.date_commande),
    CASE DAYOFWEEK(c.date_commande)
        WHEN 1 THEN 'Dimanche' WHEN 2 THEN 'Lundi' WHEN 3 THEN 'Mardi'
        WHEN 4 THEN 'Mercredi' WHEN 5 THEN 'Jeudi' WHEN 6 THEN 'Vendredi'
        WHEN 7 THEN 'Samedi'
    END
FROM Commandes c;

-- 2. Remplir Dim_Vehicule
INSERT IGNORE INTO Dim_Vehicule
SELECT
    p.id_vehicule,
    p.code_vehicule,
    p.nom_vehicule,
    p.prix_unitaire,
    p.id_categorie,
    cp.libelle_categorie
FROM Vehicules p
LEFT JOIN Categories_Vehicule cp ON p.id_categorie = cp.id_categorie;

-- 3. Remplir Dim_Commercial
INSERT IGNORE INTO Dim_Commercial
SELECT
    c.id_commercial,
    c.nom,
    c.prenom,
    c.id_filiale,
    f.nom_filiale,
    f.ville,
    f.id_territoire,
    t.nom_territoire,
    t.pays
FROM Commerciaux c
LEFT JOIN Filiales f ON c.id_filiale = f.id_filiale
LEFT JOIN Territoires t ON f.id_territoire = t.id_territoire;

-- 4. Remplir Dim_Commande
INSERT IGNORE INTO Dim_Commande
SELECT id_commande, numero_commande
FROM Commandes;

-- 5. Remplir Fact_Ventes
INSERT INTO Fact_Ventes (id_commande, id_vehicule, id_commercial, date_complete, quantite, prix_facture)
SELECT
    c.id_commande,
    lc.id_vehicule,
    c.id_commercial,
    c.date_commande,
    lc.quantite,
    lc.prix_facture
FROM Lignes_Commande lc
JOIN Commandes c ON lc.id_commande = c.id_commande;
