import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak,
    Frame, PageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import os
from datetime import datetime

EXCEL = os.path.join(os.path.dirname(__file__), "MacroBus_Export.xlsx")
OUTPUT = os.path.join(os.path.dirname(__file__), "MacroBus_Export.pdf")

xls = pd.ExcelFile(EXCEL)

# colors
NAVY = colors.HexColor("#0D233A")
DARK_BLUE = colors.HexColor("#1B3A5C")
MED_BLUE = colors.HexColor("#2B579A")
LIGHT_BLUE = colors.HexColor("#E8F0FE")
PALE_BLUE = colors.HexColor("#F4F8FC")
ACCENT = colors.HexColor("#D4A843")
WHITE = colors.white
GRAY = colors.HexColor("#7F8C8D")
LIGHT_GRAY = colors.HexColor("#F0F2F5")
DARK_GRAY = colors.HexColor("#2C3E50")
BORDER_COLOR = colors.HexColor("#D0D5DD")

PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)
ML = 20 * mm
MR = 20 * mm
MT = 28 * mm
MB = 22 * mm
AVAIL_W = PAGE_WIDTH - ML - MR

# ---------- helpers ----------
def fn(v):
    if pd.isna(v) or v == "" or v is None: return ""
    try: return f"{int(round(float(v))):,}".replace(",", " ")
    except: return str(v)

def fc(v):
    if pd.isna(v) or v == "" or v is None: return ""
    try: return f"{int(round(float(v))):,} FCFA".replace(",", " ")
    except: return str(v)

def cl(v):
    if pd.isna(v) or v is None: return ""
    return str(v).strip()

# ---------- styles ----------
def make_cell_style(fs, align=TA_CENTER, bold=False, color=colors.black):
    return ParagraphStyle(f'c_{fs}_{align}_{bold}_{id(color)}',
        fontSize=fs, leading=fs+3, fontName='Helvetica-Bold' if bold else 'Helvetica',
        textColor=color, alignment=align)

s_head = make_cell_style(9, TA_CENTER, True, WHITE)
s_num  = make_cell_style(8, TA_CENTER)
s_txt  = make_cell_style(8, TA_LEFT)
s_num7 = make_cell_style(7, TA_CENTER)
s_txt7 = make_cell_style(7, TA_LEFT)
s_bold_num = make_cell_style(9, TA_CENTER, True, DARK_BLUE)
s_bold_txt = make_cell_style(9, TA_LEFT, True, DARK_BLUE)

# ---------- page template ----------
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
        logo.scale(0.22, 0.22)
        logo.drawOn(canv, ML - 2*mm, h - 7.5*mm)
    except:
        canv.setFont("Helvetica-Bold", 10)
        canv.setFillColor(WHITE)
        canv.drawString(ML, h - 6*mm, "MACROBUS")
    canv.setFont("Helvetica", 7)
    canv.setFillColor(colors.HexColor("#8DA3C4"))
    canv.drawString(ML + 24*mm, h - 6*mm, "Rapport d'exportation des donnees")
    # date right
    dt = datetime.now().strftime("%d/%m/%Y %H:%M")
    canv.drawRightString(w - MR, h - 6*mm, dt)
    # bottom bar
    canv.setFillColor(LIGHT_GRAY)
    canv.rect(0, 0, w, 14*mm, fill=1, stroke=0)
    # bottom line accent
    canv.setStrokeColor(MED_BLUE)
    canv.setLineWidth(2)
    canv.line(0, 14*mm, w, 14*mm)
    # page number
    canv.setFont("Helvetica", 7)
    canv.setFillColor(GRAY)
    canv.drawCentredString(w/2, 5*mm, f"Page {doc.page_number}")
    canv.drawRightString(w - MR, 5*mm, "MacroBus_Export.pdf")
    canv.restoreState()

frame = Frame(ML, MB + 4*mm, AVAIL_W, PAGE_HEIGHT - MT - MB - 2*mm, id='main')
template = PageTemplate(id='main', frames=[frame], onPage=draw_page)

doc = DocWithPages(OUTPUT, pagesize=landscape(A4),
    title="MacroBus - Rapport d'Exportation",
    author="MacroBus", subject="Export base de donnees commerciale",
    leftMargin=ML, rightMargin=MR, topMargin=MT + 4*mm, bottomMargin=MB + 4*mm)
doc.addPageTemplates([template])
elems = []

# ---------- cover ----------
LOGO_PATH = os.path.join(os.path.dirname(__file__), "car_logo.svg")
elems.append(Spacer(1, 50*mm))
try:
    from reportlab.graphics import renderPDF
    from svglib.svglib import svg2rlg
    logo = svg2rlg(LOGO_PATH)
    logo.scale(0.8, 0.8)
    elems.append(logo)
except:
    try:
        from reportlab.lib.utils import ImageReader
        elems.append(Image(LOGO_PATH, width=50*mm, height=30*mm))
    except:
        pass
elems.append(Spacer(1, 6*mm))
elems.append(Paragraph("MACROBUS", ParagraphStyle('cv1',
    fontSize=34, leading=40, textColor=NAVY, alignment=TA_CENTER, fontName='Helvetica-Bold')))
elems.append(Spacer(1, 6*mm))
elems.append(Paragraph("Rapport d'Exportation des Donnees", ParagraphStyle('cv2',
    fontSize=18, leading=22, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')))
elems.append(Spacer(1, 4*mm))
elems.append(Paragraph("Base de Donnees Commerciale & Analytique", ParagraphStyle('cv3',
    fontSize=12, leading=15, textColor=ACCENT, alignment=TA_CENTER, fontName='Helvetica-Oblique')))
elems.append(Spacer(1, 30*mm))
# decorative line
elems.append(Table([[""]], colWidths=[120*mm], rowHeights=[1]))
elems[-1].setStyle(TableStyle([("LINEBELOW", (0,0), (-1,-1), 1, ACCENT)]))
elems.append(Spacer(1, 8*mm))
info_style = ParagraphStyle('cvi', fontSize=9, leading=13, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')
elems.append(Paragraph(f"Genere le : {datetime.now().strftime('%d/%m/%Y a %H:%M')}", info_style))
elems.append(Paragraph("Source : MacroBus_Export.xlsx", info_style))
elems.append(Paragraph("MacroBus - Vente de Vehicules en Afrique", info_style))
elems.append(PageBreak())

# ---------- table builder ----------
def build_table(df, col_widths, fs=8, extra_rows=None, bold_last=False):
    header_paras = [Paragraph(cl(c), s_head) for c in df.columns]
    data = [header_paras]
    for idx, (_, row) in enumerate(df.iterrows()):
        is_last = bold_last and idx == len(df) - 1
        cells = []
        for i, v in enumerate(row):
            txt = cl(v)
            if is_last:
                style = s_bold_num if txt and any(c.isdigit() for c in txt) else s_bold_txt
            else:
                if fs == 7:
                    style = s_num7 if txt and any(c.isdigit() for c in txt) else s_txt7
                else:
                    style = s_num if txt and any(c.isdigit() for c in txt) else s_txt
            cells.append(Paragraph(txt, style))
        data.append(cells)

    if extra_rows:
        for row_data in extra_rows:
            data.append(row_data)

    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign='LEFT')
    style = [
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("GRID", (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, PALE_BLUE]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ]
    if bold_last and len(data) > 1:
        last = len(data) - 1
        style += [
            ("BACKGROUND", (0,last), (-1,last), colors.HexColor("#E8EEF7")),
            ("LINEABOVE", (0,last), (-1,last), 1, MED_BLUE),
        ]
    t.setStyle(TableStyle(style))
    return t

# ---------- KPI ----------
elems.append(Paragraph("TABLEAU DE BORD", ParagraphStyle('h1',
    fontSize=16, leading=20, textColor=NAVY, spaceBefore=4, spaceAfter=6, fontName='Helvetica-Bold')))
elems.append(Spacer(1, 3*mm))

df_kpi = pd.read_excel(EXCEL, sheet_name="kpis_globaux")
kpi_data = [
    [Paragraph("Chiffre d'Affaires Total", ParagraphStyle('kl', fontSize=7, leading=9, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')),
     Paragraph("Commandes", ParagraphStyle('kl', fontSize=7, leading=9, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')),
     Paragraph("Vehicules Vendus", ParagraphStyle('kl', fontSize=7, leading=9, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')),
     Paragraph("Panier Moyen", ParagraphStyle('kl', fontSize=7, leading=9, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')),
     Paragraph("Commerciaux", ParagraphStyle('kl', fontSize=7, leading=9, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica')),
     Paragraph("Modeles", ParagraphStyle('kl', fontSize=7, leading=9, textColor=GRAY, alignment=TA_CENTER, fontName='Helvetica'))],
]
if not df_kpi.empty:
    r = df_kpi.iloc[0]
    vals = [
        fc(r['ca_total']), fn(r['nb_commandes']), fn(r['nb_vehicules']),
        fc(r['panier_moyen']), fn(r['nb_commerciaux']), fn(r['nb_modeles'])
    ]
    kpi_data.insert(0, [Paragraph(v, ParagraphStyle('kv', fontSize=15, leading=18,
        textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold')) for v in vals])
    cw = AVAIL_W / 6
    kt = Table(kpi_data, colWidths=[cw]*6)
    kt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("BACKGROUND", (0,1), (-1,1), WHITE),
        ("BOX", (0,0), (-1,-1), 1, MED_BLUE),
        ("LINEBELOW", (0,0), (-1,0), 1, MED_BLUE),
        ("LINEABOVE", (0,1), (-1,1), 1, MED_BLUE),
        ("LINEAFTER", (0,0), (-2,-1), 0.3, BORDER_COLOR),
        ("TOPPADDING", (0,0), (-1,0), 10),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ("TOPPADDING", (0,1), (-1,1), 5),
        ("BOTTOMPADDING", (0,1), (-1,1), 7),
    ]))
    elems.append(kt)
elems.append(Spacer(1, 8*mm))

# ---------- analytics ----------
elems.append(Paragraph("ANALYSES COMMERCIALES", ParagraphStyle('h1b',
    fontSize=16, leading=20, textColor=NAVY, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold',
    borderWidth=0, borderPadding=0)))
elems.append(Spacer(1, 3*mm))

# --- by comercial ---
df = pd.read_excel(EXCEL, sheet_name="ventes_par_commercial")
if not df.empty:
    elems.append(Paragraph("Chiffre d'Affaires par Commercial", ParagraphStyle('h2',
        fontSize=12, leading=15, textColor=MED_BLUE, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold')))
    dd = df[["commercial","filiale","ville","pays","nb_commandes","nb_vehicules","ca_total","panier_moyen"]].copy()
    dd["ca_total"] = dd["ca_total"].apply(fc)
    dd["panier_moyen"] = dd["panier_moyen"].apply(fc)
    # totals row
    tot_cmd = int(df["nb_commandes"].sum())
    tot_veh = int(df["nb_vehicules"].sum())
    tot_ca = int(df["ca_total"].sum())
    avg_pm = int(df["panier_moyen"].mean())
    extra = [[Paragraph("TOTAL GENERAL", s_bold_txt),
              Paragraph("", s_bold_txt), Paragraph("", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph(fn(tot_cmd), s_bold_num), Paragraph(fn(tot_veh), s_bold_num),
              Paragraph(fc(tot_ca), s_bold_num), Paragraph(fc(avg_pm), s_bold_num)]]
    cw = [65, 70, 40, 50, 38, 38, 85, 85]
    elems.append(build_table(dd, cw, 8, extra_rows=extra, bold_last=True))
    elems.append(Spacer(1, 6*mm))

# --- by category ---
df = pd.read_excel(EXCEL, sheet_name="ventes_par_categorie")
if not df.empty:
    elems.append(Paragraph("Chiffre d'Affaires par Categorie de Vehicule", ParagraphStyle('h2b',
        fontSize=12, leading=15, textColor=MED_BLUE, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold')))
    dd = df.copy()
    dd["ca_total"] = dd["ca_total"].apply(fc)
    tot_cmd = int(df["nb_commandes"].sum())
    tot_veh = int(df["nb_vehicules"].sum())
    tot_ca = int(df["ca_total"].sum())
    extra = [[Paragraph("TOTAL", s_bold_txt), Paragraph(fn(tot_cmd), s_bold_num),
              Paragraph(fn(tot_veh), s_bold_num), Paragraph(fc(tot_ca), s_bold_num)]]
    cw = [80, 70, 70, 140]
    elems.append(build_table(dd, cw, 9, extra_rows=extra, bold_last=True))
    elems.append(Spacer(1, 6*mm))

# --- by territory ---
df = pd.read_excel(EXCEL, sheet_name="ventes_par_territoire")
if not df.empty:
    elems.append(Paragraph("Chiffre d'Affaires par Territoire", ParagraphStyle('h2c',
        fontSize=12, leading=15, textColor=MED_BLUE, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold')))
    dd = df.copy()
    dd["ca_total"] = dd["ca_total"].apply(fc)
    tot_cmd = int(df["nb_commandes"].sum())
    tot_ca = int(df["ca_total"].sum())
    extra = [[Paragraph("TOTAL", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph(fn(tot_cmd), s_bold_num), Paragraph(fc(tot_ca), s_bold_num)]]
    cw = [80, 80, 70, 120]
    elems.append(build_table(dd, cw, 9, extra_rows=extra, bold_last=True))
    elems.append(Spacer(1, 6*mm))

# --- by month ---
df = pd.read_excel(EXCEL, sheet_name="ventes_par_mois")
if not df.empty:
    elems.append(Paragraph("Chiffre d'Affaires par Mois", ParagraphStyle('h2d',
        fontSize=12, leading=15, textColor=MED_BLUE, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold')))
    dd = df[["annee","mois_nom","trimestre","nb_commandes","nb_vehicules","ca_total"]].copy()
    dd["ca_total"] = dd["ca_total"].apply(fc)
    tot_cmd = int(df["nb_commandes"].sum())
    tot_veh = int(df["nb_vehicules"].sum())
    tot_ca = int(df["ca_total"].sum())
    extra = [[Paragraph("TOTAL", s_bold_txt), Paragraph("", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph(fn(tot_cmd), s_bold_num), Paragraph(fn(tot_veh), s_bold_num),
              Paragraph(fc(tot_ca), s_bold_num)]]
    cw = [35, 65, 50, 60, 60, 110]
    elems.append(build_table(dd, cw, 9, extra_rows=extra, bold_last=True))
    elems.append(Spacer(1, 6*mm))

# --- top vehicles ---
df = pd.read_excel(EXCEL, sheet_name="top_vehicules")
if not df.empty:
    elems.append(Paragraph("Top Vehicules les Plus Vendus", ParagraphStyle('h2e',
        fontSize=12, leading=15, textColor=MED_BLUE, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold')))
    dd = df.copy()
    dd["prix_catalogue"] = dd["prix_catalogue"].apply(fc)
    dd["ca_total"] = dd["ca_total"].apply(fc)
    tot_vendus = int(df["total_vendus"].sum())
    tot_ca = int(df["ca_total"].sum())
    extra = [[Paragraph("TOTAL", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph("", s_bold_txt), Paragraph(fn(tot_vendus), s_bold_num),
              Paragraph(fc(tot_ca), s_bold_num)]]
    cw = [90, 60, 70, 55, 85]
    elems.append(build_table(dd, cw, 9, extra_rows=extra, bold_last=True))

elems.append(PageBreak())

# ---------- operational ----------
elems.append(Paragraph("DONNEES OPERATIONNELLES", ParagraphStyle('h1c',
    fontSize=16, leading=20, textColor=NAVY, spaceBefore=4, spaceAfter=6, fontName='Helvetica-Bold')))
elems.append(Spacer(1, 3*mm))

op = [
    ("Territoires", [50, 120, 100]),
    ("Filiales", [35, 120, 70, 40]),
    ("Commerciaux", [35, 65, 65, 35]),
    ("Categories_Vehicule", [45, 120]),
    ("Vehicules", [35, 55, 110, 80, 40]),
    ("Commandes", [35, 80, 75, 50]),
    ("Lignes_Commande", [35, 50, 50, 50, 75]),
]
for sn, cw in op:
    try:
        df = pd.read_excel(EXCEL, sheet_name=sn)
    except:
        continue
    if df.empty: continue
    label = sn.replace("_", " ").title()
    elems.append(Paragraph(label, ParagraphStyle('h2o',
        fontSize=11, leading=14, textColor=MED_BLUE, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold')))
    dd = df.copy()
    if "prix_unitaire" in dd.columns:
        dd["prix_unitaire"] = dd["prix_unitaire"].apply(fc)
    if "prix_facture" in dd.columns:
        dd["prix_facture"] = dd["prix_facture"].apply(fc)
    elems.append(build_table(dd, cw, 8))
    elems.append(Spacer(1, 4*mm))

elems.append(PageBreak())

# ---------- star schema ----------
elems.append(Paragraph("SCHEMA EN ETOILE (OLAP)", ParagraphStyle('h1d',
    fontSize=16, leading=20, textColor=NAVY, spaceBefore=4, spaceAfter=6, fontName='Helvetica-Bold')))
elems.append(Spacer(1, 3*mm))

star = [
    ("Dim_Temps", [60, 35, 30, 65, 40, 30, 40, 65]),
    ("Dim_Vehicule", [35, 55, 85, 70, 40, 80]),
    ("Dim_Commercial", [35, 50, 50, 35, 70, 50, 40, 65, 55]),
    ("Dim_Commande", [45, 90]),
    ("Fact_Ventes", [30, 45, 45, 45, 60, 40, 55, 55]),
]
for sn, cw in star:
    df = pd.read_excel(EXCEL, sheet_name=sn)
    if df.empty: continue
    label = sn.replace("_", " ").title()
    elems.append(Paragraph(label, ParagraphStyle('h2s',
        fontSize=11, leading=14, textColor=MED_BLUE, spaceBefore=6, spaceAfter=4, fontName='Helvetica-Bold')))
    dd = df.copy()
    for col in ["prix_unitaire","prix_facture","montant_total"]:
        if col in dd.columns:
            dd[col] = dd[col].apply(fc)
    elems.append(build_table(dd, cw, 8))
    elems.append(Spacer(1, 4*mm))

elems.append(PageBreak())

# ---------- detail ventes ----------
elems.append(Paragraph("DETAIL COMPLET DES VENTES", ParagraphStyle('h1e',
    fontSize=16, leading=20, textColor=NAVY, spaceBefore=4, spaceAfter=6, fontName='Helvetica-Bold')))
elems.append(Spacer(1, 3*mm))

df = pd.read_excel(EXCEL, sheet_name="ventes_complete")
if not df.empty:
    cols = ["numero_commande","date_complete","commercial_nom_complet",
            "filiale","territoire","pays","nom_vehicule",
            "categorie","quantite","prix_facture","montant_total"]
    dd = df[cols].copy()
    dd["prix_facture"] = dd["prix_facture"].apply(fc)
    dd["montant_total"] = dd["montant_total"].apply(fc)
    labels = ["N Commande","Date","Commercial","Filiale","Territoire",
              "Pays","Vehicule","Categorie","Qte","Prix Unit.","Montant"]
    dd.columns = labels

    tot_q = int(df["quantite"].sum())
    tot_m = int(df["montant_total"].sum())
    extra = [[Paragraph("TOTAL GENERAL", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph("", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph("", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph("", s_bold_txt), Paragraph("", s_bold_txt),
              Paragraph(fn(tot_q), s_bold_num), Paragraph("", s_bold_txt),
              Paragraph(fc(tot_m), s_bold_num)]]
    cw = [50, 42, 60, 60, 55, 42, 70, 50, 28, 55, 70]
    elems.append(build_table(dd, cw, 7, extra_rows=extra, bold_last=True))

# ---------- build ----------
doc.build(elems)
print(f"PDF cree avec succes : {OUTPUT}")
