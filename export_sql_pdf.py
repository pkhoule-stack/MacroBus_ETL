import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.platypus.frames import Frame
from datetime import datetime

OUTPUT = os.path.join(os.path.dirname(__file__), "MacroBus_SQL_Script.pdf")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "car_logo.svg")
SQL_DIR = os.path.join(os.path.dirname(__file__), "src", "main", "resources")

# colors
NAVY = colors.HexColor("#0D233A")
MED_BLUE = colors.HexColor("#2B579A")
GRAY = colors.HexColor("#7F8C8D")
ACCENT = colors.HexColor("#D4A843")
WHITE = colors.white
LIGHT_GRAY = colors.HexColor("#F0F2F5")
SQL_BG = colors.HexColor("#F8F9FC")
LINE_COLOR = colors.HexColor("#D0D5DD")

PAGE_WIDTH, PAGE_HEIGHT = A4
ML = 22 * mm
MR = 22 * mm
MT = 28 * mm
MB = 22 * mm
AVAIL_W = PAGE_WIDTH - ML - MR

class DocWithPages(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.page_number = 0
    def afterPage(self):
        self.page_number += 1

def draw_page(canv, doc):
    canv.saveState()
    w, h = PAGE_WIDTH, PAGE_HEIGHT
    # top bar
    canv.setFillColor(NAVY)
    canv.rect(0, h - 8*mm, w, 8*mm, fill=1, stroke=0)
    try:
        from svglib.svglib import svg2rlg
        logo = svg2rlg(LOGO_PATH)
        logo.scale(0.2, 0.2)
        logo.drawOn(canv, ML - 2*mm, h - 7.5*mm)
    except:
        canv.setFont("Helvetica-Bold", 10)
        canv.setFillColor(WHITE)
        canv.drawString(ML, h - 6*mm, "MACROBUS")
    canv.setFont("Helvetica", 7)
    canv.setFillColor(colors.HexColor("#8DA3C4"))
    canv.drawString(ML + 22*mm, h - 6*mm, "Script SQL de creation de la base de donnees")
    dt = datetime.now().strftime("%d/%m/%Y %H:%M")
    canv.drawRightString(w - MR, h - 6*mm, dt)
    # bottom bar
    canv.setFillColor(LIGHT_GRAY)
    canv.rect(0, 0, w, 14*mm, fill=1, stroke=0)
    canv.setStrokeColor(MED_BLUE)
    canv.setLineWidth(2)
    canv.line(0, 14*mm, w, 14*mm)
    canv.setFont("Helvetica", 7)
    canv.setFillColor(GRAY)
    canv.drawCentredString(w/2, 5*mm, f"Page {doc.page_number}")
    canv.drawRightString(w - MR, 5*mm, "MacroBus_SQL_Script.pdf")
    canv.restoreState()

frame = Frame(ML, MB + 4*mm, AVAIL_W, PAGE_HEIGHT - MT - MB - 2*mm, id='main')
template = PageTemplate(id='main', frames=[frame], onPage=draw_page)

doc = DocWithPages(OUTPUT, pagesize=A4,
    title="MacroBus - Script SQL de Creation",
    author="MacroBus", subject="Script SQL base de donnees",
    leftMargin=ML, rightMargin=MR, topMargin=MT + 4*mm, bottomMargin=MB + 4*mm)
doc.addPageTemplates([template])
elems = []

# ----------- cover -----------
elems.append(Spacer(1, 70*mm))
try:
    from svglib.svglib import svg2rlg
    logo = svg2rlg(LOGO_PATH)
    logo.scale(0.6, 0.6)
    elems.append(logo)
    elems.append(Spacer(1, 4*mm))
except:
    pass
elems.append(Paragraph("MACROBUS", ParagraphStyle('cv1',
    fontSize=30, leading=36, textColor=NAVY, alignment=TA_CENTER, fontName='Helvetica-Bold')))
elems.append(Spacer(1, 4*mm))
elems.append(Paragraph("Script SQL de Creation de la Base de Donnees", ParagraphStyle('cv2',
    fontSize=14, leading=18, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')))
elems.append(Spacer(1, 4*mm))
elems.append(Paragraph("Schema operationnel (OLTP) & Schema analytique (OLAP / Star Schema)", ParagraphStyle('cv3',
    fontSize=10, leading=14, textColor=ACCENT, alignment=TA_CENTER, fontName='Helvetica-Oblique')))
elems.append(Spacer(1, 30*mm))
elems.append(Table([[""]], colWidths=[120*mm], rowHeights=[1]))
elems[-1].setStyle(TableStyle([("LINEBELOW", (0,0), (-1,-1), 1, ACCENT)]))
elems.append(Spacer(1, 8*mm))
info = ParagraphStyle('cvi', fontSize=9, leading=13, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')
elems.append(Paragraph(f"Genere le : {datetime.now().strftime('%d/%m/%Y a %H:%M')}", info))
elems.append(Paragraph("MacroBus - Vente de Vehicules en Afrique", info))
elems.append(PageBreak())

# ----------- SQL files -----------
sql_files = [
    ("01 - Schema Operationnel (OLTP)", os.path.join(SQL_DIR, "schema.sql")),
    ("02 - Schema Analytique (OLAP) + ETL", os.path.join(SQL_DIR, "star_schema.sql")),
    ("03 - Donnees de Test", os.path.join(SQL_DIR, "data_test.sql")),
    ("04 - Vues MySQL pour Power BI", os.path.join(os.path.dirname(__file__), "powerbi_views.sql")),
]

code_style = ParagraphStyle('code', fontSize=7, leading=9, fontName='Courier',
    textColor=colors.HexColor("#1a1a1a"), alignment=TA_LEFT, spaceAfter=2, spaceBefore=2)
title_style = ParagraphStyle('stitle', fontSize=14, leading=18, textColor=NAVY,
    fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=6)
desc_style = ParagraphStyle('desc', fontSize=9, leading=13, textColor=GRAY,
    fontName='Helvetica', spaceAfter=6, spaceBefore=2)

descriptions = {
    "01 - Schema Operationnel (OLTP)": (
        "Creation des 7 tables operationnelles (OLTP) de l'entreprise MacroBus : "
        "Territoires, Filiales, Commerciaux, Categories_Vehicule, Vehicules, "
        "Commandes et Lignes_Commande. Ces tables enregistrent les operations "
        "quotidiennes de vente de vehicules."
    ),
    "02 - Schema Analytique (OLAP) + ETL": (
        "Creation du schema en etoile (Star Schema) avec 4 dimensions "
        "(Dim_Temps, Dim_Vehicule, Dim_Commercial, Dim_Commande) et une table "
        "de faits (Fact_Ventes). Inclus le pipeline ETL qui alimente le star "
        "schema a partir des donnees operationnelles."
    ),
    "03 - Donnees de Test": (
        "Jeu de donnees de test representant les activites de MacroBus : "
        "7 territoires, 9 filiales, 16 commerciaux, 8 categories, "
        "18 vehicules, 37 commandes et 52 lignes de commande (2024-2025)."
    ),
    "04 - Vues MySQL pour Power BI": (
        "7 vues optimisees pour Power BI et les API REST : Ventes_Complete, "
        "Ventes_Par_Commercial, Ventes_Par_Mois, Ventes_Par_Categorie, "
        "Ventes_Par_Territoire, Top_Vehicules et KPIs_Globaux."
    ),
}

for section_name, file_path in sql_files:
    abs_path = file_path
    if not os.path.exists(abs_path):
        continue

    elems.append(Paragraph(section_name, title_style))
    if section_name in descriptions:
        elems.append(Paragraph(descriptions[section_name], desc_style))

    # file info
    file_size = os.path.getsize(abs_path)
    with open(abs_path, "r") as f:
        lines = f.readlines()
    line_count = len([l for l in lines if l.strip() and not l.strip().startswith("--")])

    info_data = [
        [Paragraph("Fichier", ParagraphStyle('fi1', fontSize=7, leading=9,
            textColor=GRAY, fontName='Helvetica-Bold')),
         Paragraph(os.path.basename(abs_path), ParagraphStyle('fi2', fontSize=7,
            leading=9, textColor=colors.black, fontName='Courier'))],
        [Paragraph("Taille", ParagraphStyle('fi1', fontSize=7, leading=9,
            textColor=GRAY, fontName='Helvetica-Bold')),
         Paragraph(f"{file_size:,} octets".replace(",", " "), ParagraphStyle('fi2',
            fontSize=7, leading=9, textColor=colors.black, fontName='Helvetica'))],
        [Paragraph("Lignes SQL", ParagraphStyle('fi1', fontSize=7, leading=9,
            textColor=GRAY, fontName='Helvetica-Bold')),
         Paragraph(str(line_count), ParagraphStyle('fi2', fontSize=7, leading=9,
            textColor=colors.black, fontName='Helvetica'))],
    ]
    info_table = Table(info_data, colWidths=[30*mm, 80*mm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), SQL_BG),
        ("BOX", (0,0), (-1,-1), 0.3, LINE_COLOR),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
    ]))
    elems.append(info_table)
    elems.append(Spacer(1, 4*mm))

    # SQL content line by line (each line as its own paragraph for wrapping)
    sql_paras = []
    blank_line_count = 0
    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            blank_line_count += 1
            if blank_line_count > 1:
                sql_paras.append(Paragraph("&nbsp;", ParagraphStyle('sqlblank',
                    fontSize=4, leading=4, fontName='Courier')))
            continue
        blank_line_count = 0

        if stripped.startswith("--"):
            fmt = f'<font color="#6A9955">{stripped}</font>'
        elif any(stripped.upper().startswith(kw) for kw in ["CREATE", "INSERT", "SELECT", "ALTER",
              "DROP", "TRUNCATE", "USE", "SET"]):
            fmt = f'<font color="#0000FF"><b>{stripped}</b></font>'
        elif any(kw in stripped.upper().split() for kw in ["TABLE", "VIEW", "INTO", "FROM", "JOIN",
              "LEFT", "WHERE", "GROUP", "ORDER", "SET", "VALUES", "FOREIGN", "PRIMARY",
              "KEY", "REFERENCES", "INDEX", "IF", "NOT", "EXISTS", "AND", "ON", "AS",
              "WHEN", "THEN", "ELSE", "END", "CASE", "DISTINCT", "ROUND", "SUM", "AVG",
              "COUNT", "YEAR", "MONTH", "DAY", "CEIL", "CONCAT", "DAYOFWEEK"]):
            fmt = f'<font color="#0000FF">{stripped}</font>'
        else:
            fmt = stripped.replace("<", "&lt;").replace(">", "&gt;")

        sql_paras.append(Paragraph(fmt, code_style))

    # Group all SQL in a background-color box using a table
    if sql_paras:
        # Split into chunks of ~50 lines to avoid page overflow
        chunk_size = 50
        for i in range(0, len(sql_paras), chunk_size):
            chunk = sql_paras[i:i+chunk_size]
            wrapper = Table([[p] for p in chunk], colWidths=[AVAIL_W])
            wrapper.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), SQL_BG),
                ("BOX", (0,0), (-1,-1), 0.3, LINE_COLOR),
                ("TOPPADDING", (0,0), (-1,-1), 1),
                ("BOTTOMPADDING", (0,0), (-1,-1), 1),
                ("LEFTPADDING", (0,0), (-1,-1), 5),
                ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ]))
            elems.append(wrapper)
            elems.append(Spacer(1, 3*mm))

    elems.append(PageBreak())

# ----------- build -----------
doc.build(elems)
print(f"PDF cree avec succes : {OUTPUT}")
