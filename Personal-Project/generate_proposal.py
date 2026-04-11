"""
Revised Proposal PDF generator for "Displaced: 27 Years of Eviction in San Francisco"
Uses ReportLab.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import os

# ─── Output path ────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "Revised_Proposal.pdf")

# ─── Colour palette ─────────────────────────────────────────────────────────
DARK_BLUE  = colors.HexColor("#0d1b2e")
MID_BLUE   = colors.HexColor("#1a2a42")
ACCENT     = colors.HexColor("#f6ad55")
TEXT_GREY  = colors.HexColor("#333333")
LIGHT_GREY = colors.HexColor("#f5f5f5")
WIRE_BG    = colors.HexColor("#e8edf3")
WIRE_BORDER= colors.HexColor("#2a3d58")
NEW_BG     = colors.HexColor("#fff8e8")
NEW_BORDER = colors.HexColor("#f6ad55")
REV_BG     = colors.HexColor("#e8f4e8")
REV_BORDER = colors.HexColor("#4caf50")

# ─── Page setup with header/footer ──────────────────────────────────────────
def make_canvas(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, letter[1] - 0.5*inch, letter[0], 0.5*inch, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.white)
    canvas.drawString(0.75*inch, letter[1] - 0.32*inch,
                      "Displaced: 27 Years of Eviction in San Francisco")
    canvas.drawRightString(letter[0] - 0.75*inch, letter[1] - 0.32*inch,
                           "Revised Proposal · USF Data Visualization · 2026")
    # Footer
    canvas.setFillColor(TEXT_GREY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.75*inch, 0.4*inch, "Miranda Cavalie · University of San Francisco")
    canvas.drawRightString(letter[0] - 0.75*inch, 0.4*inch,
                           f"Page {doc.page}")
    canvas.line(0.75*inch, 0.55*inch, letter[0] - 0.75*inch, 0.55*inch)
    canvas.restoreState()

# ─── Wireframe flowable ──────────────────────────────────────────────────────
class WireframeBox(Flowable):
    """Renders an ASCII-art wireframe as a styled code block."""
    def __init__(self, lines, width=None, title=""):
        Flowable.__init__(self)
        self.lines  = lines
        self._width  = width or 6.5*inch
        self.title   = title
        # Monospace char: ~6pt per char at 7pt font
        self._height = (len(lines) + (1 if title else 0)) * 9.5 + 18

    def wrap(self, avail_w, avail_h):
        self.width = min(self._width, avail_w)
        return self.width, self._height

    def draw(self):
        c = self.canv
        c.setFillColor(WIRE_BG)
        c.setStrokeColor(WIRE_BORDER)
        c.setLineWidth(0.8)
        c.rect(0, 0, self.width, self._height, fill=1, stroke=1)
        y = self._height - 12
        if self.title:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(DARK_BLUE)
            c.drawString(8, y, self.title)
            y -= 10
            c.setStrokeColor(WIRE_BORDER)
            c.line(4, y+2, self.width - 4, y+2)
            y -= 4
        c.setFont("Courier", 6.8)
        c.setFillColor(colors.HexColor("#1a2a42"))
        for line in self.lines:
            c.drawString(8, y, line)
            y -= 9.5

# ─── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    """Quick ParagraphStyle factory."""
    return ParagraphStyle(name, **kw)

H1 = S("H1", fontSize=20, leading=26, textColor=DARK_BLUE,
        fontName="Helvetica-Bold", spaceAfter=6)
H2 = S("H2", fontSize=14, leading=18, textColor=DARK_BLUE,
        fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=6,
        borderPad=4)
H3 = S("H3", fontSize=11, leading=15, textColor=MID_BLUE,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
BODY = S("BODY", fontSize=10.5, leading=15, textColor=TEXT_GREY,
         fontName="Helvetica", spaceAfter=6, alignment=TA_JUSTIFY)
BODY_L = S("BODY_L", fontSize=10.5, leading=15, textColor=TEXT_GREY,
           fontName="Helvetica", spaceAfter=4, alignment=TA_LEFT)
BULLET = S("BULLET", fontSize=10.5, leading=14, textColor=TEXT_GREY,
           fontName="Helvetica", leftIndent=18, spaceAfter=3,
           bulletIndent=6)
SMALL = S("SMALL", fontSize=9, leading=12, textColor=colors.HexColor("#666666"),
          fontName="Helvetica")
TAG_NEW = S("TAG_NEW", fontSize=9, leading=11, textColor=colors.HexColor("#7a4f00"),
            fontName="Helvetica-BoldOblique", backColor=NEW_BG, borderColor=NEW_BORDER,
            borderWidth=0.5, borderPad=3, spaceAfter=2)
TAG_REV = S("TAG_REV", fontSize=9, leading=11, textColor=colors.HexColor("#1a5c1a"),
            fontName="Helvetica-BoldOblique", backColor=REV_BG, borderColor=REV_BORDER,
            borderWidth=0.5, borderPad=3, spaceAfter=2)
CAPTION = S("CAPTION", fontSize=9, leading=12, textColor=colors.HexColor("#555555"),
            fontName="Helvetica-Oblique", spaceAfter=8, alignment=TA_CENTER)
MONO = S("MONO", fontSize=8, leading=11, textColor=DARK_BLUE,
         fontName="Courier")

def new_tag(text="[NEW]"):
    return Paragraph(f"<b>{text}</b>", TAG_NEW)

def rev_tag(text="[REVISED]"):
    return Paragraph(f"<b>{text}</b>", TAG_REV)

def h1(text): return Paragraph(text, H1)
def h2(text): return Paragraph(text, H2)
def h3(text): return Paragraph(text, H3)
def body(text): return Paragraph(text, BODY)
def bodyL(text): return Paragraph(text, BODY_L)
def bullet(text): return Paragraph(f"• {text}", BULLET)
def sp(n=6): return Spacer(1, n)
def hr(): return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dde3ec"),
                              spaceAfter=8, spaceBefore=4)

# ─── Table helpers ────────────────────────────────────────────────────────────
def make_table(data, col_widths=None, header_bg=DARK_BLUE, stripe=True):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    n = len(data)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, 0), 9),
        ("FONTNAME",   (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",   (0, 1), (-1, -1), 9),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]
    if stripe:
        for i in range(2, n, 2):
            style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GREY))
    t.setStyle(TableStyle(style))
    return t

# ─── Cover page ──────────────────────────────────────────────────────────────
def cover_page():
    elems = []
    elems.append(sp(40))

    title_style = S("cover_title", fontSize=28, leading=36,
                    textColor=DARK_BLUE, fontName="Helvetica-Bold",
                    alignment=TA_CENTER)
    sub_style   = S("cover_sub", fontSize=14, leading=20,
                    textColor=colors.HexColor("#1a2a42"), fontName="Helvetica",
                    alignment=TA_CENTER, spaceBefore=4, spaceAfter=2)
    meta_style  = S("cover_meta", fontSize=10, leading=16,
                    textColor=colors.HexColor("#555555"), fontName="Helvetica",
                    alignment=TA_CENTER, spaceBefore=4)

    elems.append(Paragraph("REVISED PROPOSAL", S("rl", fontSize=11, leading=14,
        fontName="Helvetica-BoldOblique",
        textColor=ACCENT, alignment=TA_CENTER, spaceAfter=10)))
    elems.append(Paragraph("Displaced", title_style))
    elems.append(Paragraph("27 Years of Eviction in San Francisco", sub_style))
    elems.append(sp(20))

    # Decorative rule
    elems.append(HRFlowable(width="60%", thickness=2, color=ACCENT,
                             hAlign="CENTER", spaceBefore=10, spaceAfter=20))

    meta_lines = [
        ("Course",   "USF Data Visualization · Spring 2026"),
        ("Student",  "Miranda Cavalie"),
        ("Website",  "https://mirandacavalie.github.io/data-vis/Personal-Project/"),
        ("Data",     "SF Rent Board Eviction Notices via DataSF"),
        ("Revised",  "April 10, 2026"),
    ]
    table_data = [[Paragraph(k, S("mk", fontSize=10, fontName="Helvetica-Bold",
                                   textColor=DARK_BLUE)),
                   Paragraph(v, S("mv", fontSize=10, fontName="Helvetica",
                                   textColor=TEXT_GREY))]
                  for k, v in meta_lines]
    mt = Table(table_data, colWidths=[1.3*inch, 4.5*inch], hAlign="CENTER")
    mt.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.4, colors.HexColor("#dddddd")),
    ]))
    elems.append(mt)
    elems.append(sp(30))

    abstract_style = S("abs", fontSize=10, leading=15, textColor=TEXT_GREY,
                       fontName="Helvetica", alignment=TA_JUSTIFY,
                       backColor=LIGHT_GREY, borderPad=10,
                       leftIndent=20, rightIndent=20)
    elems.append(Paragraph(
        "<b>Abstract.</b>  San Francisco's eviction crisis has reshaped entire "
        "neighborhoods over the past three decades. This project builds an interactive "
        "data visualization — <i>Displaced</i> — combining a scrollytelling narrative "
        "with an exploration dashboard to reveal geographic, temporal, and causal "
        "patterns in 48,000+ eviction notices filed between 1997 and 2026. "
        "The visualization uses four distinct chart types built in D3.js v7: a "
        "choropleth map, a line chart, a stacked area chart, and a horizontal bar chart.",
        abstract_style))
    elems.append(PageBreak())
    return elems

# ─── Changes Summary (NEW section at top) ────────────────────────────────────
def changes_summary():
    elems = []
    elems.append(new_tag("[NEW] CHANGES SUMMARY"))
    elems.append(h2("Changes Made in Response to Professor Feedback"))
    elems.append(body(
        "The following changes were made to address the two main items of feedback: "
        "(1) the visualization design was not clear enough and lacked detailed mockups, "
        "and (2) it was not explicitly stated that the project includes at least four "
        "distinct visualizations."))
    elems.append(sp(6))

    changes = [
        ["Change", "Section Affected", "Feedback Addressed"],
        ["[ADDED] Related Work section with 7 academic and practitioner references",
         "New Section 4", "Completeness"],
        ["[ADDED] GitHub Pages website link in Basic Information",
         "Section 1", "Website requirement"],
        ["[EXPANDED] Visualization Design: detailed ASCII wireframe layouts for all\n"
         "four designs (A, B, C, Final) showing exact page structure and dimensions",
         "Section 7 (was Section 6)", "Design clarity"],
        ["[ADDED] Explicit numbered list of 4 distinct visualization types with D3\n"
         "functions, data shown, and objectives addressed",
         "Section 7", "4 visualizations requirement"],
        ["[ADDED] Visual Encoding Justification table",
         "Section 7", "Design clarity"],
        ["[EXPANDED] Each design alternative now includes layout dimensions,\n"
         "interaction descriptions, and component details",
         "Section 7", "Design clarity"],
    ]
    elems.append(make_table(changes,
                            col_widths=[3.2*inch, 1.8*inch, 1.5*inch],
                            header_bg=DARK_BLUE))
    elems.append(sp(10))
    return elems

# ─── Section 1: Basic Information ─────────────────────────────────────────────
def basic_information():
    elems = []
    elems.append(h2("1 · Basic Information"))
    info = [
        ["Project Title", "Displaced: 27 Years of Eviction in San Francisco"],
        ["Student", "Miranda Cavalie"],
        ["Course", "Data Visualization · University of San Francisco · Spring 2026"],
        ["Data Source", "SF Rent Board Eviction Notices via DataSF (open data portal)"],
        ["Website [REVISED]",
         "https://mirandacavalie.github.io/data-vis/Personal-Project/"],
        ["Repository", "https://github.com/MirandaCavalie/data-vis"],
        ["Tools", "D3.js v7, Python (pandas, geopandas), Scrollama, HTML/CSS/JS"],
    ]
    table_data = [
        [Paragraph(k, S("ik", fontSize=9.5, fontName="Helvetica-Bold",
                        textColor=DARK_BLUE)),
         Paragraph(v, S("iv", fontSize=9.5, fontName="Helvetica",
                        textColor=TEXT_GREY))]
        for k, v in info
    ]
    t = Table(table_data, colWidths=[1.5*inch, 5.0*inch])
    t.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.4, colors.HexColor("#dddddd")),
        ("BACKGROUND",    (0, 4), (-1, 4), NEW_BG),
    ]))
    elems.append(t)
    elems.append(sp(6))
    return elems

# ─── Section 2: Background and Motivation ─────────────────────────────────────
def background_motivation():
    elems = []
    elems.append(h2("2 · Background and Motivation"))
    elems.append(body(
        "San Francisco is one of the most expensive housing markets in the United States. "
        "Since the dot-com boom of the late 1990s, the city has experienced successive "
        "waves of displacement driven by technology industry growth, speculative real "
        "estate investment, and shifts in tenant protection policy. The SF Rent Board "
        "has collected eviction notice data since 1997, creating one of the most "
        "comprehensive longitudinal records of housing displacement in any major "
        "American city."))
    elems.append(body(
        "Despite the availability of this data, most people — including long-term "
        "residents, policymakers, and advocates — lack accessible tools to understand "
        "<i>patterns</i> in the data: which neighborhoods were hardest hit in which "
        "eras, whether certain eviction types cluster in time, and how the current "
        "situation compares to historical peaks. Existing visualizations from advocacy "
        "groups (e.g., the Anti-Eviction Mapping Project) present static point maps "
        "that are difficult to interpret temporally."))
    elems.append(body(
        "This project addresses that gap by combining a guided scrollytelling narrative "
        "— structured around five historical eras — with a freely explorable "
        "cross-filtered dashboard. The goal is to give users both a curated "
        "<i>story</i> and the tools for their own <i>inquiry</i>."))
    return elems

# ─── Section 3: Project Objectives ───────────────────────────────────────────
def project_objectives():
    elems = []
    elems.append(h2("3 · Project Objectives"))
    objectives = [
        ("Objective 1", "Temporal Patterns",
         "Enable users to identify how total eviction volume changed across "
         "27 years, including spikes during the dot-com era (1999–2001), the "
         "tech surge (2013–2015), and the COVID eviction moratorium (2020–2022)."),
        ("Objective 2", "Geographic Distribution",
         "Reveal which SF neighborhoods experienced the most evictions in each "
         "era, and how displacement pressure shifted across the city over time."),
        ("Objective 3", "Causal Composition",
         "Show how the mix of eviction reasons (no-fault, breach of lease, "
         "owner move-in, nuisance, etc.) changed across eras and neighborhoods."),
        ("Objective 4", "Accessible Exploration",
         "Provide an intuitive, cross-filtered interface that allows users with "
         "no data background to explore the dataset by year range and neighborhood "
         "without feeling overwhelmed."),
    ]
    for num, title, desc in objectives:
        elems.append(h3(f"{num}: {title}"))
        elems.append(body(desc))
    return elems

# ─── Section 4: Related Work (NEW) ───────────────────────────────────────────
def related_work():
    elems = []
    elems.append(new_tag("[NEW] SECTION"))
    elems.append(h2("4 · Related Work"))
    elems.append(body(
        "This section surveys existing tools, academic papers, and technical "
        "references that directly informed the design and implementation choices "
        "for <i>Displaced</i>."))
    elems.append(sp(4))

    refs = [
        (
            "[1] Anti-Eviction Mapping Project — SF Evictions Map",
            "https://antievictionmap.com/sf-evictions",
            "The Anti-Eviction Mapping Project (AEMP) is a data visualization "
            "collective that maps all SF evictions from 1997 onward, categorized "
            "by eviction type, using the same SF Rent Board dataset that this "
            "project uses. Their interactive point maps allow users to filter by "
            "eviction type and view individual eviction records. "
            "<i>Displaced</i> extends this work by adding a temporal narrative "
            "through scrollytelling and a cross-filtered dashboard that enables "
            "neighborhood-level comparison across eras — capabilities that AEMP's "
            "static point maps do not offer."
        ),
        (
            '[2] McElroy, E. & Szeto, A. (2017). \u201cThe Anti-Eviction Mapping '
            'Project: Counter Mapping and Oral History toward Bay Area Housing '
            'Justice.\u201d Annals of the American Association of Geographers, 108(2), '
            '380\u2013389.',
            "",
            "This academic paper situates the AEMP's cartographic work within the "
            "tradition of counter-cartography — using maps as tools of advocacy "
            "rather than neutral description. The authors argue that visualizing "
            "displacement data at neighborhood granularity can make structural "
            "inequality legible to both affected communities and policymakers. "
            "This framing directly grounds <i>Displaced</i> in the literature "
            "connecting data visualization to housing justice advocacy."
        ),
        (
            "[3] Urban Displacement Project, UC Berkeley",
            "https://www.urbandisplacement.org/",
            "The Urban Displacement Project (UDP) is a research initiative that "
            "maps gentrification and displacement risk across U.S. cities using "
            "choropleth maps with sequential color scales at census-tract and "
            "neighborhood levels. Their methodology for encoding displacement "
            "intensity using a single sequential hue (rather than a diverging "
            "scale) informed my color choice: sequential blues encode "
            "'more evictions = darker' in a way that follows cartographic "
            "convention and is intuitive without prior explanation."
        ),
        (
            '[4] Vallandingham, J. \u201cSo You Want to Build A Scroller.\u201d',
            "https://vallandingham.me/scroller.html",
            "This foundational D3 scrollytelling tutorial introduces the core "
            "pattern of scroll-position-triggered visualization state changes — "
            "using IntersectionObserver or scroll events to trigger transitions "
            "in a sticky SVG as the user scrolls through narrative text. "
            "The architecture of Part 1 (scrollytelling) in <i>Displaced</i> "
            "directly follows the sticky-left / scrolling-right layout pattern "
            "described in this reference."
        ),
        (
            '[5] The Pudding. \u201cHow to implement scrollytelling with six different '
            'libraries.\u201d',
            "https://pudding.cool/process/how-to-implement-scrollytelling/",
            "This comparative analysis evaluates six scrollytelling libraries — "
            "including Scrollama, Waypoints, and custom IntersectionObserver "
            "implementations — across dimensions of ease of use, flexibility, "
            "and browser compatibility. Based on this evaluation, I chose "
            "Scrollama.js for <i>Displaced</i> because of its clean API, "
            "active maintenance, and native support for the sticky-element "
            "pattern I require."
        ),
        (
            '[6] Roberts, J.C. (2011). \u201cThe Five Design-Sheet (FdS) Approach '
            'for Sketching Information Visualization Designs.\u201d Eurographics 2011 '
            'Education Papers, pp. 27\u201341.',
            "",
            "The FdS methodology provides a structured process for exploring "
            "design alternatives before committing to implementation: Sheet 1 "
            "brainstorms many possible encodings; Sheets 2–4 develop three "
            "distinct alternatives in detail; Sheet 5 integrates the best "
            "elements into a final design. I applied this methodology to generate "
            "the three alternative designs (A: Scrollytelling, B: Dashboard, "
            "C: Neighborhood Stories) documented in Section 7 of this proposal."
        ),
        (
            '[7] Shneiderman, B. (1996). \u201cThe Eyes Have It: A Task by Data Type '
            'Taxonomy for Information Visualizations.\u201d IEEE Symposium on Visual '
            'Languages, pp. 336\u2013343.',
            "",
            'Shneiderman introduced the \u201coverview first, zoom and filter, then '
            'details on demand\u201d interaction mantra that remains the gold standard '
            "for information visualization design. The final design of "
            "<i>Displaced</i> explicitly follows this structure: the scrollytelling "
            "narrative provides the overview (5 eras, curated story), the "
            "cross-filtered dashboard enables zoom and filter (year brush, "
            "neighborhood click), and the detail panel provides details on demand "
            "(mini chart, ranked bar, neighborhood statistics)."
        ),
    ]

    for title, url, desc in refs:
        elems.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", S("rh", fontSize=10, fontName="Helvetica-Bold",
                                           textColor=DARK_BLUE, spaceBefore=8)),
            *([ Paragraph(f'<font color="#4a7aaa"><i>{url}</i></font>',
                          S("ru", fontSize=9, fontName="Helvetica-Oblique",
                            textColor=colors.HexColor("#4a7aaa"), spaceAfter=2)) ]
               if url else []),
            Paragraph(desc, S("rd", fontSize=10, leading=14.5, textColor=TEXT_GREY,
                               fontName="Helvetica", alignment=TA_JUSTIFY,
                               spaceAfter=6, leftIndent=12)),
        ]))
    return elems

# ─── Section 5: Data ──────────────────────────────────────────────────────────
def data_section():
    elems = []
    elems.append(h2("5 · Data"))
    elems.append(h3("Primary Dataset"))
    elems.append(body(
        "<b>SF Rent Board Eviction Notices</b> — Published by the City and County "
        "of San Francisco via DataSF (data.sfgov.org). The dataset contains one row "
        "per eviction notice filed with the SF Rent Board from January 1997 to the "
        "present (updated monthly). As of the project start date, the dataset "
        "contains approximately 48,000+ records."))
    elems.append(sp(4))

    fields = [
        ["Field", "Type", "Description", "Used In"],
        ["address", "String", "Street address of evicted unit", "Geocoding (optional)"],
        ["city", "String", "Always 'San Francisco'", "Filter/validation"],
        ["state", "String", "Always 'CA'", "Filter/validation"],
        ["zip", "String", "5-digit ZIP code", "Backup geo grouping"],
        ["file_date", "Date", "Date notice filed with Rent Board", "Temporal axis (all charts)"],
        ["non_payment", "Boolean (0/1)", "Eviction for non-payment of rent", "Stacked area chart"],
        ["breach", "Boolean", "Breach of rental agreement", "Stacked area chart"],
        ["nuisance", "Boolean", "Nuisance behavior", "Stacked area chart"],
        ["illegal_use", "Boolean", "Illegal use of unit", "Stacked area chart"],
        ["failure_to_sign", "Boolean", "Failure to sign new lease", "Stacked area chart"],
        ["access_denial", "Boolean", "Denial of access to unit", "Stacked area chart"],
        ["owner_move_in", "Boolean", "Owner or relative move-in (no-fault)", "Stacked area chart"],
        ["demolition", "Boolean", "Unit to be demolished", "Stacked area chart"],
        ["capital_improvement","Boolean","Unit needed for capital work","Stacked area chart"],
        ["ellis_act_withdrawal","Boolean","Ellis Act withdrawal (remove from market)","Stacked area chart"],
        ["condo_conversion", "Boolean", "Unit converted to condo", "Stacked area chart"],
        ["roommate_same_unit","Boolean","Roommate in owner-occupied unit","Stacked area chart"],
        ["other_cause", "Boolean", "Other stated cause", "Stacked area chart"],
        ["late_payments", "Boolean", "History of late payments", "Stacked area chart"],
        ["lead_remediation","Boolean","Lead paint remediation","Stacked area chart"],
        ["development", "Boolean", "Development/redevelopment", "Stacked area chart"],
        ["good_samaritan","Boolean","Good Samaritan ends","Stacked area chart"],
        ["neighbors",  "Boolean", "Neighbors / extended family", "Stacked area chart"],
        ["neighborhood_id","String","SF Neighborhood name (Analysis Neighborhoods)","Choropleth, bar chart"],
        ["supervisor_district","Integer","SF Supervisor District (1–11)","Optional grouping"],
        ["latitude",   "Float",   "Latitude of eviction address", "Map plotting"],
        ["longitude",  "Float",   "Longitude of eviction address", "Map plotting"],
    ]
    elems.append(make_table(fields,
                            col_widths=[1.4*inch, 0.9*inch, 2.4*inch, 1.8*inch]))
    elems.append(sp(6))
    elems.append(body(
        "<b>Geographic boundary file:</b> SF Analysis Neighborhoods GeoJSON from "
        "DataSF (data.sfgov.org/Geographic-Locations-and-Boundaries). Contains "
        "41 neighborhood polygons used to build the choropleth map."))
    return elems

# ─── Section 6: Data Processing ──────────────────────────────────────────────
def data_processing():
    elems = []
    elems.append(h2("6 · Data Processing"))
    elems.append(body(
        "All preprocessing is performed in Python using pandas and geopandas, "
        "with scripts stored in <code>data_exploration.py</code>. "
        "The cleaned outputs are saved as CSV and GeoJSON files that the "
        "D3 visualizations load directly via <code>d3.csv()</code> and "
        "<code>d3.json()</code>."))
    elems.append(sp(4))

    steps = [
        ("1. Parse and filter",
         "Load raw CSV. Parse file_date as datetime. "
         "Filter to records where file_date ≥ 1997-01-01. "
         "Drop rows missing neighborhood_id (< 0.5% of records)."),
        ("2. Year/month extraction",
         "Extract year and year-month columns from file_date for aggregation."),
        ("3. Eviction reason encoding",
         "The 20+ boolean reason columns are melted into a single 'reason' column "
         "per record (taking the first True column). Records with no True reason "
         "are labeled 'unspecified'."),
        ("4. Neighborhood aggregation",
         "Group by neighborhood_id and year to produce counts. "
         "Join to GeoJSON to create a choropleth-ready FeatureCollection."),
        ("5. Output files",
         "evictions_by_year.csv — total count per year (for line chart); "
         "evictions_by_neighborhood_year.csv — count by neighborhood × year "
         "(for choropleth + bar chart); "
         "evictions_by_reason_year.csv — count by reason × year "
         "(for stacked area chart); "
         "sf_neighborhoods_evictions.geojson — GeoJSON with pre-joined counts."),
    ]
    for step_title, step_desc in steps:
        elems.append(h3(step_title))
        elems.append(body(step_desc))
    return elems

# ─── Section 7: Visualization Design (REVISED) ───────────────────────────────
def visualization_design():
    elems = []
    elems.append(rev_tag("[REVISED] SECTION — Substantially expanded to address feedback"))
    elems.append(h2("7 · Visualization Design"))
    elems.append(body(
        "This section was substantially revised in response to professor feedback "
        "requesting clearer design specifications. Three alternative designs were "
        "explored using the Five Design-Sheet (FdS) methodology (Roberts, 2011) "
        "before converging on the final design. Each design is described below with "
        "a detailed wireframe layout of the planned webpage."))

    # ── 4 Distinct Visualizations ─────────────────────────────────────────────
    elems.append(new_tag("[NEW] SUBSECTION"))
    elems.append(h3("7.1 · Four Distinct Visualizations"))
    elems.append(body(
        "The final project will include exactly four distinct visualization types, "
        "each built using D3.js v7, each encoding different aspects of the eviction data:"))
    elems.append(sp(4))

    viz_data = [
        ["#", "Visualization", "Data Shown", "D3 Functions", "Objectives"],
        ["1", "Choropleth Map",
         "Eviction count per SF\nneighborhood, colored by\nintensity",
         "d3.geoMercator()\nd3.geoPath()\nd3.scaleSequential()\nd3.interpolateBlues",
         "1, 2"],
        ["2", "Line Chart",
         "Total eviction notices\nper year, 1997–2026",
         "d3.line()\nd3.scaleLinear()\nd3.axisBottom()\nbrush for year selection",
         "1"],
        ["3", "Stacked Area Chart",
         "Eviction reasons over time\n(composition view)",
         "d3.stack()\nd3.area()\nd3.schemeSet2\nd3.stackOrderNone()",
         "3"],
        ["4", "Horizontal Bar Chart",
         "Top neighborhoods by\neviction count (updates\non year-range filter)",
         "d3.scaleBand()\nd3.scaleLinear()\nanimated transitions\n(d3.transition())",
         "2, 4"],
    ]
    elems.append(make_table(viz_data,
                            col_widths=[0.3*inch, 1.2*inch, 1.6*inch, 1.8*inch, 0.7*inch]))
    elems.append(sp(10))

    # ── Visual Encoding Justification ─────────────────────────────────────────
    elems.append(new_tag("[NEW] SUBSECTION"))
    elems.append(h3("7.2 · Visual Encoding Justification"))
    elems.append(sp(4))

    enc_data = [
        ["Visual Encoding", "Data Attribute", "Chart(s)", "Justification"],
        ["Color saturation\n(sequential blues)",
         "Eviction count\n(quantitative)",
         "Choropleth map",
         "Darker = more evictions. Follows cartographic convention for "
         "intensity maps. Single hue avoids misleading divergence."],
        ["Geographic position",
         "Neighborhood location\n(spatial)",
         "Choropleth map",
         "Spatial position on the SF map directly encodes the most "
         "salient attribute (where evictions occur)."],
        ["Position x-axis",
         "Year 1997–2026\n(ordinal/temporal)",
         "Line chart,\nStacked area",
         "Time flows left to right — the most natural and universal "
         "convention for temporal data."],
        ["Position y-axis",
         "Count\n(quantitative)",
         "Line chart,\nStacked area,\nBar chart",
         "Vertical height encodes quantity. The most accurate perceptual "
         "encoding for continuous quantitative data (Cleveland & McGill)."],
        ["Color hue\n(categorical,\nSet2 palette)",
         "Eviction reason\n(nominal)",
         "Stacked area chart",
         "Distinct hues distinguish nominal categories. Set2 is "
         "colorblind-safe and has sufficient contrast at small sizes."],
        ["Bar length\n(horizontal)",
         "Eviction count\n(quantitative)",
         "Horizontal bar chart",
         "Length is the most accurate encoding for comparison between "
         "discrete categories (Mackinlay, 1986). Horizontal layout "
         "accommodates long neighborhood names."],
    ]
    elems.append(make_table(enc_data,
                            col_widths=[1.15*inch, 1.05*inch, 0.95*inch, 3.35*inch]))
    elems.append(sp(10))

    # ── Design A ──────────────────────────────────────────────────────────────
    elems.append(h3("7.3 · Design A — Scrollytelling Timeline"))
    elems.append(body(
        "Design A is a pure scrollytelling experience: a sticky choropleth map "
        "on the left transitions through 5 historical eras as the user scrolls "
        "through narrative chapters on the right. There is no dashboard component. "
        "This design prioritizes guided storytelling over open exploration."))
    elems.append(sp(6))

    wire_a = [
        "DESIGN A — PLANNED WEBPAGE LAYOUT",
        "─────────────────────────────────────────────────────────────",
        "HERO SECTION (100vh):",
        "┌────────────────────────────────────────────────────────┐",
        "│        Title: 'Displaced'  (centered, 4rem)            │",
        "│        Subtitle: '27 Years of Eviction in SF'          │",
        "│        ↓ Scroll indicator (animated arrow)             │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "SCROLLYTELLING SECTION (5 × ~100vh chapters):",
        "┌───────────────────────┬────────────────────────────────┐",
        "│                       │  CHAPTER TEXT (scrolls)        │",
        "│  CHOROPLETH MAP       │  Ch.1 — Introduction           │",
        "│  (sticky position,    │  Ch.2 — Dot-com Boom 1999–2001 │",
        "│   55% page width,     │  Ch.3 — Tech Surge 2013–2015   │",
        "│   500px height)       │  Ch.4 — COVID & Moratorium     │",
        "│                       │  Ch.5 — Recovery 2023+         │",
        "│  Sequential blues     │                                │",
        "│  d3.interpolateBlues  │  Each chapter: ~300px tall     │",
        "│  Year badge overlay   │  (triggers map update on enter)│",
        "│  (top-right corner)   │                                │",
        "└───────────────────────┴────────────────────────────────┘",
        "",
        "TIMELINE BAR (full width, 60px height, below map):",
        "┌────────────────────────────────────────────────────────┐",
        "│  1997────────────2001────────2015────2020──2023──2026  │",
        "│  Highlighted era segment moves as user scrolls         │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "END SECTION — Credits + link to GitHub data",
    ]
    elems.append(WireframeBox(wire_a, title="Design A Wireframe"))
    elems.append(Paragraph(
        "Figure 1: Design A wireframe. Pure scrollytelling — no user-driven exploration.",
        CAPTION))
    elems.append(body(
        "<b>Strengths:</b> Very clear guided narrative; works well on mobile; "
        "low cognitive load for casual viewers. "
        "<b>Weaknesses:</b> Users cannot explore their own questions; does not "
        "show all 4 visualization types; no cross-filtering. "
        "<b>Why not chosen as final:</b> Lacks the exploration component required "
        "by Objective 4 and does not fulfill the 4-visualization requirement on its own."))
    elems.append(sp(8))

    # ── Design B ──────────────────────────────────────────────────────────────
    elems.append(h3("7.4 · Design B — Interactive Dashboard"))
    elems.append(body(
        "Design B is a full-page dashboard with four linked views, all visible "
        "simultaneously. A brushable year-range selector on the line chart updates "
        "all other panels. Clicking a neighborhood on the map highlights it in "
        "the bar chart. No scrollytelling narrative."))
    elems.append(sp(6))

    wire_b = [
        "DESIGN B — PLANNED WEBPAGE LAYOUT",
        "─────────────────────────────────────────────────────────────",
        "PAGE HEADER (fixed, 60px):",
        "┌────────────────────────────────────────────────────────┐",
        "│  'Displaced' · Year range selector: [1997] ── [2026]  │",
        "│  Active filter badge  ·  Reset button                  │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "MAIN GRID (calc(100vh - 60px), 2×2 layout):",
        "┌────────────────────────┬───────────────────────────────┐",
        "│                        │                               │",
        "│  CHOROPLETH MAP        │  LINE CHART                   │",
        "│  (SF neighborhoods)    │  (total evictions/year)       │",
        "│  ~50% width, ~50% h    │  ~50% width, ~50% h          │",
        "│  Click → filter by     │  Brush → filter year range    │",
        "│  neighborhood          │  Highlighted eras shaded      │",
        "│                        │                               │",
        "├────────────────────────┼───────────────────────────────┤",
        "│                        │                               │",
        "│  STACKED AREA CHART    │  HORIZONTAL BAR CHART         │",
        "│  (eviction reasons     │  (top 15 neighborhoods        │",
        "│   over time)           │   by count, in filter)        │",
        "│  ~50% width, ~50% h    │  ~50% width, ~50% h          │",
        "│  Tooltip on hover      │  Animates on filter change    │",
        "│                        │  Click → select neighborhood  │",
        "└────────────────────────┴───────────────────────────────┘",
    ]
    elems.append(WireframeBox(wire_b, title="Design B Wireframe"))
    elems.append(Paragraph(
        "Figure 2: Design B wireframe. Four linked views in a single-page dashboard.",
        CAPTION))
    elems.append(body(
        "<b>Strengths:</b> Shows all 4 visualizations simultaneously; "
        "maximum exploration freedom; cross-filtering gives immediate context. "
        "<b>Weaknesses:</b> No guided narrative — users without background context "
        "may not understand the significance of what they see; no story arc. "
        "<b>Why not chosen as final:</b> Drops the narrative entirely, making it "
        "less engaging for general audiences unfamiliar with SF housing history."))
    elems.append(sp(8))

    # ── Design C ──────────────────────────────────────────────────────────────
    elems.append(h3("7.5 · Design C — Neighborhood Stories"))
    elems.append(body(
        "Design C presents six small-multiple choropleth maps, one per historical "
        "era, arranged in a grid. Clicking any neighborhood opens a detail drawer "
        "showing that neighborhood's full history. This design foregrounds geographic "
        "comparison across time."))
    elems.append(sp(6))

    wire_c = [
        "DESIGN C — PLANNED WEBPAGE LAYOUT",
        "─────────────────────────────────────────────────────────────",
        "HEADER (80px):",
        "┌────────────────────────────────────────────────────────┐",
        "│  'Displaced' · Sort by: [Total] [Change] [Peak year]   │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "SMALL MULTIPLE GRID (3×2, each map ~300×280px):",
        "┌──────────────┬──────────────┬──────────────────────────┐",
        "│  Era 1       │  Era 2       │  Era 3                   │",
        "│  1997–2001   │  2002–2008   │  2009–2015               │",
        "│  [SF map]    │  [SF map]    │  [SF map]                │",
        "│  blues scale │  blues scale │  blues scale             │",
        "├──────────────┼──────────────┼──────────────────────────┤",
        "│  Era 4       │  Era 5       │  Era 6                   │",
        "│  2016–2019   │  2020–2022   │  2023–2026               │",
        "│  [SF map]    │  [SF map]    │  [SF map]                │",
        "│  (COVID dip) │  (recovery)  │  (current)               │",
        "└──────────────┴──────────────┴──────────────────────────┘",
        "",
        "NEIGHBORHOOD DETAIL DRAWER (slides in from right on click):",
        "┌────────────────────────────────────────────────────────┐",
        "│  [Neighborhood Name]     [✕ Close]                     │",
        "│  Mini line chart: evictions/year for this neighborhood │",
        "│  Horizontal bar: reasons breakdown                     │",
        "│  Stats: total, peak year, most common reason           │",
        "└────────────────────────────────────────────────────────┘",
    ]
    elems.append(WireframeBox(wire_c, title="Design C Wireframe"))
    elems.append(Paragraph(
        "Figure 3: Design C wireframe. Six small-multiple maps + neighborhood detail drawer.",
        CAPTION))
    elems.append(body(
        "<b>Strengths:</b> Excellent for geographic comparison across eras; "
        "the detail drawer provides rich per-neighborhood context; novel visual form. "
        "<b>Weaknesses:</b> Six maps on one page can feel overwhelming; "
        "no temporal aggregation view (stacked area); hard to show reasons data. "
        "<b>Why not chosen as final:</b> Does not naturally accommodate all four "
        "visualization types and loses the narrative arc."))
    elems.append(sp(8))

    # ── Final Design ──────────────────────────────────────────────────────────
    elems.append(new_tag("[NEW] DETAILED WIREFRAME"))
    elems.append(h3("7.6 · Final Design — Scrollytelling + Dashboard"))
    elems.append(body(
        "The final design combines the best elements of Designs A and B: "
        "a scrollytelling narrative section (Part 1) provides guided context, "
        "followed by a fully interactive cross-filtered dashboard (Part 2) that "
        "enables open exploration. This follows Shneiderman's (1996) "
        '\u201coverview first, zoom and filter, details on demand\u201d mantra exactly.'))
    elems.append(sp(6))

    wire_f = [
        "FINAL DESIGN — PLANNED WEBPAGE LAYOUT",
        "─────────────────────────────────────────────────────────────",
        "PART 1 — SCROLLYTELLING  (approx. first 5 screen-heights)",
        "",
        "HERO (100vh):",
        "┌────────────────────────────────────────────────────────┐",
        "│  Background: semi-transparent SF aerial photo          │",
        "│  Title: 'Displaced'   (4rem, white, centered)          │",
        "│  Subtitle: '27 Years of Eviction in San Francisco'     │",
        "│  ↓ Scroll to begin  (animated indicator)               │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "SCROLLYTELLING (sticky map + scrolling chapters):",
        "┌─────────────────────────┬──────────────────────────────┐",
        "│                         │  CHAPTER TEXT  (scrolls)     │",
        "│  CHOROPLETH MAP         │                              │",
        "│  (sticky, left 55%,     │  Ch.1 Introduction (300px)   │",
        "│   500px h, d3.geo)      │  Ch.2 Dot-com '99-'01(300px) │",
        "│                         │  Ch.3 Tech Surge '13-'15(300)│",
        "│  Color: sequential      │  Ch.4 COVID '20-'22  (300px) │",
        "│  blues, 5 quantile      │  Ch.5 Recovery '23+ (300px)  │",
        "│  breaks                 │                              │",
        "│                         │  Each chapter triggers map   │",
        "│  Year badge top-right   │  color update + tooltip      │",
        "└─────────────────────────┴──────────────────────────────┘",
        "",
        "CONTEXT BAR (full width, 100px):",
        "┌────────────────────────────────────────────────────────┐",
        "│  Stacked area mini-chart (full width, 100px height)    │",
        "│  Reasons by year — gives color context before Part 2   │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "TRANSITION (full width, 80px):",
        "┌────────────────────────────────────────────────────────┐",
        "│  'Now explore the data yourself →'  (section break)    │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "PART 2 — EXPLORATION DASHBOARD",
        "",
        "FILTER BAR (fixed, 50px, appears when user reaches Part 2):",
        "┌────────────────────────────────────────────────────────┐",
        "│  Brush year range: [====1997════════════2026====]      │",
        "│  Selected: 1997–2026  ·  [Reset filters]              │",
        "└────────────────────────────────────────────────────────┘",
        "",
        "2×2 DASHBOARD GRID:",
        "┌─────────────────────────┬──────────────────────────────┐",
        "│  CHOROPLETH MAP  (V1)   │  LINE CHART  (V2)            │",
        "│  Click to select        │  Brushable year selector     │",
        "│  neighborhood           │  Shows era annotations       │",
        "│  ~50% w, ~350px h       │  ~50% w, ~350px h            │",
        "├─────────────────────────┼──────────────────────────────┤",
        "│  STACKED AREA  (V3)     │  NEIGHBORHOOD DETAIL (V4)    │",
        "│  Eviction reasons       │  If no nbhd selected:        │",
        "│  Tooltip: reason+year   │    Horizontal bar chart      │",
        "│  ~50% w, ~300px h       │    (top 15 neighborhoods)    │",
        "│                         │  If nbhd selected:           │",
        "│                         │    Mini line + bar + stats   │",
        "└─────────────────────────┴──────────────────────────────┘",
        "",
        "FOOTER: data source + credits + GitHub link",
    ]
    elems.append(WireframeBox(wire_f, title="Final Design Wireframe"))
    elems.append(Paragraph(
        "Figure 4: Final design wireframe. Part 1 provides guided narrative; "
        "Part 2 enables open exploration with all four visualizations.",
        CAPTION))
    elems.append(body(
        "<b>Why this design was chosen:</b> The scrollytelling narrative (Part 1) "
        "ensures that even users unfamiliar with SF housing history can follow the "
        "story. The dashboard (Part 2) satisfies the open-exploration requirement "
        "and naturally accommodates all four visualization types. The two parts "
        "share the choropleth map component, reducing implementation complexity. "
        "The year-range brush in Part 2 links the line chart, stacked area, and "
        "bar chart, creating a cohesive cross-filtered exploration experience."))
    return elems

# ─── Section 8: Must-Have Features ───────────────────────────────────────────
def must_have():
    elems = []
    elems.append(h2("8 · Must-Have Features"))
    features = [
        ("Feature 1: Choropleth Map",
         "An SVG choropleth map of SF Analysis Neighborhoods (41 polygons) "
         "colored by eviction count using a 5-step sequential blue scale. "
         "Built with d3.geoMercator() and d3.geoPath(). Responds to year-range "
         "brush by re-rendering with updated counts. Clicking a neighborhood "
         "highlights it and updates the bar chart / detail panel."),
        ("Feature 2: Scrollytelling Narrative",
         "A scroll-driven narrative using Scrollama.js that triggers transitions "
         "in the sticky choropleth map as the user scrolls through 5 historical "
         "chapters. Each chapter transition uses d3.transition() with a 600ms "
         "duration to update the map colors, add a year badge, and highlight "
         "relevant neighborhoods."),
        ("Feature 3: Cross-Filtered Dashboard",
         "A brushable year-range selector on the line chart that simultaneously "
         "updates the choropleth map, stacked area chart, and horizontal bar chart. "
         "All four charts use shared data bindings so that a single brush event "
         "propagates through all views via a central filter state object."),
        ("Feature 4: Neighborhood Detail Panel",
         "A detail panel (bottom-right quadrant of the dashboard) that shows "
         "a mini line chart, a reasons bar chart, and summary statistics for "
         "a selected neighborhood. Activated by clicking any neighborhood on the "
         "choropleth map. Defaults to a ranked bar chart of top-15 neighborhoods "
         "when no neighborhood is selected."),
    ]
    for title, desc in features:
        elems.append(h3(title))
        elems.append(body(desc))
    return elems

# ─── Section 9: Optional Features ────────────────────────────────────────────
def optional_features():
    elems = []
    elems.append(h2("9 · Optional Features"))
    elems.append(body(
        "The following features will be implemented if time allows, in priority order:"))
    optionals = [
        ("Animated Year Playback",
         "A 'Play' button that animates the choropleth map through years 1997–2026, "
         "showing how eviction geography evolved over time."),
        ("Eviction Type Filter",
         "Checkboxes to filter by eviction type (fault vs. no-fault), "
         "updating all dashboard panels."),
        ("Proportional Symbol Layer",
         "Optional toggle to show proportional circles on the choropleth map, "
         "encoding absolute count rather than density."),
        ("Export / Share",
         "A button to copy a shareable URL that encodes the current filter state "
         "(year range + selected neighborhood) as URL query parameters."),
    ]
    for title, desc in optionals:
        elems.append(h3(title))
        elems.append(body(desc))
    return elems

# ─── Section 10: Project Schedule ────────────────────────────────────────────
def project_schedule():
    elems = []
    elems.append(h2("10 · Project Schedule"))

    sched_data = [
        ["Week", "Dates", "Deliverable", "Tasks"],
        ["Week 1", "Apr 3–10",
         "Revised Proposal,\nRelated Work,\n& Website\n(Apr 10, 100 pts)",
         "Revise proposal with feedback.\nAdd Related Work (7 resources).\n"
         "Deploy GitHub Pages site.\nPush cleaned data & scripts."],
        ["Week 2", "Apr 10–17",
         "Alpha Release\n(Apr 17, 50 pts)",
         "All static visualizations complete\n(at least 2 in D3).\n"
         "Choropleth map + line chart in D3.\n"
         "Additional charts in matplotlib.\nWrite Alpha PDF report."],
        ["Week 3", "Apr 17–30",
         "Beta Release\n(Apr 30 by 2pm,\n100 pts)",
         "All interactivity working:\nscrolltelling, cross-filtering,\n"
         "brushing, detail panel.\nRecord 4-min video demo.\nSubmit mp4 + code zip."],
        ["Week 4", "Apr 30–\nMay 11",
         "Project Presentation\n(May 11, 50 pts)",
         "Incorporate beta feedback.\nPolish transitions and annotations.\n"
         "Prepare 8–10 min slides."],
        ["Week 5", "May 11–17",
         "Report Draft\n(May 17, 50 pts)",
         "Write IEEE-format report:\nintro, related work, approach,\n"
         "results, discussion, future work.\n10+ references."],
        ["Week 6", "May 17–20",
         "Final Submission\n(May 20, 150 pts)",
         "Final report PDF, slides,\ndemo video, commented code zip,\nuser manual."],
    ]
    elems.append(make_table(sched_data,
                            col_widths=[0.65*inch, 0.85*inch, 1.45*inch, 3.55*inch]))
    return elems

# ─── Assemble document ────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch,  bottomMargin=0.75*inch,
    )

    story = []
    story += cover_page()
    story += changes_summary()
    story.append(hr())
    story += basic_information()
    story.append(hr())
    story += background_motivation()
    story.append(hr())
    story += project_objectives()
    story.append(PageBreak())
    story += related_work()
    story.append(PageBreak())
    story += data_section()
    story.append(hr())
    story += data_processing()
    story.append(PageBreak())
    story += visualization_design()
    story.append(PageBreak())
    story += must_have()
    story.append(hr())
    story += optional_features()
    story.append(hr())
    story += project_schedule()

    doc.build(story, onFirstPage=make_canvas, onLaterPages=make_canvas)
    print(f"PDF written to: {OUT}")

if __name__ == "__main__":
    build_pdf()
