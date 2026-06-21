-- ============================================================
-- Vues Power BI pour MACROBUS
-- Utilisation : mysql -u root -p MacroBus_Production < powerbi_views.sql
-- ============================================================

-- 1. Vue principale : toutes les ventes avec leurs dimensions
CREATE OR REPLACE VIEW Ventes_Complete AS
SELECT
    fv.id_vente,
    fv.quantite,
    fv.prix_facture,
    fv.montant_total,
    -- Dimensions temps
    dt.date_complete,
    dt.annee,
    dt.mois,
    dt.mois_nom,
    dt.trimestre,
    dt.jour,
    dt.jour_semaine,
    dt.nom_jour,
    -- Dimensions vehicule
    dv.id_vehicule,
    dv.code_vehicule,
    dv.nom_vehicule,
    dv.prix_unitaire AS prix_catalogue,
    dv.libelle_categorie AS categorie,
    -- Dimensions commercial
    dc.id_commercial,
    dc.nom AS commercial_nom,
    dc.prenom AS commercial_prenom,
    CONCAT(dc.prenom, ' ', dc.nom) AS commercial_nom_complet,
    dc.nom_filiale AS filiale,
    dc.ville,
    dc.nom_territoire AS territoire,
    dc.pays,
    -- Dimensions commande
    dco.numero_commande
FROM Fact_Ventes fv
JOIN Dim_Temps dt ON fv.date_complete = dt.date_complete
JOIN Dim_Vehicule dv ON fv.id_vehicule = dv.id_vehicule
JOIN Dim_Commercial dc ON fv.id_commercial = dc.id_commercial
JOIN Dim_Commande dco ON fv.id_commande = dco.id_commande;

-- 2. Vue : CA par commercial
CREATE OR REPLACE VIEW Ventes_Par_Commercial AS
SELECT
    dc.id_commercial,
    CONCAT(dc.prenom, ' ', dc.nom) AS commercial,
    dc.nom_filiale AS filiale,
    dc.ville,
    dc.pays,
    COUNT(DISTINCT fv.id_commande) AS nb_commandes,
    SUM(fv.quantite) AS nb_vehicules,
    ROUND(SUM(fv.montant_total), 0) AS ca_total,
    ROUND(AVG(fv.montant_total), 0) AS panier_moyen
FROM Fact_Ventes fv
JOIN Dim_Commercial dc ON fv.id_commercial = dc.id_commercial
GROUP BY dc.id_commercial, commercial, dc.nom_filiale, dc.ville, dc.pays;

-- 3. Vue : CA par mois
CREATE OR REPLACE VIEW Ventes_Par_Mois AS
SELECT
    dt.annee,
    dt.mois,
    dt.mois_nom,
    dt.trimestre,
    COUNT(DISTINCT fv.id_commande) AS nb_commandes,
    SUM(fv.quantite) AS nb_vehicules,
    ROUND(SUM(fv.montant_total), 0) AS ca_total
FROM Fact_Ventes fv
JOIN Dim_Temps dt ON fv.date_complete = dt.date_complete
GROUP BY dt.annee, dt.mois, dt.mois_nom, dt.trimestre
ORDER BY dt.annee, dt.mois;

-- 4. Vue : CA par categorie
CREATE OR REPLACE VIEW Ventes_Par_Categorie AS
SELECT
    dv.libelle_categorie AS categorie,
    COUNT(DISTINCT fv.id_commande) AS nb_commandes,
    SUM(fv.quantite) AS nb_vehicules,
    ROUND(SUM(fv.montant_total), 0) AS ca_total
FROM Fact_Ventes fv
JOIN Dim_Vehicule dv ON fv.id_vehicule = dv.id_vehicule
GROUP BY dv.libelle_categorie
ORDER BY ca_total DESC;

-- 5. Vue : CA par territoire
CREATE OR REPLACE VIEW Ventes_Par_Territoire AS
SELECT
    dc.pays,
    dc.nom_territoire AS territoire,
    COUNT(DISTINCT fv.id_commande) AS nb_commandes,
    ROUND(SUM(fv.montant_total), 0) AS ca_total
FROM Fact_Ventes fv
JOIN Dim_Commercial dc ON fv.id_commercial = dc.id_commercial
GROUP BY dc.pays, dc.nom_territoire
ORDER BY ca_total DESC;

-- 6. Vue : Top vehicules
CREATE OR REPLACE VIEW Top_Vehicules AS
SELECT
    dv.nom_vehicule,
    dv.libelle_categorie AS categorie,
    dv.prix_unitaire AS prix_catalogue,
    SUM(fv.quantite) AS total_vendus,
    ROUND(SUM(fv.montant_total), 0) AS ca_total
FROM Fact_Ventes fv
JOIN Dim_Vehicule dv ON fv.id_vehicule = dv.id_vehicule
GROUP BY dv.nom_vehicule, dv.libelle_categorie, dv.prix_unitaire
ORDER BY total_vendus DESC;

-- 7. Vue : KPIs globaux
CREATE OR REPLACE VIEW KPIs_Globaux AS
SELECT
    ROUND(SUM(montant_total), 0) AS ca_total,
    COUNT(DISTINCT id_commande) AS nb_commandes,
    SUM(quantite) AS nb_vehicules,
    ROUND(AVG(montant_total), 0) AS panier_moyen,
    (SELECT COUNT(*) FROM Dim_Commercial) AS nb_commerciaux,
    (SELECT COUNT(*) FROM Dim_Vehicule) AS nb_modeles;
