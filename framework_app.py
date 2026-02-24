# To enter the .venv type [ source .venv/bin/activate ] in the terminal and bash
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

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True
)
server = app.server   # ⭐ REQUIRED FOR RENDER ⭐

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

    # ------------------- STEP 1 -------------------
    "Exploratory Analysis": ["Data size"],

    "Data size": ["50 - 100", "> 100"],

    # ------------------- IF SAMPLE SIZE 50–100 -------------------
    "50 - 100": ["Normality Tests"],

    "Normality Tests": [
        "Univariate normality test",
        "Multivariate normality test"
    ],

# ------------------- UNIVARIATE NORMALITY -------------------
    "Univariate normality test": ["Univariate Graphical", "Univariate Formal"],

    "Univariate Graphical": [
        "Q–Q Plot", 
        "Histogram", 
        "Box Plot", 
        "Dot Plot"
    ],

    "Univariate Formal": [
        "Shapiro–Wilk",
        "Kolmogorov–\nSmirnov",
    ],

    # ------------------- FORMAL TEST RESULTS -------------------
    "Shapiro–Wilk": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],
    "Kolmogorov–Smirnov": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],
  
    # Add missing node definitions (IMPORTANT)
    "p ≥ 0.05\nNormal": [
        #"Pearson's correlation",
        "Bivariate tests N",
        "Multivariate tests N",
        #"t-test",
        #"ANOVA",
        #"Simple linear regression"
    ],
    "p < 0.05\nNot Normal": [
        #"Spearman's correlation",
        "Bivariate tests NN",
        "Multivariate tests NN",
        #"Mann–Whitney U test",
       # "Kruskal–Wallis",
        #"PMF"
    ],

    # ---------------- MULTIVARIATE -----------------
    "Multivariate normality test": ["Multivariate Graphical", "Multivariate Formal"],

    "Multivariate Graphical": [
        "Gamma Plot",
        "Chi-Square Q–Q Plot",
        "Multivariate Q–Q Plot"
    ],

    "Multivariate Formal": [
        "Mardia’s skewness",
        "Mardia’s kurtosis",
    ],

    # Multivariate normality test results
    "Mardia’s skewness": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],
    "Mardia’s kurtosis": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],

    # Add missing node definitions
    "Multivariate Normal": [
        "Principal Component\nAnalysis",
        "Factor Analysis",
        "Discriminant Analysis",
        "Hierarchical\nCluster Analysis",
    ],

    "Multivariate Not Normal": [
        "PMF",
        "Robust PCA",
        "K-means Clustering",
        "Nonparametric Discriminant Analysis"
    ],
    
    "Bivariate tests NN": [
        "Spearman's correlation",
    ],
    "Multivariate tests NN": [
        "PMF",
    ],    
    
    # ------------------- IF SAMPLE SIZE > 100 -------------------
    "> 100": ["Bivariate tests N", "Multivariate tests N"],

    "Bivariate tests N": [
        "Pearson's correlation",
    ],

    "Multivariate tests N": [
        "Principal Component\nAnalysis",
        "Factor Analysis",
        "Discriminant Analysis",
        "Hierarchical\nCluster Analysis",
        "PMF"
    ]
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
    # > 100
    # --------------------------------------------------------------------
    "> 100": {
        "description": "Based on the Central Limit Theorem which explaines that the sampling distribution of the mean"
        " tends to be normal for large samples (n > 100)",
        "formula": "-",
        "rules": [
            "-",
        ],
        "interpretation": [
            "-",
            "-"
        ],
        "example": "-",
        "citation": "Cao et al. (2024)",
        "image": "shapiro.png"
    },

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
    # Kolmogorov–\n Smirnov
    # --------------------------------------------------------------------
    "Kolmogorov–\nSmirnov": {
        "description": (
        "The Kolmogorov–Smirnov (K–S) test compares the empirical distribution "
        "of sample data to a reference distribution (commonly normal). It is "
        "less powerful than Shapiro–Wilk for small sample sizes but useful for "
        "general goodness-of-fit testing."
         ),
        "formula": (
        r"D = \max |F_n(x) - F(x)| \n"
        r"Where F_n(x) is the empirical CDF and F(x) is the theoretical CDF."
         ),
         "citation": "Kolmogorov (1933); Smirnov (1939).",
        "image": "ks_test.png"
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

    # --------------------------------------------------------------------
    # Gamma Plot
    # --------------------------------------------------------------------    
    "Gamma Plot": {
    "description": (
        "A Gamma plot is a multivariate graphical technique that evaluates "
        "whether the squared Mahalanobis distances follow a linear trend. "
        "Used for diagnosing multivariate normality."
    ),
    "formula": (
        r"D^2 = (x - \bar{x})^T S^{-1} (x - \bar{x}) \n"
        "A linear trend in ordered D² values suggests multivariate normality."
    ),
    "citation": "Mardia (1970); Gnanadesikan (1977). Methods for Statistical Data Analysis.",
    "image": "gamma_plot.png"
},    
    
    # --------------------------------------------------------------------
    # Chi-Square Q–Q Plot
    # --------------------------------------------------------------------       
    "Chi-Square Q–Q Plot": {
    "description": (
        "Plots ordered Mahalanobis distances against theoretical chi-square "
        "quantiles. If points fall on a straight line, multivariate normality "
        "is plausible."
    ),
    "formula": (
        r"D^2_i = (x_i - \bar{x})^T S^{-1} (x_i - \bar{x}) \n"
        r"Compare ordered D² values to χ²(p) quantiles."
    ),
    "citation": "Rencher & Christensen (2012). Methods of Multivariate Analysis.",
    "image": "chi_square_qq.png"
},
    
    # --------------------------------------------------------------------
    # Multivariate Q–Q Plot
    # --------------------------------------------------------------------       
    "Multivariate Q–Q Plot": {
    "description": (
        "Generalized Q–Q plot comparing the empirical distribution of "
        "Mahalanobis distances to a theoretical chi-square distribution. "
        "Used for assessing multivariate normality."
    ),
    "formula": (
        r"D^2 = (x - \bar{x})^T S^{-1} (x - \bar{x}) \n"
        "Points close to the diagonal indicate multivariate normality."
    ),
    "citation": "Li (1991). Multivariate Q–Q Plots for Assessing Normality.",
    "image": "mv_qqplot.png"
},
    
    # --------------------------------------------------------------------
    # Mardia’s skewness
    # --------------------------------------------------------------------        
    "Mardia’s skewness": {
    "description": (
        "Mardia’s multivariate skewness measures the departure from symmetry "
        "in a multivariate distribution. Large skewness indicates deviation "
        "from multivariate normality."
    ),
    "formula": (
        r"b_{1,p} = \frac{1}{n^2}\sum_{i=1}^{n}\sum_{j=1}^{n} "
        r"[(x_i - \bar{x})^T S^{-1}(x_j - \bar{x})]^3"
    ),
    "citation": "Mardia, K.V. (1970). Measures of multivariate skewness and kurtosis.",
    "image": "mardia_skew.png"
},    
    
    # --------------------------------------------------------------------
    # Mardia’s kurtosis
    # --------------------------------------------------------------------  
    "Mardia’s kurtosis": {
    "description": (
        "Mardia’s multivariate kurtosis evaluates how heavy-tailed the "
        "multivariate distribution is. Excess kurtosis indicates significant "
        "departure from multivariate normality."
    ),
    "formula": (
        r"b_{2,p} = \frac{1}{n}\sum_{i=1}^{n} "
        r"[(x_i - \bar{x})^T S^{-1}(x_i - \bar{x})]^2"
    ),
    "citation": "Mardia, K.V. (1970). Measures of multivariate skewness and kurtosis.",
    "image": "mardia_kurtosis.png"
},
    
    
    # --------------------------------------------------------------------    
    # PEARSON CORRELATION
    # --------------------------------------------------------------------
    "Pearson's correlation": {
    "description": (
        "Pearson's correlation coefficient (r) measures the strength and "
        "direction of a linear relationship between two continuous variables.\n\n"
        "Assumptions:\n"
        "• Variables are normally distributed\n"
        "• Relationship is linear\n"
        "• No extreme outliers\n"
    ),
    "formula": r"r = \frac{\sum (x - \bar{x})(y - \bar{y})}{\sqrt{\sum (x - \bar{x})^2 \sum (y - \bar{y})^2}}",
    "citation": "Pearson, K. (1895). Proceedings of the Royal Society of London.",
    "image": "pearson.png"
},
    # --------------------------------------------------------------------
    # SPEARMAN CORRELATION 
    # --------------------------------------------------------------------
    "Spearman's correlation": {
    "description": (
        "Spearman's rank correlation (ρ) measures monotonic relationships "
        "between two variables. It does NOT require normality and is robust "
        "to outliers.\n\n"
        "When to use:\n"
        "• Data not normally distributed\n"
        "• Relationship is monotonic but not necessarily linear\n"
        "• Variables are ordinal or ranked"
    ),
    "formula": r"ρ = 1 - \frac{6\sum d_i^2}{n(n^2 - 1)}",
    "citation": "Spearman, C. (1904). The American Journal of Psychology.",
    "image": "spearman.png"
},

    # ====================================================================
    # NEW: PCA / FA / PMF DETAILS
    # ====================================================================

    "Principal Component\nAnalysis": {
        "description": "Principal Component Analysis (PCA) reduces dimensionality by maximizing variance.\n\n"
                       "When to use:\n"
                       "• You want to summarize many correlated variables\n"
                       "• You want orthogonal components\n"
                       "• You assume linear relationships\n",
        "formula": r"Z = XW \quad \text{(eigenvectors of covariance matrix)}",
        "citation": "Jolliffe (2002). Principal Component Analysis.",
        "image": "pca.png"
    },

    "Factor Analysis": {
        "description": "Factor Analysis (FA) models latent variables that explain observed correlations.\n\n"
                       "When to use:\n"
                       "• You want to identify underlying factors\n"
                       "• Shared variance is more important than total variance",
        "formula": r"X = \Lambda F + \epsilon",
        "citation": "Fabrigar et al. (1999). Psychological Methods.",
        "image": "fa.png"
    },
        # ---------------- DISCRIMINANT ANALYSIS ----------------
    "Discriminant Analysis": {
        "description": (
            "Discriminant Analysis finds linear combinations of predictors that best separate predefined groups.\n\n"
            "Used when:\n"
            "• Groups are known (supervised)\n"
            "• Goal is classification or group prediction"
        ),
        "formula": r"D = w_1x_1 + w_2x_2 + \dots + w_px_p",
        "citation": "Fisher (1936). Annals of Eugenics.",
        "image": "da.png"
    },
    
        # ---------------- HIERARCHICAL CLUSTER ANALYSIS ----------------
    "Hierarchical\nCluster Analysis": {
        "description": (
            "HCA builds nested clusters using distance-based or linkage-based algorithms.\n\n"
            "Used when:\n"
            "• You want tree-like structure (dendrogram)\n"
            "• Number of clusters not known in advance"
        ),
        "formula": "Distance metrics like Euclidean; linkage methods such as Ward's or complete linkage.",
        "citation": "Ward (1963). Journal of the American Statistical Association.",
        "image": "hca.png"
    },

    "PMF": {
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

def toggle_node(node_id, current_elements):
    global expanded_nodes

    # ---------------- COLLAPSE ----------------
    if node_id in expanded_nodes:
        expanded_nodes.remove(node_id)

        # recursively gather all descendants
        def get_descendants(parent):
            children = tree.get(parent, [])
            all_desc = set(children)
            for child in children:
                all_desc |= get_descendants(child)
            return all_desc

        descendants = get_descendants(node_id)

        new_elements = []
        for el in current_elements:
            data = el.get("data", {})

            # remove edges from parent or any descendant
            if data.get("source") in descendants or data.get("source") == node_id:
                continue
            if data.get("target") in descendants:
                continue

            # remove nodes that are descendants
            if data.get("id") in descendants:
                continue

            new_elements.append(el)

        return new_elements

    # ---------------- EXPAND ----------------
    expanded_nodes.add(node_id)

    parent_pos = None
    for el in current_elements:
        if el["data"].get("id") == node_id:
            parent_pos = el["position"]
            break

    parent_x, parent_y = parent_pos["x"], parent_pos["y"]
    children = tree.get(node_id, [])

    spacing = 200
    start_x = parent_x - (len(children) - 1) * spacing / 2
    child_y = parent_y + 140

    new_elements = current_elements.copy()

    for i, child in enumerate(children):
        new_elements.append({
            "data": {"id": child, "label": child},
            "position": {"x": start_x + i * spacing, "y": child_y}
        })
        new_elements.append({
            "data": {"source": node_id, "target": child}
        })

    return new_elements


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

        # MathJax LaTeX support
        html.Script(src="https://polyfill.io/v3/polyfill.min.js?features=es6"),
        html.Script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),

        html.H1("📊 Statistical Framework for Water Quality Assessment"),
        html.P("Click the nodes to expand/collapse and explore full statistical details.\nUse the mouse scroll wheel to zoom in/out."),

        # Theme selector
        dcc.RadioItems(
            id="theme",
            options=[
                {"label": "🌞 Light", "value": "light"},
                {"label": "🌙 Dark", "value": "dark"},
            ],
            value="light",
            inline=True
        ),

        # ------------- SPLIT SCREEN (TREE LEFT • INFO PANEL RIGHT) -------------
        html.Div(
            style={
                "display": "flex",
                "flexDirection": "row",
                "width": "100%",
                "height": "750px",
                "marginTop": "20px"
            },
            children=[

                # LEFT AREA — TREE (70%)
                html.Div(
                    style={"width": "70%", "paddingRight": "15px"},
                    children=[
                        cyto.Cytoscape(
                            id="cy",
                            layout={"name": "preset"},
                            style={"width": "100%", "height": "100%"},
                            elements=elements,
                            stylesheet=[],
    
                    # ⭐ These 3 settings prevent zoom bugs
                            minZoom=0.2,
                            maxZoom=2,
                            zoom=0.6,   # ⭐ DEFAULT ZOOM (fits your tree)
                        )
                    ]
                ),

                # RIGHT AREA — INFO PANEL (30%)
                html.Div(
                    id="info",
                    style={
                        "width": "30%",
                        "borderLeft": "2px solid #ccc",
                        "padding": "15px",
                        "overflowY": "scroll",
                        "fontSize": "20px"
                    }
                )
            ]
        ),

        html.Hr(style={"marginTop": "20px", "opacity": 0.3}),
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
                    html.A("btalsabti93@gmail.com",
                           href="mailto:btalsabti93@gmail.com",
                           style={"textDecoration": "none"}),
                    html.Span(" • "),
                    html.A("Research Gate",
                           href="https://www.researchgate.net/profile/Bedour-Alsabti",
                           target="_blank",
                           style={"textDecoration": "none"}),
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

    # If no details exist
    if node_id not in node_details:
        return elements, html.H3(f"You selected: {node_id}")

    d = node_details[node_id]

    # ------------------- INITIAL DEFAULT CONTENT -------------------
    default_text = d.get("description", "")

    # ------------------- RIGHT PANEL LAYOUT ------------------------
    panel = html.Div(

        children=[
            html.Div(
                children=[
                    html.Button("📘 Description", id="btn-desc", n_clicks=1,
                                style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),

                    html.Button("∑ Formula", id="btn-formula", n_clicks=0,
                                style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),

                    html.Button("📚 Citation", id="btn-citation", n_clicks=0,
                                style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),

                    html.Button("🖼 Image", id="btn-image", n_clicks=0,
                                style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),
                ]
            ),

            html.Hr(),

            html.Div(
                id="content-panel",
                children=html.Pre(
                    default_text,
                    style={
                        "whiteSpace": "pre-wrap",
                        "fontFamily": "Times New Roman, Times, serif",
                        "fontSize": "20px",
                        "lineHeight": "1.6"
                    }
                )
            )
        ]
    )

    return elements, panel

#---------------------------

@app.callback(
    Output("content-panel", "children"),
    Input("btn-desc", "n_clicks"),
    Input("btn-formula", "n_clicks"),
    Input("btn-citation", "n_clicks"),
    Input("btn-image", "n_clicks"),
    Input("cy", "tapNodeData")
)
def update_panel(desc, formula, citation, image, node):

    if not node or node["id"] not in node_details:
        return ""

    d = node_details[node["id"]]
    ctx = dash.callback_context.triggered_id

    # ---------------- DESCRIPTION -----------------
    if ctx == "btn-desc":
        return html.Pre(
            d.get("description", ""),
            style={
                "whiteSpace": "pre-wrap",
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px",
                "lineHeight": "1.6"
            }
        )

    # ---------------- FORMULA (LaTeX) -----------------
    if ctx == "btn-formula":
        return html.Div([
            html.Div(
                d.get("formula", ""),
                style={
                    "fontSize": "22px",
                    "fontFamily": "Times New Roman, Times, serif",
                    "lineHeight": "1.6"
                }
            ),
            html.Script("MathJax.typeset();")
        ])

    # ---------------- CITATION -----------------
    if ctx == "btn-citation":
        return html.P(
            d.get("citation", ""),
            style={
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px"
            }
        )

    # ---------------- IMAGE -----------------
    if ctx == "btn-image":
        return html.Img(
            src="/assets/" + d.get("image", ""),
            style={"width": "90%", "marginTop": "15px"}
        )

    # Default fallback
    return html.Pre(d.get("description", ""), style={"whiteSpace": "pre-wrap"})
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
    {
    "selector": "core",
    "style": {"font-family": "Times New Roman, Times, serif"}
    },
    {
    "selector": "label",
    "style": {"font-family": "Times New Roman, Times, serif"}
    },
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
        "fontSize": "20px",
        "lineHeight": "1",
        "paddingBottom": "20px",
        "maxWidth": "1920px",
        #"maxHight": "1080px",
        "margin": "0 auto",    
    }

    return stylesheet, cy_style, page_style



# ========================================================================
# PART 9 — RUN APP
# ========================================================================


if __name__ == "__main__":
    app.run(debug=True)
 



