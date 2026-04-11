# To enter the .venv type [ source .venv/bin/activate ] in the terminal and bash
# to # multiple lines click (cmd+/) while highliting the lines 
# ========================================================================
#  FRAMEWORK APP — INTERACTIVE COLLAPSIBLE DECISION TREE (DASH)
#  Prepared for scientific publication + extendable by the author.
#  *** EVERY SECTION IS EXPLAINED SO YOU CAN MODIFY IT EASILY ***
# ========================================================================
# To open the dash terminal run the full script. Press control+C to close it and return you back to main terminal.
# ========================================================================

#LIBRARIES 

import dash
from dash import html, Input, Output, dcc
import dash_cytoscape as cyto
from dash.dependencies import ALL 
from dash.dependencies import Input, Output, State, ALL
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
# PART 2 — TREE ORGANISATION
# ========================================================================
# This section is now split into:
#   A. METHOD_GROUPS     → controls the dropdown navigation
#   B. STRUCTURAL_NODES  → non-method tree labels
#   C. TREE_* sections   → actual tree branches
#
# To edit the tree:
#   - add/remove branches inside TREE_* dictionaries
#   - keep node names EXACTLY the same everywhere
# ========================================================================

# ------------------------------------------
# A. Statistical method legend / navigation
# ------------------------------------------
METHOD_GROUPS = {
    "Univariate": [
        "Univariate normality test",
        "Shapiro–Wilk",
        "Kolmogorov–\nSmirnov",
    ],
    "Bivariate": [
        "Pearson's correlation",
        "Spearman's correlation"
    ],
    "Multivariate": [
        "Multivariate normality test",
        "Principal Component\nAnalysis",
        "Factor Analysis",
        "Hierarchical\nCluster Analysis",
        "Positive Matrix\nFactorization",
        "Discriminant Analysis"
    ]
}

# ------------------------------------------
# B. Structural / navigation-only nodes
# ------------------------------------------
STRUCTURAL_NODES = {
    "root",
    "Exploratory Analysis",
    "Data size",
    "Normality Tests",
    "Univariate normality test",
    "Multivariate normality test",
    "Univariate Graphical",
    "Univariate Formal",
    "Multivariate Graphical",
    "Multivariate Formal",
    "Bivariate tests N",
    "Bivariate tests NN",
    "Multivariate tests N",
    "Multivariate tests NN",
    "p ≥ 0.05\nNormal",
    "p < 0.05\nNot Normal",
    "n < 100",
    "n > 100",
    "Box Plot",
    "Dot Plot",
    "Multivariate Normal",
    "Multivariate Not Normal",
}

# ------------------------------------------
# C. Tree branches
# ------------------------------------------

TREE_ROOT = {
    "Exploratory Analysis": ["Data size"],
    "Data size": ["n < 100", "n > 100"],
}

TREE_UNIVARIATE = {
    "n < 100": ["Normality Tests"],
    "Normality Tests": ["Univariate normality test", "Multivariate normality test"],

    "Univariate normality test": ["Univariate Graphical", "Univariate Formal"],
    "Univariate Graphical": ["Q–Q Plot", "Histogram", "Box Plot", "Dot Plot"],
    "Univariate Formal": ["Shapiro–Wilk", "Kolmogorov–\nSmirnov"],

    "Shapiro–Wilk": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],
    "Kolmogorov–\nSmirnov": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],
}

TREE_MULTIVARIATE = {
    "Multivariate normality test": ["Multivariate Graphical", "Multivariate Formal"],
    "Multivariate Graphical": ["Gamma Plot", "Chi-Square Q–Q Plot", "Multivariate Q–Q Plot"],
    "Multivariate Formal": ["Mardia’s skewness", "Mardia’s kurtosis"],

    "Mardia’s skewness": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],
    "Mardia’s kurtosis": ["p ≥ 0.05\nNormal", "p < 0.05\nNot Normal"],
}

TREE_RESULTS = {
    "p ≥ 0.05\nNormal": ["Bivariate tests N", "Multivariate tests N"],
    "p < 0.05\nNot Normal": ["Bivariate tests NN", "Multivariate tests NN"],

    "Bivariate tests N": ["Pearson's correlation"],
    "Bivariate tests NN": ["Spearman's correlation"],

    "Multivariate tests N": [
        "Principal Component\nAnalysis",
        "Factor Analysis",
        "Discriminant Analysis",
        "Hierarchical\nCluster Analysis",
        "Positive Matrix\nFactorization"
    ],
    "Multivariate tests NN": [
        "Positive Matrix\nFactorization"
    ],
}

TREE_LARGE_SAMPLE = {
    "n > 100": ["Bivariate tests N", "Multivariate tests N"]
}

# ------------------------------------------
# Final combined tree
# ------------------------------------------
tree = {}
for section in [
    TREE_ROOT,
    TREE_UNIVARIATE,
    TREE_MULTIVARIATE,
    TREE_RESULTS,
    TREE_LARGE_SAMPLE,
]:
    tree.update(section)

# ========================================================================
# PART 2B — METHOD INFORMATION
# ========================================================================
# This section is now standardised.
#
# To add a new method:
#   1. Add its node name in the tree
#   2. Add its content below using make_method(...)
#
# Standard fields:
#   - description
#   - interpretation
#   - limitations
#   - citation
#   - image
#   - formula
#   - example
# ========================================================================

def make_method(
    description="",
    interpretation="",
    limitations="",
    citation="",
    image="",
    formula="",
    example="",
):
    return {
        "description": description,
        "interpretation": interpretation,
        "limitations": limitations,
        "citation": citation,
        "image": image,
        "formula": formula,
        "example": example,
    }

node_details = {

    # --------------------------------------------------------------------
    # n > 100
    # --------------------------------------------------------------------
    "n > 100": make_method(
        description=(
            "Based on the Central Limit Theorem, the sampling distribution "
            "of the mean tends to approach normality for large sample sizes "
            "(n > 100)."
        ),
        interpretation=(
            "• Large sample sizes often support the use of parametric methods more easily\n"
            "• However, assumption checks may still be needed depending on the method"
        ),
        limitations=(
            "• A large sample size does not automatically mean all variables are normally distributed\n"
            "• Multivariate methods may still require additional assumption checks"
        ),
        citation="Cao et al. (2024).",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Shapiro–Wilk
    # --------------------------------------------------------------------
    "Shapiro–Wilk": make_method(
        description="Best normality test for small samples (n < 50). Very sensitive to tail deviations.",
        interpretation=(
            "• p < 0.05 → data significantly deviates from normality\n"
            "• p ≥ 0.05 → normality cannot be rejected"
        ),
        limitations=(
            "• Very sensitive to outliers\n"
            "• Not suitable for very large samples (n > 2000)\n"
            "• Assumes continuous data"
        ),
        formula=r"W = \frac{(\sum a_i x_{(i)})^2}{\sum (x_i - \bar{x})^2}",
        example="Example: n = 25 gives p = 0.03 → not normally distributed.",
        citation="Shapiro & Wilk (1965). Biometrika.",
        image="Shapirowilk_1965_eq.png"
    ),

    # --------------------------------------------------------------------
    # Kolmogorov–Smirnov
    # --------------------------------------------------------------------
    "Kolmogorov–\nSmirnov": make_method(
        description=(
            "The Kolmogorov–Smirnov (K–S) test compares the empirical distribution "
            "of sample data to a reference distribution (commonly normal). It is "
            "less powerful than Shapiro–Wilk for small sample sizes but useful for "
            "general goodness-of-fit testing."
        ),
        interpretation=(
            "• Measures the maximum difference between empirical and theoretical CDF\n"
            "• p < 0.05 → distribution differs significantly from the normal distribution\n"
            "• Works for medium to large samples"
        ),
        limitations=(
            "• Low power for small samples\n"
            "• Assumes parameters of reference distribution are known (unless corrected)\n"
            "• Less sensitive than Shapiro–Wilk for tail deviations"
        ),
        formula=r"D = \max_x |F_n(x) - F(x)|",
        citation="Kolmogorov (1933); Smirnov (1939).",
        image="Kolmogorov_eq.PNG"
    ),

    # --------------------------------------------------------------------
    # Q–Q Plot
    # --------------------------------------------------------------------
    "Q–Q Plot": make_method(
        description="A graphical method to check whether data follows a normal distribution.",
        interpretation=(
            "• Points on a straight line → normality is plausible\n"
            "• S-shaped curve → skewness may be present\n"
            "• Deviations at ends → heavy or light tails"
        ),
        limitations=(
            "• Subjective assessment\n"
            "• Hard to interpret with very large datasets\n"
            "• Outliers strongly influence the visual appearance"
        ),
        formula="No formula (graphical method).",
        example="Example: upward deviation in the right tail → right-skewed data.",
        citation="Wilk & Gnanadesikan (1968). Biometrika.",
        image="Q_Q_plot_1.png"
    ),

    # --------------------------------------------------------------------
    # Histogram
    # --------------------------------------------------------------------
    "Histogram": make_method(
        description="Basic visual method for checking distribution shape.",
        interpretation=(
            "• Bell-shaped curve → suggests approximate normality\n"
            "• Skewed or multi-modal shapes → indicate deviation from normality"
        ),
        limitations=(
            "• Highly sensitive to bin width\n"
            "• Only a visual guide, not a formal statistical test"
        ),
        formula="No formula.",
        example="Example: an uneven shape may suggest skewness or multiple populations.",
        citation="Cleveland (1985). The Elements of Graphing Data.",
        image="Histogram_1.png"
    ),


    # --------------------------------------------------------------------
    # Gamma Plot
    # --------------------------------------------------------------------
    "Gamma Plot": make_method(
        description=(
            "A Gamma plot is a multivariate graphical technique that evaluates "
            "whether the squared Mahalanobis distances follow a linear trend. "
            "It is used for diagnosing multivariate normality."
        ),
        interpretation=(
            "• Linear pattern in ordered Mahalanobis distances → multivariate normality likely\n"
            "• Curved pattern → deviation from multivariate normality"
        ),
        limitations=(
            "• Requires stable estimation of the covariance matrix\n"
            "• Sensitive to outliers and high dimensionality"
        ),
        formula=(
            r"D^2 = (x - \bar{x})^T S^{-1} (x - \bar{x})" "\n"
            "A linear trend in ordered D² values suggests multivariate normality."
        ),
        citation="Mardia (1970); Gnanadesikan (1977). Methods for Statistical Data Analysis.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Chi-Square Q–Q Plot
    # --------------------------------------------------------------------
    "Chi-Square Q–Q Plot": make_method(
        description=(
            "Plots ordered Mahalanobis distances against theoretical chi-square "
            "quantiles. If points fall on a straight line, multivariate normality "
            "is plausible."
        ),
        interpretation=(
            "• Points on the diagonal line → data may follow multivariate normality\n"
            "• Systematic deviations → skewness, kurtosis, or covariance structure issues"
        ),
        limitations=(
            "• Depends heavily on reliable covariance estimation\n"
            "• Outliers can distort the plot strongly"
        ),
        formula=(
            r"D^2_i = (x_i - \bar{x})^T S^{-1} (x_i - \bar{x})" "\n"
            r"Compare ordered D² values to χ²(p) quantiles."
        ),
        citation="Rencher & Christensen (2012). Methods of Multivariate Analysis.",
        image="Chi_sqplot_1.png"
    ),

    # --------------------------------------------------------------------
    # Multivariate Q–Q Plot
    # --------------------------------------------------------------------
    "Multivariate Q–Q Plot": make_method(
        description=(
            "A generalized Q–Q plot comparing the empirical distribution of "
            "Mahalanobis distances to a theoretical chi-square distribution. "
            "Used for assessing multivariate normality."
        ),
        interpretation=(
            "• Close fit to the diagonal → supports multivariate normality\n"
            "• Deviations in the upper tail → heavy tails or multivariate outliers"
        ),
        limitations=(
            "• Requires adequate sample size relative to dimensionality\n"
            "• Visual method with subjective interpretation"
        ),
        formula=(
            r"D^2 = (x - \bar{x})^T S^{-1} (x - \bar{x})" "\n"
            "Points close to the diagonal indicate multivariate normality."
        ),
        citation="Li (1991). Multivariate Q–Q Plots for Assessing Normality.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Mardia’s skewness
    # --------------------------------------------------------------------
    "Mardia’s skewness": make_method(
        description=(
            "Mardia’s multivariate skewness measures the departure from symmetry "
            "in a multivariate distribution. Large skewness indicates deviation "
            "from multivariate normality."
        ),
        interpretation=(
            "• High b₁ₚ value → substantial multivariate skewness\n"
            "• p < 0.05 → reject multivariate normality"
        ),
        limitations=(
            "• Very sensitive to outliers\n"
            "• Requires an invertible covariance matrix\n"
            "• Not reliable for very small samples"
        ),
        formula=(
            r"b_{1,p} = \frac{1}{n^2}\sum_{i=1}^{n}\sum_{j=1}^{n}"
            r"[(x_i - \bar{x})^T S^{-1}(x_j - \bar{x})]^3"
        ),
        citation="Mardia, K.V. (1970). Wulandari et al., (2021)",
        image="M_Skewness_1.png"
    ),

    # --------------------------------------------------------------------
    # Mardia’s kurtosis
    # --------------------------------------------------------------------
    "Mardia’s kurtosis": make_method(
        description=(
            "Mardia’s multivariate kurtosis evaluates how heavy-tailed the "
            "multivariate distribution is. Excess kurtosis indicates departure "
            "from multivariate normality."
        ),
        interpretation=(
            "• b₂ₚ > expected value → heavy tails\n"
            "• b₂ₚ < expected value → light tails\n"
            "• Significant deviation → reject multivariate normality"
        ),
        limitations=(
            "• Sensitive to higher-order moment deviations\n"
            "• Requires adequate sample size (n > p)"
        ),
        formula=(
            r"b_{2,p} = \frac{1}{n}\sum_{i=1}^{n}"
            r"[(x_i - \bar{x})^T S^{-1}(x_i - \bar{x})]^2"
        ),
        citation="Mardia, K.V. (1970); Wulandari et al., (2021)",
        image="M_Kurtosis_1.png"
    ),

    # --------------------------------------------------------------------
    # Pearson correlation
    # --------------------------------------------------------------------
    "Pearson's correlation": make_method(
        description=(
            "Pearson's correlation coefficient (r) measures the strength and "
            "direction of a linear relationship between two continuous variables.\n\n"
            "Assumptions:\n"
            "• Variables are approximately normally distributed\n"
            "• Relationship is linear\n"
            "• No extreme outliers"
        ),
        interpretation=(
            "• r close to +1 → strong positive linear relationship\n"
            "• r close to -1 → strong negative linear relationship\n"
            "• r ≈ 0 → no linear relationship\n"
            "• p-value tests whether the relationship is statistically significant"
        ),
        limitations=(
            "• Only detects linear relationships\n"
            "• Highly sensitive to outliers\n"
            "• Requires approximate normality for standard inference"
        ),
        formula=r"r = \frac{\sum (x - \bar{x})(y - \bar{y})}{\sqrt{\sum (x - \bar{x})^2 \sum (y - \bar{y})^2}}",
        citation="Pearson, K. (1895). Proceedings of the Royal Society of London.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Spearman correlation
    # --------------------------------------------------------------------
    "Spearman's correlation": make_method(
        description=(
            "Spearman's rank correlation (ρ) measures monotonic relationships "
            "between two variables. It does not require normality and is more "
            "robust to outliers than Pearson’s correlation.\n\n"
            "Used when:\n"
            "• Data are not normally distributed\n"
            "• Relationship is monotonic but not necessarily linear\n"
            "• Variables are ordinal or ranked"
        ),
        interpretation=(
            "• ρ close to +1 or -1 → strong monotonic relationship\n"
            "• ρ ≈ 0 → no monotonic relationship\n"
            "• Useful for non-normal and ordinal data"
        ),
        limitations=(
            "• Does not detect non-monotonic nonlinear patterns\n"
            "• Ties in ranks can reduce precision"
        ),
        formula=r"ρ = 1 - \frac{6\sum d_i^2}{n(n^2 - 1)}",
        citation="Spearman, C. (1904). The American Journal of Psychology.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # PCA
    # --------------------------------------------------------------------
    "Principal Component\nAnalysis": make_method(
        description=(
            "Principal Component Analysis (PCA) reduces dimensionality by transforming "
            "correlated variables into a smaller set of orthogonal components.\n\n"
            "Used when:\n"
            "• You want to summarise many correlated variables\n"
            "• You want orthogonal components\n"
            "• You assume mainly linear relationships"
        ),
        interpretation=(
            "• High loadings indicate strong influence of variables on components\n"
            "• PC1 explains the largest proportion of variance"
        ),
        limitations=(
            "• Only captures linear structure\n"
            "• Sensitive to variable scaling\n"
            "• Sensitive to outliers"
        ),
        formula=r"Z = XW \quad \text{(eigenvectors of covariance/correlation matrix)}",
        citation="Jolliffe (2002). Principal Component Analysis.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Factor Analysis
    # --------------------------------------------------------------------
    "Factor Analysis": make_method(
        description=(
            "Factor Analysis (FA) models latent variables that explain observed "
            "correlations among measured variables.\n\n"
            "Used when:\n"
            "• You want to identify underlying latent factors\n"
            "• Shared variance is more important than total variance"
        ),
        interpretation=(
            "• Factors represent latent constructs underlying the observed variables\n"
            "• High communalities mean variables are well explained by the factor model"
        ),
        limitations=(
            "• Requires sufficiently large sample size\n"
            "• Factor rotation introduces subjectivity\n"
            "• Model fit can be poor if assumptions are violated"
        ),
        formula=r"X = \Lambda F + \epsilon",
        citation="Fabrigar et al. (1999). Psychological Methods.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Discriminant Analysis
    # --------------------------------------------------------------------
    "Discriminant Analysis": make_method(
        description=(
            "Discriminant Analysis finds linear combinations of predictors that best "
            "separate predefined groups.\n\n"
            "Used when:\n"
            "• Groups are known in advance (supervised setting)\n"
            "• The goal is classification or group prediction"
        ),
        interpretation=(
            "• Discriminant scores indicate separation among groups\n"
            "• Classification accuracy indicates predictive performance"
        ),
        limitations=(
            "• Assumes multivariate normality of predictors\n"
            "• Often assumes similar covariance matrices across groups\n"
            "• Sensitive to outliers"
        ),
        formula=r"D = w_1x_1 + w_2x_2 + \dots + w_px_p",
        citation="Fisher (1936). Annals of Eugenics.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Hierarchical Cluster Analysis
    # --------------------------------------------------------------------
    "Hierarchical\nCluster Analysis": make_method(
        description=(
            "Hierarchical Cluster Analysis (HCA) builds nested clusters using "
            "distance-based and linkage-based algorithms.\n\n"
            "Used when:\n"
            "• You want a dendrogram structure\n"
            "• The number of clusters is not known in advance"
        ),
        interpretation=(
            "• The dendrogram shows grouping structure\n"
            "• Fusion height reflects cluster similarity or dissimilarity"
        ),
        limitations=(
            "• Sensitive to scaling of variables\n"
            "• Different linkage methods may give different results\n"
            "• Earlier merge decisions cannot be revised"
        ),
        formula="Distance metrics such as Euclidean distance; linkage methods such as Ward's or complete linkage.",
        citation="Ward (1963). Journal of the American Statistical Association.",
        image="_"
    ),

    # --------------------------------------------------------------------
    # Positive matrix factorization
    # --------------------------------------------------------------------
    "Positive Matrix\nFactorization": make_method(
        description=(
            "Positive Matrix Factorization (PMF) is widely used in environmental "
            "sciences for source apportionment of compositional data.\n\n"
            "Used when:\n"
            "• You need source apportionment of pollutants\n"
            "• You work with chemical compositional data\n"
            "• Non-negative constraints are required"
        ),
        interpretation=(
            "• Factors represent source profiles\n"
            "• Contribution values indicate source strengths across samples"
        ),
        limitations=(
            "• Choosing the number of factors can be subjective\n"
            "• Rotational ambiguity affects stability\n"
            "• Requires reasonable uncertainty estimates\n"
            "• Sensitive to collinearity among variables"
        ),
        formula=r"X = GF + E",
        citation="Paatero & Tapper (1994). Environmetrics.",
        image="_"
    ),
}

# ========================================================================
# PART 3 — INITIAL ELEMENTS
# ========================================================================

elements = [
    {
        "data": {"id": "Exploratory Analysis", "label": "Exploratory\nAnalysis"},
        "position": {"x": 300, "y": 50}
    }
]

expanded_nodes = set()

# ========================================================================
# PART 4 — TREE HELPER FUNCTIONS
# ========================================================================

def toggle_node(node_id, current_elements):
    global expanded_nodes

    # ---------------- COLLAPSE ----------------
    if node_id in expanded_nodes:
        expanded_nodes.remove(node_id)

        def collect_descendants(parent):
            children = tree.get(parent, [])
            all_desc = set(children)
            for child in children:
                all_desc |= collect_descendants(child)
            return all_desc

        descendants = collect_descendants(node_id)

        new_elements = []
        for el in current_elements:
            data = el.get("data", {})

            if data.get("source") in descendants or data.get("source") == node_id:
                continue
            if data.get("target") in descendants:
                continue
            if data.get("id") in descendants:
                continue

            new_elements.append(el)

        return new_elements

    # ---------------- EXPAND ----------------
    expanded_nodes.add(node_id)

    parent_pos = None
    for el in current_elements:
        if el.get("data", {}).get("id") == node_id:
            parent_pos = el["position"]
            break

    if parent_pos is None:
        return current_elements

    parent_x, parent_y = parent_pos["x"], parent_pos["y"]
    children = tree.get(node_id, [])

    spacing = 200
    start_x = parent_x - (len(children) - 1) * spacing / 2
    child_y = parent_y + 140

    new_elements = current_elements.copy()

    existing_node_ids = {
        el.get("data", {}).get("id")
        for el in new_elements
        if "data" in el
    }
    existing_edges = {
        (el.get("data", {}).get("source"), el.get("data", {}).get("target"))
        for el in new_elements
        if el.get("data", {}).get("source") and el.get("data", {}).get("target")
    }

    for i, child in enumerate(children):
        if child not in existing_node_ids:
            new_elements.append({
                "data": {"id": child, "label": child},
                "position": {"x": start_x + i * spacing, "y": child_y}
            })

        if (node_id, child) not in existing_edges:
            new_elements.append({
                "data": {"source": node_id, "target": child}
            })

    return new_elements


def get_ancestors(node):
    parents = []
    for parent, children in tree.items():
        if node in children:
            parents.append(parent)
            parents.extend(get_ancestors(parent))
    return parents


def get_descendants(node):
    children = tree.get(node, [])
    all_desc = []
    for c in children:
        all_desc.append(c)
        all_desc.extend(get_descendants(c))
    return all_desc

# ========================================================================
# PART 5 — THEMES
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
# PART 6 — UI HELPERS
# ========================================================================

def method_selector():
    return html.Div(
        id="method-selector-box",
        style={
            "border": "1px solid #ccc",
            "borderRadius": "8px",
            "padding": "10px",
            "marginBottom": "10px"
        },
        children=[
            html.Div("Quick method selector", style={"fontWeight": "bold"}),

            dcc.Dropdown(
                id="method-group",
                options=[{"label": k, "value": k} for k in METHOD_GROUPS],
                placeholder="Select analysis level (Univariate / Bivariate / Multivariate)",
                style={"marginBottom": "8px"}
            ),

            dcc.Dropdown(
                id="method-name",
                placeholder="Select method",
            )
        ]
    )


def build_info_panel(method_name):
    if method_name not in node_details:
        return html.H3(f"You selected: {method_name}")

    d = node_details[method_name]

    return html.Div(
        children=[
            html.Div(
                children=[
                    html.Button(
                        "📘 Description", id="btn-desc", n_clicks=1,
                        style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}
                    ),
                    html.Button(
                        "🔍 Interpretation", id="btn-interpret", n_clicks=0,
                        style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}
                    ),
                    html.Button(
                        "⚠️ Limitations", id="btn-limit", n_clicks=0,
                        style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}
                    ),
                    html.Button(
                        "🖼 Image", id="btn-image", n_clicks=0,
                        style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}
                    ),
                    html.Button(
                        "📚 Citation", id="btn-citation", n_clicks=0,
                        style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}
                    ),
                ]
            ),
            html.Hr(),
            html.Div(
                id="content-panel",
                children=html.Pre(
                    d.get("description", ""),
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

# ========================================================================
# PART 7 — LAYOUT
# ========================================================================

app.layout = html.Div(
    id="page-container",
    children=[

        html.Script("""
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$','$$']]
            },
            svg: {
                fontCache: 'global'
            }
        };
        """),
        html.Script(src="https://polyfill.io/v3/polyfill.min.js?features=es6"),
        html.Script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),

        html.H1("📊 Decision Framework for Method Selection in Assessing Water Quality"),

        html.Button(
            "📘 User's Guide",
            id="toggle-guide",
            n_clicks=0,
            style={
                "marginTop": "10px",
                "marginBottom": "10px",
                "padding": "6px 14px",
                "fontSize": "16px",
                "cursor": "pointer"
            }
        ),

        html.Div(
            id="guide-box",
            style={"display": "none"},
        ),

        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "20px",
                "marginTop": "10px",
                "marginBottom": "10px"
            },
            children=[
                dcc.RadioItems(
                    id="theme",
                    options=[
                        {"label": "🌞 Light", "value": "light"},
                        {"label": "🌙 Dark", "value": "dark"},
                    ],
                    value="light",
                    inline=True
                ),

                html.Button(
                    "🔄 Reset Tree",
                    id="reset-tree",
                    n_clicks=0,
                    style={
                        "padding": "6px 14px",
                        "fontSize": "16px",
                        "cursor": "pointer"
                    }
                ),

                html.Button(
                    "📤 Export Tree",
                    id="export-tree",
                    n_clicks=0,
                    style={
                        "padding": "6px 14px",
                        "fontSize": "16px",
                        "cursor": "pointer"
                    },
                ),
            ]
        ),

        html.Div(
            style={
                "display": "flex",
                "flexDirection": "row",
                "width": "100%",
                "height": "600px",
                "marginTop": "20px"
            },
            children=[

                html.Div(
                    style={"width": "70%", "paddingRight": "15px"},
                    children=[
                        method_selector(),

                        cyto.Cytoscape(
                            id="cy",
                            generateImage={"type": "png"},
                            layout={"name": "preset"},
                            style={"width": "100%", "height": "100%"},
                            elements=elements,
                            stylesheet=[],
                            minZoom=0.2,
                            maxZoom=2,
                            zoom=0.6,
                        )
                    ]
                ),

                html.Div(
                    id="info",
                    style={
                        "width": "30%",
                        "borderLeft": "2px solid #ccc",
                        "padding": "15px",
                        "overflowY": "auto",
                        "fontSize": "20px"
                    },
                    children=[
                        html.Div(id="info-content"),
                        html.Hr(),
                        html.Div(
                            style={
                                "marginTop": "15px",
                                "textAlign": "center"
                            },
                            children=[]
                        )
                    ]
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
                    html.A(
                        "btalsabti93@gmail.com",
                        href="mailto:btalsabti93@gmail.com",
                        style={"textDecoration": "none"}
                    ),
                    html.Span(" • "),
                    html.A(
                        "ResearchGate",
                        href="https://www.researchgate.net/profile/Bedour-Alsabti",
                        target="_blank",
                        style={"textDecoration": "none"}
                    ),
                ]),
                html.Div("© 2026 Authors: Alsabti, B., Robinson, T., Sabarathinam, C., Viswanathan, P. M., & Wolff-Boenisch, D. All rights reserved."),
            ],
        ),
    ]
)

# ========================================================================
# PART 8 — MAIN TREE CALLBACK
# ========================================================================

@app.callback(
    Output("cy", "elements"),
    Output("info-content", "children"),
    Output("method-name", "value"),
    Output("method-group", "value"),
    Input("cy", "tapNodeData"),
    Input("method-name", "value"),
    Input("reset-tree", "n_clicks"),
    prevent_initial_call=True
)
def click_or_autofocus(node, selected_method, reset_clicks):
    global elements, expanded_nodes

    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    # --------------------------------------------------
    # RESET TREE
    # --------------------------------------------------
    if trigger == "reset-tree.n_clicks":
        elements = [
            {
                "data": {"id": "Exploratory Analysis", "label": "Exploratory\nAnalysis"},
                "position": {"x": 300, "y": 50}
            }
        ]
        expanded_nodes.clear()

        panel = html.Div(
            children=[
                html.H3("Tree reset"),
                html.P("Select a node or method to begin.")
            ]
        )

        return elements, panel, None, None

    # --------------------------------------------------
    # DROPDOWN SELECTED → AUTO-EXPAND + INFO
    # --------------------------------------------------
    if trigger == "method-name.value" and selected_method:
        elements = [
            {
                "data": {"id": "Exploratory Analysis", "label": "Exploratory\nAnalysis"},
                "position": {"x": 300, "y": 50}
            }
        ]
        expanded_nodes.clear()

        ancestors = get_ancestors(selected_method)[::-1]
        for n in ancestors:
            elements = toggle_node(n, elements)

        if selected_method in tree:
            elements = toggle_node(selected_method, elements)

        panel = build_info_panel(selected_method)

        return elements, panel, dash.no_update, dash.no_update

    # --------------------------------------------------
    # NODE CLICK → EXPAND / COLLAPSE
    # --------------------------------------------------
    if trigger == "cy.tapNodeData" and node:
        node_id = node["id"]
        elements = toggle_node(node_id, elements)

        panel = build_info_panel(node_id)
        return elements, panel, dash.no_update, dash.no_update

    raise dash.exceptions.PreventUpdate

# ========================================================================
# PART 8B — INFO PANEL BUTTONS
# ========================================================================

@app.callback(
    Output("content-panel", "children"),
    Input("btn-desc", "n_clicks"),
    Input("btn-interpret", "n_clicks"),
    Input("btn-limit", "n_clicks"),
    Input("btn-citation", "n_clicks"),
    Input("btn-image", "n_clicks"),
    Input("cy", "tapNodeData"),
    Input("method-name", "value")
)
def update_panel(desc, interpret, limit, citation, image, node, selected_method):
    node_id = None

    if node and node["id"] in node_details:
        node_id = node["id"]
    elif selected_method and selected_method in node_details:
        node_id = selected_method

    if not node_id:
        return ""

    d = node_details[node_id]
    ctx = dash.callback_context.triggered_id

    if ctx == "btn-desc" or ctx is None:
        return html.Pre(
            d.get("description", "No description available."),
            style={
                "whiteSpace": "pre-wrap",
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px",
                "lineHeight": "1.6"
            }
        )

    if ctx == "btn-interpret":
        return html.Pre(
            d.get("interpretation", "No interpretation available."),
            style={
                "whiteSpace": "pre-wrap",
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px",
                "lineHeight": "1.6"
            }
        )

    if ctx == "btn-limit":
        return html.Pre(
            d.get("limitations", "No limitations provided."),
            style={
                "whiteSpace": "pre-wrap",
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px",
                "lineHeight": "1.6"
            }
        )

    if ctx == "btn-image":
        return html.Img(
            src="/assets/" + d.get("image", ""),
            style={"width": "90%", "marginTop": "15px"}
        )

    if ctx == "btn-citation":
        return html.P(
            d.get("citation", "No citation available."),
            style={
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px"
            }
        )

    return html.Pre(
        d.get("description", ""),
        style={
            "whiteSpace": "pre-wrap",
            "fontFamily": "Times New Roman, Times, serif",
            "fontSize": "20px",
            "lineHeight": "1.6"
        }
    )

# ========================================================================
# PART 9 — THEME SWITCH CALLBACK
# ========================================================================

@app.callback(
    Output("cy", "stylesheet"),
    Output("cy", "style"),
    Output("page-container", "style"),
    Output("method-selector-box", "style"),
    Input("theme", "value"),
    Input("method-name", "value")
)
def theme_and_highlight(mode, selected_method):
    theme = LIGHT if mode == "light" else DARK

    stylesheet = [
        {
            "selector": "node",
            "style": {
                "content": "data(label)",
                "background-color": theme["node"],
                "color": theme["node_text"],
                "border-color": theme["border"],
                "border-width": 2,
                "white-space": "pre-wrap",
                "text-wrap": "wrap",
                "text-max-width": 160,
                "shape": "round-rectangle",
                "text-valign": "center",
                "text-halign": "center",
                "width": 180,
                "height": 80,
                "font-family": "Times New Roman, Times, serif",
                "font-size": "22px",
            }
        },
        {
            "selector": "edge",
            "style": {
                "line-color": theme["edge"],
                "width": 3
            }
        }
    ]

    selector_style = {
        "border": "1px solid #ccc",
        "borderRadius": "8px",
        "padding": "10px",
        "marginBottom": "10px",
        "backgroundColor": theme["cy_bg"],
        "color": theme["text"]
    }

    if selected_method:
        highlight_nodes = (
            [selected_method]
            + get_ancestors(selected_method)
            + get_descendants(selected_method)
        )

        stylesheet.append({"selector": "node", "style": {"opacity": 0.2}})
        stylesheet.append({"selector": "edge", "style": {"opacity": 0.1}})

        for n in highlight_nodes:
            stylesheet.append({
                "selector": f'node[id = "{n}"]',
                "style": {
                    "opacity": 1,
                    "border-width": 4,
                    "border-color": "#D55E00",
                    "background-color": "#FFE6D5"
                }
            })

            stylesheet.append({
                "selector": f'edge[source = "{n}"], edge[target = "{n}"]',
                "style": {
                    "opacity": 1,
                    "line-width": 4,
                    "line-color": "#D55E00"
                }
            })

    cy_style = {
        "width": "100%",
        "height": "500px",
        "backgroundColor": theme["cy_bg"]
    }

    page_style = {
        "backgroundColor": theme["page"],
        "color": theme["text"],
        "minHeight": "100vh",
        "padding": "20px",
        "fontFamily": "Times New Roman, Times, serif",
        "fontSize": "20px",
        "maxWidth": "1920px",
        "margin": "0 auto",
    }

    return stylesheet, cy_style, page_style, selector_style

# ========================================================================
# PART 10 — USER GUIDE TOGGLE
# ========================================================================

@app.callback(
    Output("guide-box", "children"),
    Output("guide-box", "style"),
    Input("toggle-guide", "n_clicks"),
    prevent_initial_call=True
)
def toggle_user_guide(n):
    if n % 2 == 1:
        return (
            html.Div(
                children=[
                    html.H3("User Guide"),
                    html.P("• Click nodes to expand or collapse the statistical decision tree."),
                    html.P("• Use the mouse scroll wheel to zoom in and out."),
                    html.P("• Use the Quick Method Selector to jump directly to a statistical test."),
                    html.P("• The information panel shows descriptions, interpretation, limitations, and references."),
                    html.P("• Use the Export button to download the currently visible tree.")
                ],
                style={
                    "border": "1px solid #ccc",
                    "padding": "15px",
                    "borderRadius": "6px",
                    "marginBottom": "15px",
                    "backgroundColor": "#f9f9f9"
                }
            ),
            {"display": "block"}
        )

    return "", {"display": "none"}

# ========================================================================
# PART 11 — EXPORT TREE
# ========================================================================

@app.callback(
    Output("cy", "generateImage"),
    Input("export-tree", "n_clicks"),
    prevent_initial_call=True
)
def export_tree(n):
    if not n:
        raise dash.exceptions.PreventUpdate

    return {
        "type": "png",
        "action": "download",
        "filename": "decision_tree"
    }

# ========================================================================
# PART 12 — METHOD SELECTOR DROPDOWN
# ========================================================================

@app.callback(
    Output("method-name", "options"),
    Input("method-group", "value")
)
def update_method_list(group):
    if not group:
        return []
    return [{"label": m.replace("\n", " "), "value": m} for m in METHOD_GROUPS[group]]

# ========================================================================
# PART 13 — RUN APP
# ========================================================================

if __name__ == "__main__":
    app.run(debug=True)
 



