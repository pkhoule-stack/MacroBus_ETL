CREATE TABLE IF NOT EXISTS Territoires (
    id_territoire INT PRIMARY KEY AUTO_INCREMENT,
    nom_territoire VARCHAR(50) NOT NULL,
    pays VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Filiales (
    id_filiale INT PRIMARY KEY AUTO_INCREMENT,
    nom_filiale VARCHAR(100) NOT NULL,
    ville VARCHAR(50) NOT NULL,
    id_territoire INT,
    FOREIGN KEY (id_territoire) REFERENCES Territoires(id_territoire)
);

CREATE TABLE IF NOT EXISTS Commerciaux (
    id_commercial INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    id_filiale INT,
    FOREIGN KEY (id_filiale) REFERENCES Filiales(id_filiale)
);

CREATE TABLE IF NOT EXISTS Categories_Vehicule (
    id_categorie INT PRIMARY KEY AUTO_INCREMENT,
    libelle_categorie VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Vehicules (
    id_vehicule INT PRIMARY KEY AUTO_INCREMENT,
    code_vehicule VARCHAR(20) NOT NULL,
    nom_vehicule VARCHAR(100) NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    id_categorie INT,
    FOREIGN KEY (id_categorie) REFERENCES Categories_Vehicule(id_categorie)
);

CREATE TABLE IF NOT EXISTS Commandes (
    id_commande INT PRIMARY KEY AUTO_INCREMENT,
    numero_commande VARCHAR(20) NOT NULL,
    date_commande DATE NOT NULL,
    id_commercial INT,
    FOREIGN KEY (id_commercial) REFERENCES Commerciaux(id_commercial)
);

CREATE TABLE IF NOT EXISTS Lignes_Commande (
    id_ligne INT PRIMARY KEY AUTO_INCREMENT,
    id_commande INT,
    id_vehicule INT,
    quantite INT NOT NULL,
    prix_facture DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_commande) REFERENCES Commandes(id_commande),
    FOREIGN KEY (id_vehicule) REFERENCES Vehicules(id_vehicule)
);
