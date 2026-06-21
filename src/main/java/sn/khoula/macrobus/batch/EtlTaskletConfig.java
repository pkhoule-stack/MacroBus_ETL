package sn.khoula.macrobus.batch;

import sn.khoula.macrobus.batch.EtlTasklet;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.List;

@Configuration
public class EtlTaskletConfig {

    private final JdbcTemplate jdbcTemplate;

    public EtlTaskletConfig(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Bean
    public EtlTasklet cleanupTasklet() {
        return new EtlTasklet(jdbcTemplate, List.of(
            "SET FOREIGN_KEY_CHECKS = 0",
            "TRUNCATE TABLE Fact_Ventes",
            "TRUNCATE TABLE Dim_Temps",
            "TRUNCATE TABLE Dim_Vehicule",
            "TRUNCATE TABLE Dim_Commercial",
            "TRUNCATE TABLE Dim_Commande",
            "SET FOREIGN_KEY_CHECKS = 1"
        ));
    }

    @Bean
    public EtlTasklet dimTempsTasklet() {
        return new EtlTasklet(jdbcTemplate, """
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
            FROM Commandes c
        """);
    }

    @Bean
    public EtlTasklet dimVehiculeTasklet() {
        return new EtlTasklet(jdbcTemplate, """
            INSERT IGNORE INTO Dim_Vehicule
            SELECT
                p.id_vehicule, p.code_vehicule, p.nom_vehicule, p.prix_unitaire,
                p.id_categorie, cp.libelle_categorie
            FROM Vehicules p
            LEFT JOIN Categories_Vehicule cp ON p.id_categorie = cp.id_categorie
        """);
    }

    @Bean
    public EtlTasklet dimCommercialTasklet() {
        return new EtlTasklet(jdbcTemplate, """
            INSERT IGNORE INTO Dim_Commercial
            SELECT
                c.id_commercial, c.nom, c.prenom,
                c.id_filiale, f.nom_filiale, f.ville,
                f.id_territoire, t.nom_territoire, t.pays
            FROM Commerciaux c
            LEFT JOIN Filiales f ON c.id_filiale = f.id_filiale
            LEFT JOIN Territoires t ON f.id_territoire = t.id_territoire
        """);
    }

    @Bean
    public EtlTasklet dimCommandeTasklet() {
        return new EtlTasklet(jdbcTemplate, """
            INSERT IGNORE INTO Dim_Commande
            SELECT id_commande, numero_commande FROM Commandes
        """);
    }

    @Bean
    public EtlTasklet factVentesTasklet() {
        return new EtlTasklet(jdbcTemplate, """
            INSERT INTO Fact_Ventes (id_commande, id_vehicule, id_commercial, date_complete, quantite, prix_facture)
            SELECT
                c.id_commande, lc.id_vehicule, c.id_commercial,
                c.date_commande, lc.quantite, lc.prix_facture
            FROM Lignes_Commande lc
            JOIN Commandes c ON lc.id_commande = c.id_commande
        """);
    }
}
