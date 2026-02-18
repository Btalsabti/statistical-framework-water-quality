import dash
from dash import html, Input, Output, dcc
import dash_cytoscape as cyto

# --------------------------------------------------------------
# PART 1 — INITIALIZE DASH APP
# --------------------------------------------------------------
app = dash.Dash(__name__)
server = app.server

# --------------------------------------------------------------
# PART 2 — DECISION TREE STRUCTURE
# --------------------------------------------------------------

tree = {
    "root": ["Exploratory Analysis"],
    "Exploratory Analysis": ["Normality Tests"],
    "Normality Tests": ["Univariate", "Multivariate"],

    "Univariate": ["Univariate Graphical", "Univariate Formal"],
    "Univariate Graphical": ["Q–Q Plot", "Histogram", "Box Plot", "Dot Plot"],
    "Univariate Formal": [
        "Shapiro–Wilk",
        "Anderson–Darling",
        "Kolmogorov–Smirnov",
        "D’Agostino Skewness",
        "Anscombe–Glynn Kurtosis"
    ],

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
    ]
}

# --------------------------------------------------------------
# PART 2B — DETAILS FOR INFO PANEL
# --------------------------------------------------------------

node_details = {
    "Shapiro–Wilk": {
        "description": "Best normality test for small samples (n < 50).",
        "formula": r"W = \frac{(\sum a_i x_{(i)})^2}{\sum (x_i - \bar{x})^2}",
        "rules": ["Recommended for n < 50", "Sensitive to tails"],
        "interpretation": ["p < 0.05 → NOT normal"],
        "example": "Example: p = 0.03 → reject normality.",
        "citation": "Shapiro & Wilk (1965). Biometrika.",
        "image": "shapiro.png"
    },
    "Q–Q Plot": {
        "description": "Graphical normality test.",
        "formula": "No formula (graphical).",
        "rules": ["Good visual check"],
        "interpretation": ["Points on line → normal"],
        "example": "Example: S-shape → skewness.",
        "citation": "Wilk & Gnanadesikan (1968).",
        "image": "qqplot.png"
    },
    "Histogram": {
        "description": "Visualizes distribution shape.",
        "formula": "No formula.",
        "rules": ["Choose bins carefully"],
        "interpretation": ["Bell shape → normal"],
        "citation": "Cleveland (1985).",
        "image": "histogram.png"
    },
    "Mardia Skewness": {
        "description": "Multivariate skewness measure.",
        "formula": r"b_{1,p} = \frac{1}{n^2}\sum_{i,j}[(x_i-\bar{x})^TS^{-1}(x_j-\bar{x})]^3",
        "rules": ["Requires invertible covariance"],
        "interpretation": ["Large value → not normal"],
        "example": "Example: b > χ² crit → reject normality.",
        "citation": "Mardia (1970). Biometrika.",
        "image": "mardia.png"
    }
}

# --------------------------------------------------------------
# PART 3 — INITIAL GRAPH ELEMENTS
# --------------------------------------------------------------

elements = [
    {"data": {"id": "root", "label": "Statistical Decision Tree"}, "position": {"x": 400, "y": 50}}
]

expanded_nodes = set()

# --------------------------------------------------------------
# PART 4 — NODE EXPANSION / COLLAPSE LOGIC
# --------------------------------------------------------------

def toggle_node(node_id, current_elements):
    global expanded_nodes

    # COLLAPSE
    if node_id in expanded_nodes:
        expanded_nodes.remove(node_id)
        children = tree.get(node_id, [])

        new_list = []
        for el in current_elements:
            if "source" in el.get("data", {}) and el["data"]["source"] == node_id:
                continue
            if "id" in el.get("data", {}) and el["data"]["id"] in children:
                continue
            new_list.append(el)

        return new_list

    # EXPAND
    expanded_nodes.add(node_id)

    parent_x = parent_y = 0
    for el in current_elements:
        if el["data"].get("id") == node_id:
            parent_x = el["position"]["x"]
            parent_y = el["position"]["y"]

    children = tree.get(node_id, [])
    spacing = 180
    start_x = parent_x - (len(children) - 1) * spacing / 2
    child_y = parent_y + 130

    new_list = current_elements.copy()

    for i, child in enumerate(children):
        new_list.append({
            "data": {"id": child, "label": child},
            "position": {"x": start_x + i * spacing, "y": child_y}
        })
        new_list.append({"data": {"source": node_id, "target": child}})

    return new_list

# --------------------------------------------------------------
# PART 5 — THEMES
# --------------------------------------------------------------

LIGHT = {
    "page": "white",
    "text": "black",
    "cy_bg": "#f2f2f2",
    "node": "#0072B2",
    "node_text": "white",
    "border": "#D55E00",
    "edge": "#555"
}

DARK = {
    "page": "#2b2b2b",
    "text": "white",
    "cy_bg": "#3a3a3a",
    "node": "#0072B2",
    "node_text": "white",
    "border": "#F0E442",
    "edge": "#ccc"
}

# --------------------------------------------------------------
# PART 6 — LAYOUT
# --------------------------------------------------------------

app.layout = html.Div(
    id="page-container",
    children=[
        html.H1("📊 Collapsible Statistical Decision Tree"),
        html.P("Click any node to expand or collapse."),

        # THEME SWITCH
        html.Div([
            html.Label("Theme:"),
            dcc.RadioItems(
                id="theme",
                options=[
                    {"label": "🌞 Light", "value": "light"},
                    {"label": "🌙 Dark", "value": "dark"},
                ],
                value="dark",
                inline=True
            )
        ], style={"marginBottom": "15px"}),

        cyto.Cytoscape(
            id="cy",
            layout={"name": "preset"},
            elements=elements,
            style={"width": "100%", "height": "700px"},
            stylesheet=[]
        ),

        html.Div(id="info", style={"marginTop": "25px"})
    ]
)

# --------------------------------------------------------------
# PART 7 — CLICK CALLBACK
# --------------------------------------------------------------

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

    if node_id in node_details:
        d = node_details[node_id]
        return elements, html.Div([
            html.H2(node_id),
            html.P(d["description"]),
            html.H3("Rules"), html.Ul([html.Li(x) for x in d["rules"]]),
            html.H3("Interpretation"), html.Ul([html.Li(x) for x in d["interpretation"]]),
            html.H3("Example"), html.P(d["example"]),
            html.H3("Formula"), html.Pre(d["formula"]),
            html.H3("Citation"), html.P(d["citation"]),
            html.H3("Image"),
            html.Img(src="/assets/" + d["image"], style={"width": "60%", "margin": "20px"})
        ])

    return elements, f"You selected: {node_id}"

# --------------------------------------------------------------
# PART 8 — THEME CALLBACK
# --------------------------------------------------------------

@app.callback(
    Output("cy", "stylesheet"),
    Output("cy", "style"),
    Output("page-container", "style"),
    Input("theme", "value")
)
def update_theme(mode):

    theme = LIGHT if mode == "light" else DARK

    stylesheet = [
        {"selector": "node",
         "style": {
             "content": "data(label)",
             "background-color": theme["node"],
             "color": theme["node_text"],
             "border-color": theme["border"],
             "border-width": 2,
             "shape": "round-rectangle",
             "text-valign": "center",
             "text-halign": "center",
             "width": 180,
             "height": 60,
             "font-size": "14px"
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
        "padding": "20px"
    }

    return stylesheet, cy_style, page_style

# --------------------------------------------------------------
# PART 9 — RUN APP
# --------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
