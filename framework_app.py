# ========================================================================
#  FRAMEWORK APP — INTERACTIVE COLLAPSIBLE DECISION TREE (DASH)
#  Prepared for scientific publication + extendable by the author.
#  *** EVERY SECTION IS EXPLAINED SO YOU CAN MODIFY IT EASILY ***
# ========================================================================

import dash
from dash import html, Input, Output, dcc
import dash_cytoscape as cyto


# ========================================================================
# PART 1 — INITIALIZE DASH APP
# ========================================================================
# ⚠️ VERY IMPORTANT for Render deployment:
#     "server = app.server" must stay exactly like this.
# ========================================================================

app = dash.Dash(__name__)
server = app.server



# ========================================================================
# PART 2 — DECISION TREE STRUCTURE (MAIN HIERARCHY)
# ========================================================================
# 🎯 THIS IS WHERE YOU MODIFY THE TREE ITSELF
#
# Left side  = parent node
# Right side = list of children nodes
#
# To add new branches:
#   tree["Your Node"] = ["Child 1", "Child 2", ...]
#
# To add new tests:
#   Add them under the branch where they belong.
#
# ⚠️ The node name MUST be unique.
# ========================================================================

tree = {
    "root": ["Exploratory Analysis"],

    "Exploratory Analysis": ["Normality Tests"],

    "Normality Tests": ["Univariate", "Multivariate"],

    # ---------------- UNIVARIATE -----------------
    "Univariate": ["Univariate Graphical", "Univariate Formal"],

    "Univariate Graphical": [
        "Q–Q Plot", 
        "Histogram", 
        "Box Plot", 
        "Dot Plot"
    ],

    "Univariate Formal": [
        "Shapiro–Wilk",
        "Anderson–Darling",
        "Kolmogorov\n–Smirnov",
        "D’Agostino Skewness",
        "Anscombe–Glynn Kurtosis"
    ],

    # ---------------- MULTIVARIATE -----------------
    "Multivariate": ["Multivariate Graphical", "Multivariate Formal"],

    "Multivariate Graphical": [
        "Gamma Plot",
        "Chi-Square Q–Q Plot",
        "Multivariate Q–Q Plot"
    ],

    "Multivariate Formal": [
        "Mardia Skewness",
        "Mardia Kurtosis",
        "Royston Test",
        "Henze–Zirkler Test"
    ],

      # ---------------- PCA / FA / PMF SECTION -----------------
    "Multivariate Dimension Reduction": ["PCA", "FA", "PMF"],

    "PCA": ["PCA Details"],
    "FA": ["FA Details"],
    "PMF": ["PMF Details"],
}



# ========================================================================
# PART 2B — DETAILS FOR INFO PANEL (TABS)
# ========================================================================
# 🎯 Each test can have:
#     - Description
#     - Formula
#     - Rules
#     - Interpretation
#     - Example
#     - Citation
#     - Image (stored inside /assets/)
#
# To ADD NEW TEST DETAILS:
#   node_details["Your Test"] = { ... }
#
# To MODIFY FORMULAS / TEXTS / RULES:
#   Edit the dictionary below.
# ========================================================================

node_details = {

    # --------------------------------------------------------------------
    # EXAMPLE 1 — SHAPIRO-WILK
    # --------------------------------------------------------------------
    "Shapiro–Wilk": {
        "description": "Best normality test for small samples (n < 50). Very sensitive to tail deviations.",
        "formula": r"W = \frac{(\sum a_i x_{(i)})^2}{\sum (x_i - \bar{x})^2}",
        "rules": [
            "Recommended for n < 50",
            "More powerful than K–S test for small samples",
            "Very sensitive to tail deviations"
        ],
        "interpretation": [
            "p < 0.05 → reject normality",
            "p ≥ 0.05 → normality not rejected"
        ],
        "example": "Example: n = 25 gives p = 0.03 → not normally distributed.",
        "citation": "Shapiro & Wilk (1965). Biometrika.",
        "image": "shapiro.png"
    },

    # --------------------------------------------------------------------
    # EXAMPLE 2 — Q-Q PLOT
    # --------------------------------------------------------------------
    "Q–Q Plot": {
        "description": "A graphical method to check if data follows a normal distribution.",
        "formula": "No formula (graphical method).",
        "rules": ["Look for deviations in tails", "S-shape → skewness"],
        "interpretation": ["Straight line → normal", "Curved → not normal"],
        "example": "Example: upward deviation in right tail → right skew.",
        "citation": "Wilk & Gnanadesikan (1968). Biometrika.",
        "image": "qqplot.png"
    },

    # --------------------------------------------------------------------
    # EXAMPLE 3 — HISTOGRAM
    # --------------------------------------------------------------------
    "Histogram": {
        "description": "Basic visual distribution check.",
        "formula": "No formula.",
        "rules": ["Bin size affects interpretation", "Used for quick inspection"],
        "interpretation": ["Bell curve → normal"],
        "example": "Example: uneven shape → skewness.",
        "citation": "Cleveland (1985). The Elements of Graphing Data.",
        "image": "histogram.png"
    },

    # --------------------------------------------------------------------
    # EXAMPLE 4 — MARDIA SKEWNESS
    # --------------------------------------------------------------------
    "Mardia Skewness": {
        "description": "Measures multivariate skewness in multivariate normality testing.",
        "formula": r"b_{1,p} = \frac{1}{n^2}\sum_{i,j}[(x_i-\bar{x})^TS^{-1}(x_j-\bar{x})]^3",
        "rules": ["Requires covariance matrix invertibility", "Sensitive to multivariate outliers"],
        "interpretation": ["Large value → violates multivariate normality"],
        "example": "Example: b₁ₚ > χ² critical value → reject normality.",
        "citation": "Mardia (1970). Biometrika.",
        "image": "mardia.png"
    },

    # ====================================================================
    # NEW: PCA / FA / PMF DETAILS
    # ====================================================================

    "PCA Details": {
        "description": "Principal Component Analysis (PCA) reduces dimensionality by maximizing variance.\n\n"
                       "When to use:\n"
                       "• You want to summarize many correlated variables\n"
                       "• You want orthogonal components\n"
                       "• You assume linear relationships\n",
        "formula": r"Z = XW \quad \text{(eigenvectors of covariance matrix)}",
        "citation": "Jolliffe (2002). Principal Component Analysis.",
        "image": "pca.png"
    },

    "FA Details": {
        "description": "Factor Analysis (FA) models latent variables that explain observed correlations.\n\n"
                       "When to use:\n"
                       "• You want to identify underlying factors\n"
                       "• Shared variance is more important than total variance",
        "formula": r"X = \Lambda F + \epsilon",
        "citation": "Fabrigar et al. (1999). Psychological Methods.",
        "image": "fa.png"
    },

    "PMF Details": {
        "description": "Positive Matrix Factorization (PMF) is widely used in environmental sciences.\n\n"
                       "When to use:\n"
                       "• Source apportionment of pollutants\n"
                       "• Chemical compositional data\n"
                       "• Non-negative constraints required",
        "formula": r"X = GF + E",
        "citation": "Paatero & Tapper (1994). Environmetrics.",
        "image": "pmf.png"
    }
}



# ========================================================================
# PART 3 — INITIAL ELEMENTS (ROOT NODE)
# ========================================================================

elements = [
    {"data": {"id": "root", "label": "Statistical\nDecision Tree"},
     "position": {"x": 300, "y": 50}}
]

expanded_nodes = set()



# ========================================================================
# PART 4 — EXPAND & COLLAPSE LOGIC
# ========================================================================
# 🎯 You do *not* need to edit this unless you change layout spacing.
#
# spacing = 170  → horizontal distance between nodes
# child_y = +130 → vertical distance between levels
#
# If your tree gets wide, increase spacing.

# ⭐ Note that you can UPDATED SPACING HERE ⭐
# spacing (horizontal) → widened from 170 → 260
# vertical spacing     → increased from 130 → 160
# ========================================================================

def toggle_node(node_id, current):
    global expanded_nodes

    # 1) COLLAPSE NODE
    if node_id in expanded_nodes:
        expanded_nodes.remove(node_id)
        children = tree.get(node_id, [])
        new_list = []
        for el in current:
            if "source" in el.get("data", {}) and el["data"]["source"] == node_id:
                continue
            if "id" in el.get("data", {}) and el["data"]["id"] in children:
                continue
            new_list.append(el)
        return new_list

    # 2) EXPAND NODE
    expanded_nodes.add(node_id)

    parent_x = parent_y = 0
    for el in current:
        if el["data"].get("id") == node_id:
            parent_x, parent_y = el["position"]["x"], el["position"]["y"]

    kids = tree.get(node_id, [])
    spacing = 260
    start_x = parent_x - (len(kids) - 1) * spacing / 2
    child_y = parent_y + 160

    new_list = current.copy()

    for i, kid in enumerate(kids):
        new_list.append({
            "data": {"id": kid, "label": kid},
            "position": {"x": start_x + i * spacing, "y": child_y}
        })
        new_list.append({"data": {"source": node_id, "target": kid}})

    return new_list



# ========================================================================
# PART 5 — THEMES (EDIT COLORS HERE)
# ========================================================================
# 🎨 To change color themes, modify LIGHT / DARK dictionaries.
# ========================================================================

LIGHT = {
    "page": "white",
    "text": "black",
    "cy_bg": "#f2f2f2",
    "node": "#f2f2f2",
    "node_text": "#900034",
    "border": "#0072B2",
    "edge": "#444"
}

DARK = {
    "page": "#2b2b2b",
    "text": "white",
    "cy_bg": "#3a3a3a",
    "node": "#3a3a3a",
    "node_text": "#FFC20A",
    "border": "#71BDFF",
    "edge": "#ddd"
}

# ========================================================================
# PART 6 — LAYOUT (PAGE STRUCTURE)
# ========================================================================

app.layout = html.Div(
    id="page-container",
    children=[

        html.H1("📊 Statistical Framework for Water Quality Assessment"),
        html.P("Click the nodes to expand/collapse and explore full statistical details.\nUse the mouse scroll wheel to zoom in/out."),

        # ---------------- THEME SWITCH ----------------
        dcc.RadioItems(
            id="theme",
            options=[
                {"label": "🌞 Light", "value": "light"},
                {"label": "🌙 Dark", "value": "dark"},
            ],
            value="light",
            inline=True
        ),

        # ---------------- INTERACTIVE TREE ----------------
        cyto.Cytoscape(
            id="cy",
            layout={"name": "preset"},
            style={"width": "100%", "height": "700px"},
            elements=elements,
            stylesheet=[]
        ),

        # ---------------- INFO PANEL ----------------
        html.Div(id="info", style={"marginTop": "25px"}),

        # ---------------- FOOTER (CONTACT + COPYRIGHT) ----------------
        html.Hr(style={"marginTop": "30px", "opacity": 0.3}),

        html.Footer(
            id="footer",
            style={
                "marginTop": "10px",
                "paddingTop": "12px",
                "paddingBottom": "12px",
                "fontSize": "13px",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "flexWrap": "wrap",
                "gap": "10px",
                "borderTop": "1px solid rgba(128,128,128,0.35)",
            },
            children=[
                html.Div([
                    html.Span("Contact: "),
                    html.A(
                        "btalsabti93@gmail.com",
                        href="mailto:btalsabti93@gmail.com",
                        style={"textDecoration": "none"}
                    ),
                    html.Span(" • "),
                    html.A(
                        "Research Gate",
                        href="https://www.researchgate.net/profile/Bedour-Alsabti",
                        target="_blank",
                        style={"textDecoration": "none"}
                    ),
                ]),

                html.Div("© 2026 Bedour Alsabti & co-authors. All rights reserved."),
            ],
        ),
    ]
)


# ========================================================================
# PART 7 — NODE CLICK CALLBACK (INFO TABS)
# ========================================================================
# 🎯 This controls what appears when a user clicks a test.
#
# To ADD a new tab:
#   Insert a dcc.Tab(...) into the list.
#
# To REMOVE a tab:
#   Delete that dcc.Tab(...) line.
#
# ========================================================================

@app.callback(
    Output("cy", "elements"),
    Output("info", "children"),
    Input("cy", "tapNodeData"),
    prevent_initial_call=True
)
def click(node):
    global elements
    if not node:
        return elements, ""

    node_id = node["id"]
    elements = toggle_node(node_id, elements)

    # If the node has no details, just return selection text
    if node_id not in node_details:
        return elements, f"You selected: {node_id}"

    d = node_details[node_id]

    # ---- MERGE sections into a single descriptive text ----
    merged_text = ""

    if "description" in d:
        merged_text += f"{d['description']}\n\n"

    if "rules" in d:
        merged_text += "Rules:\n"
        for r in d["rules"]:
            merged_text += f"• {r}\n"
        merged_text += "\n"

    if "interpretation" in d:
        merged_text += "Interpretation:\n"
        for inter in d["interpretation"]:
            merged_text += f"• {inter}\n"
        merged_text += "\n"

    if "example" in d:
        merged_text += f"Example:\n{d['example']}\n"

    # ---- Tabs ----
    tabs = dcc.Tabs([
        dcc.Tab(label="📘 Description", children=html.Pre(merged_text, style={"whiteSpace": "pre-wrap"})),

        dcc.Tab(label="∑ Formula", children=html.Pre(d.get("formula", ""), style={"whiteSpace": "pre-wrap"})),

        dcc.Tab(label="📚 Citation", children=html.P(d.get("citation", ""))),

        dcc.Tab(label="🖼 Image", children=html.Img(
            src="/assets/" + d.get("image", ""),
            style={"width": "60%", "margin": "20px"}
        ))
    ])

    return elements, tabs


# ========================================================================
# PART 8 — THEME SWITCH CALLBACK
# ========================================================================
# 🎯 Controls light/dark mode styles.
# ========================================================================

@app.callback(
    Output("cy", "stylesheet"),
    Output("cy", "style"),
    Output("page-container", "style"),
    Input("theme", "value")
)
def theme_switch(mode):

    theme = LIGHT if mode == "light" else DARK

    stylesheet = [
    {"selector": "node",
     "style": {
         "content": "data(label)",
         "background-color": theme["node"],
         "color": theme["node_text"],
         "border-color": theme["border"],
         "border-width": 2,

         # ✅ wrapping + newlines
         "white-space": "pre-wrap",
         "text-wrap": "wrap",
         "text-max-width": 160,   # 👈 IMPORTANT (tune 140–170)
         "line-height": 1.2,

         "shape": "round-rectangle",
         "text-valign": "center",
         "text-halign": "center",
         "width": 180,
         "height": 80,            # 👈 increase for 2 lines (since font-size=20)
         "font-family": "Times New Roman, Times, serif", # or "Arial, Helvetica, sans-serif"
         "font-size": "22px",
         "font-weight": "normal"
     }},
    {"selector": "edge",
     "style": {"line-color": theme["edge"], "width": 3}}
]

    cy_style = {
        "width": "100%",
        "height": "700px",
        "backgroundColor": theme["cy_bg"]
    }

    page_style = {
        "backgroundColor": theme["page"],
        "color": theme["text"],
        "minHeight": "100vh",
        "padding": "20px",
        "fontFamily": "Times New Roman, Times, serif",   # or "Arial, sans-serif" or "Arial, Helvetica, sans-serif"
        "fontSize": "20px"
    }

    return stylesheet, cy_style, page_style



# ========================================================================
# PART 9 — RUN APP
# ========================================================================

if __name__ == "__main__":
    app.run(debug=True)
