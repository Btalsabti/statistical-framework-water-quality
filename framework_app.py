# To enter the .venv type [ source .venv/bin/activate ] in the terminal and bash
# to # multiple lines click (cmd+/) while highliting the lines 
# ========================================================================
#  FRAMEWORK APP — INTERACTIVE COLLAPSIBLE DECISION TREE (DASH)
#  Prepared for scientific publication + extendable by the author.
#  *** EVERY SECTION IS EXPLAINED SO YOU CAN MODIFY IT EASILY ***
# ========================================================================

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


# ==========================================
# Statistical method legend (navigation only)
# ==========================================
METHOD_GROUPS = {
    "Univariate": [
        "Shapiro–Wilk",
        "Kolmogorov–\nSmirnov",
        "Q–Q Plot",
        "Histogram"
    ],
    "Bivariate": [
        "Pearson's correlation",
        "Spearman's correlation"
    ],
    "Multivariate": [
        "Principal Component\nAnalysis",
        "Factor Analysis",
        "Hierarchical\nCluster Analysis",
        "PMF"
    ]
}

# ==========================================
# Legend panel
# ==========================================
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
        "interpretation": (
            "• p < 0.05 → data significantly deviates from normality\n"
            "• p ≥ 0.05 → normality cannot be rejected\n"
        ),
        "limitations": (
            "• Very sensitive to outliers\n"
            "• Not suitable for large samples (n > 2000)\n"
            "• Assumes continuous data\n"
        ),
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
        "interpretation": (
            "• Measures the maximum difference between empirical and theoretical CDF\n"
            "• p < 0.05 → distribution differs significantly from the normal distribution\n"
            "• Works for medium to large samples\n"
        ),
        "limitations": (
            "• Low power for small samples\n"
            "• Assumes parameters of reference distribution known (unless corrected)\n"
            "• Less sensitive than Shapiro–Wilk for tail deviations\n"
        ),
        "formula": (
        r"D = \max_x |F_n(x) - F(x)|",
         ),
        "citation": "Kolmogorov (1933); Smirnov (1939).",
        "image": "ks_test.png"
    },
    # --------------------------------------------------------------------
    # EXAMPLE 2 — Q-Q PLOT
    # --------------------------------------------------------------------
    "Q–Q Plot": {
        "description": "A graphical method to check if data follows a normal distribution.",
        "interpretation": (
            "• Points on a straight line → normality holds\n"
            "• S-shaped curve → skewness present\n"
            "• Deviations at ends → heavy or light tails\n"
        ),
        "limitations": (
            "• Subjective assessment\n"
            "• Hard to interpret with very large datasets\n"
            "• Outliers strongly influence the visual appearance\n"
        ),
        "formula": "No formula (graphical method).",
        "rules": ["Look for deviations in tails", "S-shape → skewness"],
        "example": "Example: upward deviation in right tail → right skew.",
        "citation": "Wilk & Gnanadesikan (1968). Biometrika.",
        "image": "qqplot.png"
    },

    # --------------------------------------------------------------------
    # EXAMPLE 3 — HISTOGRAM
    # --------------------------------------------------------------------
    "Histogram": {
        "description": "Basic visual distribution check.",
    "interpretation": (
        "• Bell-shaped curve → suggests normality\n"
        "• Skewed or multi-modal shapes → deviations from normality\n"
    ),
    "limitations": (
        "• Highly sensitive to bin size\n"
        "• Only a visual guide, not a formal statistical test\n"
    ),
        "formula": "No formula.",
        "rules": ["Bin size affects interpretation", "Used for quick inspection"],
        "example": "Example: uneven shape → skewness.",
        "citation": "Cleveland (1985). The Elements of Graphing Data.",
        "image": "histogram.png"
    },


  # EXAMPLE 3 — Box-plot
# "interpretation": (
#     "• Symmetric box and whiskers → approximate normality\n"
#     "• Long whisker → skewness\n"
#     "• Outliers appear as individual points\n"
# ),
# "limitations": (
#     "• Does not show distribution shape\n"
#     "• Cannot confirm normality alone\n"
# ),


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
    "interpretation": (
        "• Linear pattern in ordered Mahalanobis distances → multivariate normality likely\n"
        "• Curved pattern → deviation from multivariate normality\n"
    ),
    "limitations": (
        "• Requires stable estimation of covariance matrix\n"
        "• Sensitive to outliers and high-dimensionality\n"
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
    "interpretation": (
    "• Points on diagonal line → data follows multivariate normality\n"
    "• Systematic deviations → skewness, kurtosis, or correlation structure issues\n"
    ),
    "limitations": (
        "• Depends heavily on reliable covariance estimation\n"
        "• Outliers distort the plot drastically\n"
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
    "interpretation": (
    "• Close fit to diagonal → supports multivariate normal assumption\n"
    "• Deviations at upper tail → heavy tails or multivariate outliers\n"
    ),
    "limitations": (
        "• Requires adequate sample size relative to dimensionality\n"
        "• Visual method — subjective interpretation\n"
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
    "interpretation": (
    "• High b₁ₚ value → significant multivariate skewness\n"
    "• p < 0.05 → reject multivariate normality\n"
    ),
    "limitations": (
        "• Very sensitive to outliers\n"
        "• Requires invertible covariance matrix\n"
        "• Not reliable for small sample sizes\n"
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
    "interpretation": (
    "• b₂ₚ > expected value → heavy tails\n"
    "• b₂ₚ < expected value → light tails\n"
    "• Significant deviation → reject multivariate normality\n"
    ),
    "limitations": (
        "• Sensitive to deviations in higher-order moments\n"
        "• Requires adequate sample size (n > p)\n"
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
    "interpretation": (
    "• r close to +1 → strong positive linear relationship\n"
    "• r close to -1 → strong negative linear relationship\n"
    "• r ≈ 0 → no linear relationship\n"
    "• p-value tests whether the linear relationship is statistically significant\n"
    ),
    "limitations": (
        "• Only detects linear relationships\n"
        "• Highly sensitive to outliers\n"
        "• Requires variables to be approximately normal\n"
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
    "interpretation": (
    "• ρ close to +1 or -1 → strong monotonic relationship\n"
    "• ρ ≈ 0 → no monotonic relationship\n"
    "• Works for non-normal and ordinal data\n"
    ),
    "limitations": (
        "• Does not detect non-monotonic nonlinear patterns\n"
        "• Ties in ranked data reduce precision\n"
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
        "interpretation": (
            "• High loadings indicate strong influence of variables on components\n"
            "• PC1 explains the largest variance in the dataset\n"
        ),
        "limitations": (
            "• Only captures linear structure\n"
            "• Sensitive to variable scaling\n"
            "• Sensitive to outliers\n"),
        "formula": r"Z = XW \quad \text{(eigenvectors of covariance matrix)}",
        "citation": "Jolliffe (2002). Principal Component Analysis.",
        "image": "pca.png"
    },

    "Factor Analysis": {
        "description": "Factor Analysis (FA) models latent variables that explain observed correlations.\n\n"
                       "When to use:\n"
                       "• You want to identify underlying factors\n"
                       "• Shared variance is more important than total variance",
        "interpretation": (
            "• Factors represent latent constructs underlying correlations\n"
            "• High communalities → variables well explained\n"
        ),
        "limitations": (
            "• Requires large sample size (often n > 100)\n"
            "• Factor rotation introduces subjectivity\n"
            "• Model fit can be poor if data violate assumptions\n"
        ),
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
        "interpretation": (
            "• Positive or negative discriminant scores indicate group separation\n"
            "• Classification accuracy indicates predictive performance\n"
        ),
        "limitations": (
            "• Assumes multivariate normality of predictors\n"
            "• Classes must have similar covariance matrices\n"
            "• Sensitive to outliers\n"
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
        "interpretation": (
            "• Dendrogram shows group structure\n"
            "• Height of fusion → cluster similarity\n"
        ),
        "limitations": (
            "• Sensitive to scaling of variables\n"
            "• Different linkage methods can give different results\n"
            "• Cannot revise earlier merge decisions\n"
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
        "interpretation": (
            "• Factors represent source profiles\n"
            "• Contribution values indicate source strengths over samples\n"
        ),
        "limitations": (
            "• Factor number selection subjective\n"
            "• Rotational ambiguity affects stability\n"
            "• Requires accurate uncertainty estimates\n"
            "• Sensitive to collinearity in species data\n"
        ),
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
    if parent_pos is None:
        # Parent not yet rendered → skip expansion safely
        return current_elements

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
# HELPER FUNCTIONS FOR TREE NAVIGATION
# ========================================================================

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

        # ---------------- MathJax Support ----------------
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

        # ---------------- Title ----------------
        html.H1("📊 Statistical Framework for Water Quality Assessment"),

        # ---------------- User Guide Button ----------------
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
        ),  # ← COMMA FIXED HERE


        # ---------------- Theme selector + Reset ----------------
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

        # ---------------- Split Screen ----------------
        html.Div(
            style={
                "display": "flex",
                "flexDirection": "row",
                "width": "100%",
                "height": "600px",
                "marginTop": "20px"
            },
            children=[

                # -------- LEFT: TREE --------
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

                # -------- RIGHT: INFO PANEL --------
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

                        # Dynamic info content (filled by callbacks)
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

        # ---------------- Footer ----------------
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
# ========================================================================
# PART 7 — CLICK / DROPDOWN AUTO-FOCUS / RESET TREE
# ========================================================================
# ========================================================================
# PART 7 — CLICK / DROPDOWN AUTO-FOCUS / RESET TREE (+ keep dropdown state)
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

# ==================================================
# CASE 0 — RESET TREE (clear both dropdowns)
# ==================================================
    if trigger == "reset-tree.n_clicks":

        elements = [
            {"data": {"id": "root", "label": "Statistical\nDecision Tree"},
            "position": {"x": 300, "y": 50}}
        ]

        expanded_nodes.clear()

        panel = html.Div(
            children=[
                html.H3("Tree reset"),
                html.P("Select a node or method to begin.")
            ]
        )

        return (
            elements,
            panel,
            None,   # clear method-name
            None    # clear method-group
        )
    # ==================================================
    # CASE 1 — DROPDOWN SELECTED → AUTO-EXPAND + AUTO INFO
    # ==================================================
    if trigger == "method-name.value" and selected_method:

        # Reset tree structure
        elements = [
            {"data": {"id": "root", "label": "Statistical\nDecision Tree"},
            "position": {"x": 300, "y": 50}}
        ]
        expanded_nodes.clear()

        # Expand valid ancestors only (top → down)
        ancestors = get_ancestors(selected_method)[::-1]
        for n in ancestors:
            elements = toggle_node(n, elements)

        # Expand selected method node
        elements = toggle_node(selected_method, elements)

        # Auto-open info panel if available
        if selected_method in node_details:
            d = node_details[selected_method]

            panel = html.Div(
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
        else:
            panel = html.H3(f"Focused on: {selected_method}")

        return elements, panel, dash.no_update, dash.no_update
    # ==================================================
    # CASE 2 — NODE CLICK → NORMAL EXPAND / COLLAPSE
    # (DO NOT modify dropdowns)
    # ==================================================
    if trigger == "cy.tapNodeData" and node:
        node_id = node["id"]
        elements = toggle_node(node_id, elements)

        if node_id not in node_details:
            return elements, html.H3(f"You selected: {node_id}"), dash.no_update, dash.no_update

        d = node_details[node_id]
        panel = html.Div(
            children=[
                html.Div(
                    children=[
                        html.Button("📘 Description", id="btn-desc", n_clicks=1,
                                    style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),
                        html.Button("🔍 Interpretation", id="btn-interpret", n_clicks=0,
                                    style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),
                        html.Button("⚠️ Limitations", id="btn-limit", n_clicks=0,
                                    style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),
                        html.Button("🖼 Image", id="btn-image", n_clicks=0,
                                    style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),
                        html.Button("📚 Citation", id="btn-citation", n_clicks=0,
                                    style={"marginBottom": "10px", "width": "100%", "fontSize": "18px"}),
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

        return elements, panel, dash.no_update, dash.no_update

    raise dash.exceptions.PreventUpdate
# ========================================================================
# PART 7B — INFO PANEL
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

    # ---------------- DESCRIPTION -----------------
    if ctx == "btn-desc":
        return html.Pre(
            d.get("description", "No description available."),
            style={
                "whiteSpace": "pre-wrap",
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px",
                "lineHeight": "1.6"
            }
        )

    # ---------------- INTERPRETATION -----------------
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

    # ---------------- LIMITATIONS -----------------
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

    # ---------------- IMAGE -----------------
    if ctx == "btn-image":
        return html.Img(
            src="/assets/" + d.get("image", ""),
            style={"width": "90%", "marginTop": "15px"}
        )

    # ---------------- CITATION -----------------
    if ctx == "btn-citation":
        return html.P(
            d.get("citation", "No citation available."),
            style={
                "fontFamily": "Times New Roman, Times, serif",
                "fontSize": "20px"
            }
        )

    # Default fallback
    return html.Pre(
        d.get("description", ""),
        style={"whiteSpace": "pre-wrap"}
    )
# ========================================================================
# PART 8 — THEME SWITCH CALLBACK
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
        {"selector": "edge", "style": {"line-color": theme["edge"], "width": 3}}
    ]

    # -------- Quick selector style --------
    selector_style = {
        "border": "1px solid #ccc",
        "borderRadius": "8px",
        "padding": "10px",
        "marginBottom": "10px",
        "backgroundColor": theme["cy_bg"],
        "color": theme["text"]
    }

    # -------- Highlight subtree --------
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
# USER GUIDE TOGGLE
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
# EXPORT SELECTED TREE (PNG)
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
# Method selector
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
# PART 9 — RUN APP
# ========================================================================
if __name__ == "__main__":
    app.run(debug=True)
 



