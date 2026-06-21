import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak,
    Frame, PageTemplate
)
from reportlab.pdfgen import canvas
from datetime import datetime

OUTPUT = os.path.join(os.path.dirname(__file__), "MacroBus_Tables.pdf")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "car_logo.svg")

NAVY = colors.HexColor("#0D233A")
MED_BLUE = colors.HexColor("#2B579A")
WHITE = colors.white
GRAY = colors.HexColor("#7F8C8D")
ACCENT = colors.HexColor("#D4A843")
LIGHT_GRAY = colors.HexColor("#F0F2F5")
PALE_BLUE = colors.HexColor("#E8F0FE")
BORDER = colors.HexColor("#D0D5DD")

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 22*mm, 22*mm, 28*mm, 22*mm
AVAIL_W = PAGE_W - ML - MR

class Doc(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.pn = 0
    def afterPage(self):
        self.pn += 1

def draw(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, PAGE_H - 8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    try:
        from svglib.svglib import svg2rlg
        logo = svg2rlg(LOGO_PATH)
        logo.scale(0.2, 0.2)
        logo.drawOn(canv, ML - 2*mm, PAGE_H - 7.5*mm)
    except:
        canv.setFont("Helvetica-Bold", 10)
        canv.setFillColor(WHITE)
        canv.drawString(ML, PAGE_H - 6*mm, "MACROBUS")
    canv.setFont("Helvetica", 7)
    canv.setFillColor(colors.HexColor("#8DA3C4"))
    canv.drawString(ML + 22*mm, PAGE_H - 6*mm, "Composants de la base de donnees")
    canv.drawRightString(PAGE_W - MR, PAGE_H - 6*mm, datetime.now().strftime("%d/%m/%Y %H:%M"))
    canv.setFillColor(LIGHT_GRAY)
    canv.rect(0, 0, PAGE_W, 14*mm, fill=1, stroke=0)
    canv.setStrokeColor(MED_BLUE)
    canv.setLineWidth(2)
    canv.line(0, 14*mm, PAGE_W, 14*mm)
    canv.setFont("Helvetica", 7)
    canv.setFillColor(GRAY)
    canv.drawCentredString(PAGE_W/2, 5*mm, f"Page {doc.pn}")
    canv.restoreState()

frame = Frame(ML, MB + 4*mm, AVAIL_W, PAGE_H - MT - MB - 2*mm, id='main')
doc = Doc(OUTPUT, pagesize=A4, title="MacroBus - Tables",
    leftMargin=ML, rightMargin=MR, topMargin=MT + 4*mm, bottomMargin=MB + 4*mm)
doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=draw)])
elems = []

s_head = ParagraphStyle('sh', fontSize=9, leading=12, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold')
s_center = ParagraphStyle('sc', fontSize=9, leading=12, textColor=colors.HexColor("#333"), alignment=TA_CENTER, fontName='Helvetica')
s_left = ParagraphStyle('sl', fontSize=9, leading=12, textColor=colors.HexColor("#333"), alignment=TA_LEFT, fontName='Helvetica')
s_bold = ParagraphStyle('sb', fontSize=9, leading=12, textColor=colors.HexColor("#333"), alignment=TA_LEFT, fontName='Helvetica-Bold')
s_h2 = ParagraphStyle('h2', fontSize=12, leading=15, textColor=NAVY, spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold')
s_h3 = ParagraphStyle('h3', fontSize=11, leading=14, textColor=MED_BLUE, spaceBefore=6, spaceAfter=3, fontName='Helvetica-Bold')
s_desc = ParagraphStyle('desc', fontSize=8, leading=11, textColor=GRAY, fontName='Helvetica', spaceAfter=4)
s_note = ParagraphStyle('sn', fontSize=8, leading=10, textColor=GRAY, fontName='Helvetica-Oblique')
s_intro = ParagraphStyle('intro', fontSize=9, leading=13, textColor=colors.HexColor("#333"), fontName='Helvetica', spaceAfter=8)

s_th = ParagraphStyle('th', fontSize=8, leading=10, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold')
s_tc = ParagraphStyle('tc', fontSize=8, leading=10, textColor=colors.HexColor("#333"), alignment=TA_CENTER, fontName='Helvetica')
s_tl = ParagraphStyle('tl', fontSize=8, leading=10, textColor=colors.HexColor("#333"), alignment=TA_LEFT, fontName='Courier')
s_tlb = ParagraphStyle('tlb', fontSize=8, leading=10, textColor=colors.HexColor("#333"), alignment=TA_LEFT, fontName='Helvetica-Bold')

# Cover
elems.append(Spacer(1, 80*mm))
try:
    from svglib.svglib import svg2rlg
    logo = svg2rlg(LOGO_PATH)
    logo.scale(0.7, 0.7)
    elems.append(logo)
    elems.append(Spacer(1, 4*mm))
except: pass
elems.append(Paragraph("MACROBUS", ParagraphStyle('cv1', fontSize=28, leading=34,
    textColor=NAVY, alignment=TA_CENTER, fontName='Helvetica-Bold')))
elems.append(Spacer(1, 4*mm))
elems.append(Paragraph("Composants de la Base de Donnees", ParagraphStyle('cv2',
    fontSize=14, leading=18, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')))
elems.append(Paragraph("Schema detaille des 12 tables", ParagraphStyle('cv3',
    fontSize=10, leading=14, textColor=ACCENT, alignment=TA_CENTER, fontName='Helvetica-Oblique')))
elems.append(Spacer(1, 30*mm))
t = Table([[""]], colWidths=[120*mm], rowHeights=[1])
t.setStyle(TableStyle([("LINEBELOW", (0,0), (-1,-1), 1, ACCENT)]))
elems.append(t)
elems.append(Spacer(1, 8*mm))
info = ParagraphStyle('cvi', fontSize=9, leading=13, textColor=GRAY, alignment=TA_CENTER)
elems.append(Paragraph(f"Genere le : {datetime.now().strftime('%d/%m/%Y a %H:%M')}", info))
elems.append(PageBreak())

# ============ OVERVIEW TABLE ============
elems.append(Paragraph("Inventaire des 12 Tables", s_h2))
elems.append(Paragraph(
    "La base de donnees MACROBUS est composee de <b>7 tables operationnelles (OLTP)</b> et "
    "de <b>5 tables analytiques (Star Schema / OLAP)</b>, soit un total de <b>12 tables</b> "
    "contenant <b>307 lignes</b> de donnees.",
    s_intro))

overview = [
    ["Table", "Lignes", "Categorie", "Description"],
    ["Territoires", "7", "OLTP", "7 pays d'implantation en Afrique"],
    ["Filiales", "9", "OLTP", "9 agences reparties dans les territoires"],
    ["Commerciaux", "16", "OLTP", "Vendeurs repartis dans les filiales"],
    ["Categories_Vehicule", "8", "OLTP", "8 categories de vehicules"],
    ["Vehicules", "18", "OLTP", "18 modeles (8M a 95M FCFA)"],
    ["Commandes", "37", "OLTP", "37 commandes clients (2024-2025)"],
    ["Lignes_Commande", "52", "OLTP", "52 lignes de vente detaillees"],
    ["Dim_Temps", "37", "Star Schema", "Dimensions temporelles"],
    ["Dim_Vehicule", "18", "Star Schema", "Vehicules + categorie denormalisee"],
    ["Dim_Commercial", "16", "Star Schema", "Commerciaux + filiale + territoire"],
    ["Dim_Commande", "37", "Star Schema", "Numeros de commande"],
    ["Fact_Ventes", "52", "Star Schema", "Faits de vente (montant calcule)"],
]

ov_data = []
for i, row in enumerate(overview):
    if i == 0:
        ov_data.append([Paragraph(c, s_head) for c in row])
    else:
        ov_data.append([
            Paragraph(row[0], s_bold),
            Paragraph(row[1], s_center),
            Paragraph(row[2], s_center),
            Paragraph(row[3], s_left),
        ])

cw_ov = [50*mm, 20*mm, 35*mm, AVAIL_W - 105*mm]
ov_table = Table(ov_data, colWidths=cw_ov, repeatRows=1, hAlign='LEFT')
ov_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("GRID", (0,0), (-1,-1), 0.4, BORDER),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, PALE_BLUE]),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("LINEABOVE", (0,8), (-1,8), 1.5, MED_BLUE),
]))
elems.append(ov_table)

elems.append(Spacer(1, 8*mm))

# Summary table
elems.append(Paragraph("Resume", s_h3))
sum_data = [
    [Paragraph("Categorie", s_head), Paragraph("Tables", s_head), Paragraph("Lignes", s_head)],
    [Paragraph("Tables operationnelles (OLTP)", ParagraphStyle('sb2', fontSize=9, leading=12, textColor=colors.HexColor("#333"), alignment=TA_LEFT, fontName='Helvetica-Bold')),
     Paragraph("7", s_center), Paragraph("147", s_center)],
    [Paragraph("Tables analytiques (Star Schema)", ParagraphStyle('sb2', fontSize=9, leading=12, textColor=colors.HexColor("#333"), alignment=TA_LEFT, fontName='Helvetica-Bold')),
     Paragraph("5", s_center), Paragraph("160", s_center)],
    [Paragraph("TOTAL", ParagraphStyle('st', fontSize=10, leading=13, textColor=WHITE, alignment=TA_LEFT, fontName='Helvetica-Bold')),
     Paragraph("12", ParagraphStyle('stc', fontSize=10, leading=13, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold')),
     Paragraph("307", ParagraphStyle('stc', fontSize=10, leading=13, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold'))],
]
cw_sum = [80*mm, 30*mm, 35*mm]
st = Table(sum_data, colWidths=cw_sum, hAlign='LEFT')
st.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("BACKGROUND", (0,-1), (-1,-1), MED_BLUE),
    ("GRID", (0,0), (-1,-1), 0.4, BORDER),
    ("ROWBACKGROUNDS", (0,1), (-1,2), [WHITE, PALE_BLUE]),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
]))
elems.append(st)

elems.append(PageBreak())

# ============ DETAILED TABLES ============
elems.append(Paragraph("Details des 12 Tables", s_h2))
elems.append(Spacer(1, 3*mm))

# Schema data for each table
table_schemas = {
    "Territoires": {
        "lignes": "7",
        "desc": "Enregistre les zones geographiques ou MacroBus est implante.",
        "colonnes": [
            ("id_territoire", "INT (PK)", "Identifiant unique du territoire"),
            ("nom_territoire", "VARCHAR(50)", "Nom du territoire (ex: Afrique de l'Ouest)"),
            ("pays", "VARCHAR(50)", "Nom du pays"),
        ]
    },
    "Filiales": {
        "lignes": "9",
        "desc": "Agences locales de MacroBus dans chaque pays.",
        "colonnes": [
            ("id_filiale", "INT (PK)", "Identifiant unique de la filiale"),
            ("nom_filiale", "VARCHAR(100)", "Nom de l'agence (ex: MacroBus Dakar Centre)"),
            ("ville", "VARCHAR(50)", "Ville de la filiale"),
            ("id_territoire", "INT (FK)", "Reference vers Territoires"),
        ]
    },
    "Commerciaux": {
        "lignes": "16",
        "desc": "Vendeurs attaches aux filiales.",
        "colonnes": [
            ("id_commercial", "INT (PK)", "Identifiant unique du commercial"),
            ("nom", "VARCHAR(50)", "Nom de famille"),
            ("prenom", "VARCHAR(50)", "Prenom"),
            ("id_filiale", "INT (FK)", "Reference vers Filiales"),
        ]
    },
    "Categories_Vehicule": {
        "lignes": "8",
        "desc": "Categories de vehicules proposees par MacroBus.",
        "colonnes": [
            ("id_categorie", "INT (PK)", "Identifiant unique de la categorie"),
            ("libelle_categorie", "VARCHAR(50)", "Libelle (SUV, Berline, Camion, Bus...)"),
        ]
    },
    "Vehicules": {
        "lignes": "18",
        "desc": "Catalogue des vehicules disponibles a la vente.",
        "colonnes": [
            ("id_vehicule", "INT (PK)", "Identifiant unique du vehicule"),
            ("code_vehicule", "VARCHAR(20)", "Code modele (ex: SUV-001)"),
            ("nom_vehicule", "VARCHAR(100)", "Nom commercial du vehicule"),
            ("prix_unitaire", "DECIMAL(10,2)", "Prix catalogue en FCFA"),
            ("id_categorie", "INT (FK)", "Reference vers Categories_Vehicule"),
        ]
    },
    "Commandes": {
        "lignes": "37",
        "desc": "En-tetes des commandes clients.",
        "colonnes": [
            ("id_commande", "INT (PK)", "Identifiant unique de la commande"),
            ("numero_commande", "VARCHAR(20)", "Numero de commande (ex: CMD-2024-001)"),
            ("date_commande", "DATE", "Date de la commande"),
            ("id_commercial", "INT (FK)", "Reference vers Commerciaux"),
        ]
    },
    "Lignes_Commande": {
        "lignes": "52",
        "desc": "Detail des articles commandes (produits, quantites, prix).",
        "colonnes": [
            ("id_ligne", "INT (PK)", "Identifiant unique de la ligne"),
            ("id_commande", "INT (FK)", "Reference vers Commandes"),
            ("id_vehicule", "INT (FK)", "Reference vers Vehicules"),
            ("quantite", "INT", "Quantite commandee"),
            ("prix_facture", "DECIMAL(10,2)", "Prix unitaire facture en FCFA"),
        ]
    },
    "Dim_Temps": {
        "lignes": "37",
        "desc": "Dimension temporelle (Star Schema). Contient les dates des commandes avec leurs attributs.",
        "colonnes": [
            ("date_complete", "DATE (PK)", "Date complete de la commande"),
            ("annee", "INT", "Annee"),
            ("mois", "INT", "Mois (1-12)"),
            ("mois_nom", "VARCHAR(20)", "Nom du mois en francais"),
            ("trimestre", "INT", "Trimestre (1-4)"),
            ("jour", "INT", "Jour du mois"),
            ("jour_semaine", "INT", "Jour de la semaine (1-7)"),
            ("nom_jour", "VARCHAR(20)", "Nom du jour en francais"),
        ]
    },
    "Dim_Vehicule": {
        "lignes": "18",
        "desc": "Dimension vehicule denormalisee. Inclut le libelle de la categorie.",
        "colonnes": [
            ("id_vehicule", "INT (PK)", "Identifiant du vehicule"),
            ("code_vehicule", "VARCHAR(20)", "Code modele"),
            ("nom_vehicule", "VARCHAR(100)", "Nom du vehicule"),
            ("prix_unitaire", "DECIMAL(10,2)", "Prix catalogue"),
            ("id_categorie", "INT", "Reference categorie"),
            ("libelle_categorie", "VARCHAR(50)", "Libelle categorie (denormalise)"),
        ]
    },
    "Dim_Commercial": {
        "lignes": "16",
        "desc": "Dimension commercial denormalisee. Inclut filiale, ville, territoire et pays.",
        "colonnes": [
            ("id_commercial", "INT (PK)", "Identifiant du commercial"),
            ("nom", "VARCHAR(50)", "Nom"),
            ("prenom", "VARCHAR(50)", "Prenom"),
            ("id_filiale", "INT", "Reference filiale"),
            ("nom_filiale", "VARCHAR(100)", "Nom de l'agence (denormalise)"),
            ("ville", "VARCHAR(50)", "Ville (denormalise)"),
            ("id_territoire", "INT", "Reference territoire"),
            ("nom_territoire", "VARCHAR(50)", "Nom territoire (denormalise)"),
            ("pays", "VARCHAR(50)", "Pays (denormalise)"),
        ]
    },
    "Dim_Commande": {
        "lignes": "37",
        "desc": "Dimension commande. Contient le numero de commande.",
        "colonnes": [
            ("id_commande", "INT (PK)", "Identifiant de la commande"),
            ("numero_commande", "VARCHAR(20)", "Numero de commande"),
        ]
    },
    "Fact_Ventes": {
        "lignes": "52",
        "desc": "Table de faits centrale. Chaque ligne represente une vente avec ses dimensions.",
        "colonnes": [
            ("id_vente", "INT (PK)", "Identifiant unique de la vente (auto-increment)"),
            ("id_commande", "INT (FK)", "Vers Dim_Commande"),
            ("id_vehicule", "INT (FK)", "Vers Dim_Vehicule"),
            ("id_commercial", "INT (FK)", "Vers Dim_Commercial"),
            ("date_complete", "DATE (FK)", "Vers Dim_Temps"),
            ("quantite", "INT", "Quantite vendue"),
            ("prix_facture", "DECIMAL(10,2)", "Prix unitaire facture (FCFA)"),
            ("montant_total", "DECIMAL(10,2)", "= quantite x prix_facture (calcule automatiquement)"),
        ]
    },
}

for i, (tn, info) in enumerate(table_schemas.items()):
    cat = "OLTP" if tn in ["Territoires","Filiales","Commerciaux","Categories_Vehicule","Vehicules","Commandes","Lignes_Commande"] else "Star Schema"

    # Table header with name and category badge
    header_text = f"{i+1}. {tn}"
    elems.append(Paragraph(header_text, s_h3))
    elems.append(Paragraph(f"<b>Categorie :</b> {cat} | <b>Lignes :</b> {info['lignes']} | <b>Description :</b> {info['desc']}", s_desc))

    # Columns table
    col_data = [
        [Paragraph("Colonne", s_th), Paragraph("Type", s_th), Paragraph("Description", s_th)],
    ]
    for col_name, col_type, col_desc in info["colonnes"]:
        col_data.append([
            Paragraph(col_name, s_tl),
            Paragraph(col_type, s_tc),
            Paragraph(col_desc, s_tlb),
        ])

    # Highlight PK and FK with color
    col_cw = [55*mm, 45*mm, AVAIL_W - 100*mm]
    col_table = Table(col_data, colWidths=col_cw, repeatRows=1, hAlign='LEFT')
    col_style = [
        ("BACKGROUND", (0,0), (-1,0), MED_BLUE),
        ("GRID", (0,0), (-1,-1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, PALE_BLUE]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ]
    # color PK rows
    for j, (cn, ct, cd) in enumerate(info["colonnes"]):
        if "(PK)" in ct:
            col_style += [
                ("BACKGROUND", (0, j+1), (0, j+1), colors.HexColor("#FFF3CD")),
            ]
    col_table.setStyle(TableStyle(col_style))
    elems.append(col_table)
    elems.append(Spacer(1, 5*mm))

doc.build(elems)
print(f"PDF cree : {OUTPUT}")
