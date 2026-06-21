import mysql.connector
import pandas as pd
import os

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Ngone1993",
    "database": "MacroBus_Production",
}

TABLES = [
    "Territoires", "Filiales", "Commerciaux",
    "Categories_Vehicule", "Vehicules", "Commandes", "Lignes_Commande",
    "Dim_Temps", "Dim_Vehicule", "Dim_Commercial", "Dim_Commande", "Fact_Ventes",
    "ventes_complete", "ventes_par_commercial", "ventes_par_mois",
    "ventes_par_categorie", "ventes_par_territoire", "top_vehicules", "kpis_globaux",
]

OUTPUT = os.path.join(os.path.dirname(__file__), "MacroBus_Export.xlsx")

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
    for table in TABLES:
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            sheet_name = table[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"  OK  {table:30s} -> {len(df)} lignes")
        except Exception as e:
            print(f"  ERR {table:30s} -> {e}")

cursor.close()
conn.close()
print(f"\nFichier créé : {OUTPUT}")
