# MACROBUS — Entrepôt de Données pour l'Analyse des Ventes de Véhicules

## 1. Contexte et Objectifs

**MacroBus** est une entreprise de vente de véhicules implantée dans plusieurs pays d'Afrique.
Le PDG manquait de visibilité pour analyser les ventes et la performance des commerciaux.

**Objectif** : Ne pas gérer les opérations quotidiennes, mais centraliser et structurer
l'historique des données pour que les décideurs puissent analyser l'activité :
- **Quoi** se vend ? (produits, catégories)
- **Où** ? (territoires, filiales, pays)
- **Quand** ? (mois, trimestre, année)
- **Par qui** ? (commerciaux)

---

## 2. Architecture Générale

```
┌──────────────────────────────────────────────────────────┐
│                  Tables Opérationnelles (OLTP)            │
│  Territoires → Filiales → Commerciaux                   │
│  Categories_Vehicule → Vehicules                        │
│  Commandes → Lignes_Commande                            │
└──────────────────────┬───────────────────────────────────┘
                       │
            ┌──────────▼──────────┐
            │   Pipeline ETL       │
            │   (Spring Batch)     │
            │   6 étapes :         │
            │   Cleanup            │
            │   → Dim_Temps        │
            │   → Dim_Vehicule     │
            │   → Dim_Commercial   │
            │   → Dim_Commande     │
            │   → Fact_Ventes      │
            └──────────┬──────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│               Schéma en Étoile (OLAP)                    │
│                                                          │
│    ┌──────────────┐      ┌──────────────────┐           │
│    │  Dim_Temps   │      │  Dim_Vehicule    │           │
│    │  (date_compl)│◄────►│  (id_vehicule)   │           │
│    └──────────────┘      └──────────────────┘           │
│           ▲                       ▲                      │
│           │                       │                      │
│    ┌──────┴───────────────────────┴────────────────┐    │
│    │              Fact_Ventes                       │    │
│    │  id_vente | quantite | prix_facture            │    │
│    │  montant_total (colonne générée)               │    │
│    └──────┬───────────────────────┬────────────────┘    │
│           │                       │                      │
│           ▼                       ▼                      │
│    ┌──────────────┐      ┌──────────────────┐           │
│    │ Dim_Commercial│      │  Dim_Commande    │           │
│    │ (nom, filiale,│      │  (numero)        │           │
│    │  territoire)  │      │                  │           │
│    └──────────────┘      └──────────────────┘           │
└──────────────────────────────────────────────────────────┘
                       │
            ┌──────────▼──────────┐
            │   API REST          │
            │   (Spring Web MVC)  │
            └──────────┬──────────┘
                       │
            ┌──────────▼──────────┐
            │   Décideurs         │
            │   (Tableaux de bord)│
            └─────────────────────┘
```

---

## 3. Stack Technique

| Composant | Technologie |
|---|---|
| Langage | Java 17 |
| Framework | Spring Boot 4.1.0 |
| ORM | Spring Data JPA / Hibernate 7 |
| Batch / ETL | Spring Batch 6 |
| Base de données | MySQL 8.0.45 (InnoDB) |
| API | Spring Web MVC (REST JSON) |
| Build | Maven avec Wrapper |
| IDE | IntelliJ IDEA |

---

## 4. Base de Données

### 4.1 Tables Opérationnelles (OLTP)

Ces tables enregistrent les opérations quotidiennes de l'entreprise.

**Territoires**
| Colonne | Type | Description |
|---|---|---|
| id_territoire | INT (PK) | Identifiant |
| nom_territoire | VARCHAR(50) | Nom du territoire |
| pays | VARCHAR(50) | Pays |

**Filiales**
| Colonne | Type | Description |
|---|---|---|
| id_filiale | INT (PK) | Identifiant |
| nom_filiale | VARCHAR(100) | Nom de l'agence |
| ville | VARCHAR(50) | Ville |
| id_territoire | INT (FK) | Réf. territoire |

**Commerciaux**
| Colonne | Type | Description |
|---|---|---|
| id_commercial | INT (PK) | Identifiant |
| nom | VARCHAR(50) | Nom du vendeur |
| prenom | VARCHAR(50) | Prénom |
| id_filiale | INT (FK) | Réf. filiale |

**Categories_Vehicule**
| Colonne | Type | Description |
|---|---|---|
| id_categorie | INT (PK) | Identifiant |
| libelle_categorie | VARCHAR(50) | Libellé (SUV, Berline...) |

**Vehicules**
| Colonne | Type | Description |
|---|---|---|
| id_vehicule | INT (PK) | Identifiant |
| code_vehicule | VARCHAR(20) | Code modèle |
| nom_vehicule | VARCHAR(100) | Nom du modèle |
| prix_unitaire | DECIMAL(10,2) | Prix catalogue (FCFA) |
| id_categorie | INT (FK) | Réf. catégorie |

**Commandes**
| Colonne | Type | Description |
|---|---|---|
| id_commande | INT (PK) | Identifiant |
| numero_commande | VARCHAR(20) | Numéro de commande |
| date_commande | DATE | Date de commande |
| id_commercial | INT (FK) | Réf. commercial |

**Lignes_Commande**
| Colonne | Type | Description |
|---|---|---|
| id_ligne | INT (PK) | Identifiant |
| id_commande | INT (FK) | Réf. commande |
| id_vehicule | INT (FK) | Réf. véhicule |
| quantite | INT | Quantité commandée |
| prix_facture | DECIMAL(10,2) | Prix facturé unitaire (FCFA) |

### 4.2 Schéma en Étoile (OLAP)

**Dimensions**

**Dim_Temps**
| Colonne | Type | Description |
|---|---|---|
| date_complete | DATE (PK) | Date de la commande |
| annee | INT | Année |
| mois | INT | Mois (1-12) |
| mois_nom | VARCHAR(20) | Nom du mois en français |
| trimestre | INT | Trimestre (1-4) |
| jour | INT | Jour du mois |
| jour_semaine | INT | Jour de la semaine (1-7) |
| nom_jour | VARCHAR(20) | Nom du jour en français |

**Dim_Vehicule** (dénormalise Categories_Vehicule)
| Colonne | Type | Description |
|---|---|---|
| id_vehicule | INT (PK) | Identifiant |
| code_vehicule | VARCHAR(20) | Code modèle |
| nom_vehicule | VARCHAR(100) | Nom du modèle |
| prix_unitaire | DECIMAL(10,2) | Prix catalogue |
| id_categorie | INT | Réf. catégorie |
| libelle_categorie | VARCHAR(50) | Libellé catégorie (dénormalisé) |

**Dim_Commercial** (dénormalise Filiales + Territoires)
| Colonne | Type | Description |
|---|---|---|
| id_commercial | INT (PK) | Identifiant |
| nom | VARCHAR(50) | Nom |
| prenom | VARCHAR(50) | Prénom |
| id_filiale | INT | Réf. filiale |
| nom_filiale | VARCHAR(100) | Nom agence (dénormalisé) |
| ville | VARCHAR(50) | Ville (dénormalisé) |
| id_territoire | INT | Réf. territoire |
| nom_territoire | VARCHAR(50) | Territoire (dénormalisé) |
| pays | VARCHAR(50) | Pays (dénormalisé) |

**Dim_Commande**
| Colonne | Type | Description |
|---|---|---|
| id_commande | INT (PK) | Identifiant |
| numero_commande | VARCHAR(20) | Numéro de commande |

**Table de Faits**ription |
|---|---|---|
| id_vente | INT (PK) | Identifiant (auto) |
| id_commande | INT (FK) | → Dim_Commande |
| id_vehicule | INT (FK) | → Dim_Vehicule |
| id_commercial | INT (FK) | → Dim_Commercial |
| date_complete | DATE (FK) | → Dim_Temps |
| quantite | INT | Quantité vendue |
| prix_facture | DECIMAL(10,2) | Prix unitaire facturé |
| montant_total | DECIMAL(10,2) | Calculé : quantite × prix_facture |

### 4.3 Données de Test

| Table | Lignes | Détail |
|---|---|---|
| Territoires | 7 | Sénégal, Côte d'Ivoire, Cameroun, Kenya, Afrique du Sud, Maroc, Tunisie |
| Filiales | 9 | Dakar (×2), Abidjan, Douala, Yaoundé, Nairobi, Johannesburg, Casablanca, Tunis |
| Commerciaux | 16 | Répartis dans les 9 filiales |
| Categories_Vehicule | 8 | SUV, Berline, Camion, Bus, Utilitaire, Pick-up, Sport, Électrique |
| Vehicules | 18 | 18 modèles avec prix de 8M à 95M FCFA |
| Commandes | 37 | Sur 2024-2025 |
| Lignes_Commande | 52 | Lignes de vente |
| Fact_Ventes | 52 | Alimentée par l'ETL |

---

## 5. Pipeline ETL (Spring Batch)

### 5.1 Fonctionnement

Le pipeline Spring Batch exécute 6 étapes séquentiellement :

1. **cleanupStep** : Vide les tables du star schema (TRUNCATE)
2. **dimTempsStep** : Extrait les dates distinctes des commandes
3. **dimVehiculeStep** : Jointure Vehicules + Categories_Vehicule
4. **dimCommercialStep** : Jointure Commerciaux + Filiales + Territoires
5. **dimCommandeStep** : Copie des commandes
6. **factVentesStep** : Jointure Lignes_Commande + Commandes

Chaque étape est un `Tasklet` Spring Batch qui exécute une requête SQL via
`JdbcTemplate`. L'ordre garantit l'intégrité des clés étrangères.

### 5.2 Déclenchement

**Manuel** : `POST /api/etl/run`

**Automatique** : Tous les jours à 2h00 du matin
```java
@Scheduled(cron = "0 0 2 * * ?")
```

### 5.3 Classes Java

| Fichier | Rôle |
|---|---|
| `config/BatchConfig.java` | Configuration du job Spring Batch (6 steps) |
| `batch/EtlTasklet.java` | Tasklet générique exécutant du SQL |
| `batch/EtlTaskletConfig.java` | Définition des 6 étapes avec leurs requêtes |

---

## 6. API REST

### 6.1 Endpoints

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics/vue-ensemble` | KPIs globaux (CA, commandes, panier moyen) |
| GET | `/api/analytics/ca-par-commercial` | Chiffre d'affaires par commercial |
| GET | `/api/analytics/ca-par-categorie` | CA par catégorie de véhicule |
| GET | `/api/analytics/ca-par-territoire` | CA par pays / territoire |
| GET | `/api/analytics/ca-par-periode` | CA par mois et trimestre |
| GET | `/api/analytics/ca-par-filiale` | CA par agence |
| GET | `/api/analytics/top-vehicules?limit=N` | Top N véhicules les plus vendus |
| GET | `/api/analytics/top-commerciaux?limit=N` | Top N commerciaux (nb commandes) |
| GET | `/api/analytics/performances-commerciaux` | Classement complet des vendeurs |
| GET | `/api/analytics/evolution-mensuelle` | Évolution mensuelle du CA |
| POST | `/api/etl/run` | Déclencher l'ETL manuellement |

### 6.2 Exemple de réponse

```
GET /api/analytics/vue-ensemble
```
```json
[
  {
    "ca_total": 2134600000.0,
    "nb_commandes": 36,
    "nb_vehicules": 84,
    "panier_moyen": 41050000.0,
    "nb_commerciaux": 16,
    "nb_vehicules_catalogue": 18
  }
]
```

---

## 7. Fichiers du Projet

```
MACROBUS/
├── pom.xml                              # Dépendances Maven
├── resapi.http                          # Requêtes de test pour IntelliJ
│
├── src/main/java/sn/khoula/macrobus/
│   ├── MacrobusApplication.java         # Point d'entrée Spring Boot
│   │
│   ├── config/
│   │   └── BatchConfig.java             # Configuration Spring Batch
│   │
│   ├── batch/
│   │   ├── EtlTasklet.java              # Tasklet générique
│   │   └── EtlTaskletConfig.java        # Définition des 6 étapes ETL
│   │
│   ├── scheduler/
│   │   └── EtlScheduler.java            # Planification (2h du matin)
│   │
│   ├── service/
│   │   └── AnalyticsService.java        # Requêtes analytiques SQL
│   │
│   └── controller/
│       ├── EtlController.java           # POST /api/etl/run
│       └── AnalyticsController.java     # GET /api/analytics/*
│
└── src/main/resources/
    ├── application.properties           # Configuration DB + Batch
    ├── schema.sql                       # Création tables opérationnelles
    ├── data_test.sql                    # Données de test en FCFA
    └── star_schema.sql                  # Création star schema + ETL SQL
```

---

## 8. Guide de Démarrage

### Prérequis
- Java 17+
- MySQL 8.0+
- Maven (ou utiliser le wrapper `./mvnw`)

### Installation

```bash
# 1. Créer la base de données
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS MacroBus_Production;"

# 2. Créer les tables opérationnelles
mysql -u root -p MacroBus_Production < src/main/resources/schema.sql

# 3. Insérer les données de test
mysql -u root -p MacroBus_Production < src/main/resources/data_test.sql

# 4. Créer le star schema et charger l'ETL
mysql -u root -p MacroBus_Production < src/main/resources/star_schema.sql

# 5. Lancer l'application
./mvnw spring-boot:run

# 6. Déclencher l'ETL (ou attendre 2h du matin)
curl -X POST http://localhost:8080/api/etl/run
```

### Configuration
Éditer `src/main/resources/application.properties` :
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/MacroBus_Production?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true&characterEncoding=UTF-8
spring.datasource.username=root
spring.datasource.password=VOTRE_MOT_DE_PASSE
```

⚠️ **Sécurité** : Ne pas commiter le mot de passe. Utiliser une variable d'environnement :
```properties
spring.datasource.password=${MYSQL_PASSWORD}
```
