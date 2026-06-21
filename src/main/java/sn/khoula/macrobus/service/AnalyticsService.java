package sn.khoula.macrobus.service;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class AnalyticsService {

    private final JdbcTemplate jdbcTemplate;

    public AnalyticsService(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public List<Map<String, Object>> caParCommercial() {
        return jdbcTemplate.queryForList("""
            SELECT c.nom, c.prenom, c.nom_filiale, c.pays,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   SUM(fv.quantite) AS nb_vehicules,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total
            FROM MacroBus_Production.Fait_Ventes fv
            JOIN Dim_Commercial c ON fv.id_commercial = c.id_commercial
            GROUP BY c.id_commercial
            ORDER BY ca_total DESC
        """);
    }

    public List<Map<String, Object>> caParCategorie() {
        return jdbcTemplate.queryForList("""
            SELECT p.libelle_categorie,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   SUM(fv.quantite) AS nb_vehicules,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total
            FROM Fait_Ventes fv
            JOIN Dim_Vehicule p ON fv.id_vehicule = p.id_vehicule
            GROUP BY p.libelle_categorie
            ORDER BY ca_total DESC
        """);
    }

    public List<Map<String, Object>> caParTerritoire() {
        return jdbcTemplate.queryForList("""
            SELECT c.pays, c.nom_territoire,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total
            FROM Fact_Ventes fv
            JOIN Dim_Commercial c ON fv.id_commercial = c.id_commercial
            GROUP BY c.pays, c.nom_territoire
            ORDER BY ca_total DESC
        """);
    }

    public List<Map<String, Object>> caParPeriode() {
        return jdbcTemplate.queryForList("""
            SELECT t.annee, t.mois_nom, t.mois, t.trimestre,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total
            FROM Fact_Ventes fv
            JOIN Dim_Temps t ON fv.date_complete = t.date_complete
            GROUP BY t.annee, t.mois_nom, t.mois, t.trimestre
            ORDER BY t.annee DESC, t.mois DESC
        """);
    }

    public List<Map<String, Object>> topVehicules(int limit) {
        return jdbcTemplate.queryForList("""
            SELECT p.nom_vehicule, p.libelle_categorie, p.prix_unitaire,
                   SUM(fv.quantite) AS total_vendus,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total
            FROM Fact_Ventes fv
            JOIN Dim_Vehicule p ON fv.id_vehicule = p.id_vehicule
            GROUP BY p.id_vehicule
            ORDER BY total_vendus DESC
            LIMIT ?
        """, limit);
    }

    public List<Map<String, Object>> topCommerciaux(int limit) {
        return jdbcTemplate.queryForList("""
            SELECT c.nom, c.prenom, c.nom_filiale, c.pays,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   SUM(fv.quantite) AS vehicules_vendus,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total
            FROM Fact_Ventes fv
            JOIN Dim_Commercial c ON fv.id_commercial = c.id_commercial
            GROUP BY c.id_commercial
            ORDER BY nb_commandes DESC
            LIMIT ?
        """, limit);
    }

    public List<Map<String, Object>> performancesCommerciaux() {
        return jdbcTemplate.queryForList("""
            SELECT c.nom, c.prenom, c.nom_filiale, c.pays,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   ROUND(AVG(fv.montant_total), 2) AS panier_moyen,
                   SUM(fv.quantite) AS vehicules_vendus,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total
            FROM Fact_Ventes fv
            JOIN Dim_Commercial c ON fv.id_commercial = c.id_commercial
            GROUP BY c.id_commercial
            ORDER BY ca_total DESC
        """);
    }

    public List<Map<String, Object>> evolutionMensuelle() {
        return jdbcTemplate.queryForList("""
            SELECT DATE_FORMAT(t.date_complete, '%Y-%m') AS mois_annee,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   SUM(fv.quantite) AS nb_vehicules
            FROM Fact_Ventes fv
            JOIN Dim_Temps t ON fv.date_complete = t.date_complete
            GROUP BY mois_annee
            ORDER BY mois_annee ASC
        """);
    }

    public List<Map<String, Object>> caParFiliale() {
        return jdbcTemplate.queryForList("""
            SELECT c.nom_filiale, c.ville, c.pays,
                   COUNT(DISTINCT fv.id_commande) AS nb_commandes,
                   ROUND(SUM(fv.montant_total), 2) AS ca_total,
                   ROUND(AVG(fv.montant_total), 2) AS panier_moyen
            FROM Fact_Ventes fv
            JOIN Dim_Commercial c ON fv.id_commercial = c.id_commercial
            GROUP BY c.nom_filiale, c.ville, c.pays
            ORDER BY ca_total DESC
        """);
    }

    public List<Map<String, Object>> vueEnsemble() {
        return jdbcTemplate.queryForList("""
            SELECT
                (SELECT ROUND(SUM(montant_total), 2) FROM Fact_Ventes) AS ca_total,
                (SELECT COUNT(DISTINCT id_commande) FROM Fact_Ventes) AS nb_commandes,
                (SELECT SUM(quantite) FROM Fact_Ventes) AS nb_vehicules,
                (SELECT ROUND(AVG(montant_total), 2) FROM Fact_Ventes) AS panier_moyen,
                (SELECT COUNT(*) FROM Dim_Commercial) AS nb_commerciaux,
                (SELECT COUNT(*) FROM Dim_Vehicule) AS nb_vehicules_catalogue
        """);
    }
}
