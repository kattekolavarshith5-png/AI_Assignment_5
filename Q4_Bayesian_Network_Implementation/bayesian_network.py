"""
=============================================================================
QUESTION 4: Bayesian Networks – Tools, Modelling, and Inference
=============================================================================

WHAT IS A BAYESIAN NETWORK?
-----------------------------
A Bayesian Network (BN) is a probabilistic graphical model that represents
a set of variables and their conditional dependencies via a Directed Acyclic
Graph (DAG). Each node is a random variable; each directed edge encodes a
direct probabilistic influence. Each node carries a Conditional Probability
Table (CPT) that quantifies the effect of parent nodes.

KEY CONCEPTS:
  - Nodes: Random variables (discrete or continuous)
  - Edges: Direct causal or statistical dependence
  - CPT: P(Node | Parents) — the local probability distribution
  - DAG: Directed Acyclic Graph (no cycles allowed)
  - Inference: Computing P(Query | Evidence) using the BN

PYTHON TOOLS FOR BAYESIAN NETWORKS:
--------------------------------------
1. pgmpy       – Full-featured BN library: structure, CPTs, exact/approx inference
2. bnlearn     – Structure learning from data + visualisation (scikit-learn style)
3. pomegranate – Fast, scikit-compatible probabilistic models
4. PyMC        – Bayesian modelling with MCMC sampling (continuous variables)
5. BayesPy     – Variational Bayesian inference
6. Hugin/Netica– Commercial tools (not Python-native)

This script uses pgmpy (the most complete open-source Python BN library).

EXAMPLE CHOSEN: Medical Diagnosis – "Chest Disease" Network
------------------------------------------------------------
Classic BN from the AI literature. Variables:

  Asia (A)        → Did the patient visit Asia recently?
  Smoking (S)     → Is the patient a smoker?
  Tuberculosis (T)→ Does the patient have tuberculosis? (influenced by Asia)
  LungCancer (L)  → Does the patient have lung cancer? (influenced by Smoking)
  Bronchitis (B)  → Does the patient have bronchitis? (influenced by Smoking)
  Either (E)      → Has either T or L? (T-L combination node)
  XRay (X)        → Is the chest X-ray abnormal? (influenced by Either)
  Dyspnea (D)     → Does the patient have shortness of breath? (E + B)

DAG:  A→T, S→L, S→B, T→E, L→E, E→X, E→D, B→D
=============================================================================
"""

from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination, BeliefPropagation
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import networkx as nx
import warnings
warnings.filterwarnings("ignore")

print("=" * 65)
print("  BAYESIAN NETWORKS – MEDICAL DIAGNOSIS EXAMPLE")
print("=" * 65)

# ─────────────────────────────────────────────────────────────
# STEP 1: Define the DAG Structure
# ─────────────────────────────────────────────────────────────
print("\n─── STEP 1: Define the DAG ─────────────────────────────────────")

model = BayesianNetwork([
    ("Asia",    "Tuberculosis"),
    ("Smoking", "LungCancer"),
    ("Smoking", "Bronchitis"),
    ("Tuberculosis", "Either"),
    ("LungCancer",   "Either"),
    ("Either",  "XRay"),
    ("Either",  "Dyspnea"),
    ("Bronchitis",   "Dyspnea"),
])

print("DAG Edges (causal structure):")
for u, v in model.edges():
    print(f"   {u} → {v}")

print(f"\nNodes : {list(model.nodes())}")
print(f"Edges : {model.number_of_edges()}")

# ─────────────────────────────────────────────────────────────
# STEP 2: Define Conditional Probability Tables (CPTs)
# ─────────────────────────────────────────────────────────────
print("\n─── STEP 2: Specify CPTs ───────────────────────────────────────")
print("Each node gets a Conditional Probability Table P(Node|Parents).\n")

# P(Asia): Prior — visiting Asia is uncommon
cpd_asia = TabularCPD(
    variable="Asia", variable_card=2,
    values=[[0.99], [0.01]],   # [No, Yes]
    state_names={"Asia": ["No", "Yes"]}
)

# P(Smoking): Prior — 50% chance the patient smokes
cpd_smoking = TabularCPD(
    variable="Smoking", variable_card=2,
    values=[[0.50], [0.50]],
    state_names={"Smoking": ["No", "Yes"]}
)

# P(Tuberculosis | Asia)
#           Asia=No  Asia=Yes
# T=No       0.99     0.95
# T=Yes      0.01     0.05
cpd_tb = TabularCPD(
    variable="Tuberculosis", variable_card=2,
    values=[[0.99, 0.95],
            [0.01, 0.05]],
    evidence=["Asia"], evidence_card=[2],
    state_names={"Tuberculosis": ["No", "Yes"], "Asia": ["No", "Yes"]}
)

# P(LungCancer | Smoking)
#              S=No  S=Yes
# LC=No        0.99   0.90
# LC=Yes       0.01   0.10
cpd_lc = TabularCPD(
    variable="LungCancer", variable_card=2,
    values=[[0.99, 0.90],
            [0.01, 0.10]],
    evidence=["Smoking"], evidence_card=[2],
    state_names={"LungCancer": ["No", "Yes"], "Smoking": ["No", "Yes"]}
)

# P(Bronchitis | Smoking)
#              S=No  S=Yes
# B=No         0.70   0.40
# B=Yes        0.30   0.60
cpd_bron = TabularCPD(
    variable="Bronchitis", variable_card=2,
    values=[[0.70, 0.40],
            [0.30, 0.60]],
    evidence=["Smoking"], evidence_card=[2],
    state_names={"Bronchitis": ["No", "Yes"], "Smoking": ["No", "Yes"]}
)

# P(Either | Tuberculosis, LungCancer)
# E=Yes if T=Yes OR L=Yes (noisy-OR like)
#           T=No,L=No  T=No,L=Yes  T=Yes,L=No  T=Yes,L=Yes
# E=No       1.0         0.0         0.0          0.0
# E=Yes      0.0         1.0         1.0          1.0
cpd_either = TabularCPD(
    variable="Either", variable_card=2,
    values=[[1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 1.0, 1.0]],
    evidence=["Tuberculosis", "LungCancer"], evidence_card=[2, 2],
    state_names={
        "Either": ["No", "Yes"],
        "Tuberculosis": ["No", "Yes"],
        "LungCancer": ["No", "Yes"]
    }
)

# P(XRay | Either)
#              E=No  E=Yes
# X=No         0.95   0.02
# X=Yes        0.05   0.98
cpd_xray = TabularCPD(
    variable="XRay", variable_card=2,
    values=[[0.95, 0.02],
            [0.05, 0.98]],
    evidence=["Either"], evidence_card=[2],
    state_names={"XRay": ["Normal", "Abnormal"], "Either": ["No", "Yes"]}
)

# P(Dyspnea | Either, Bronchitis)
#           E=No,B=No  E=No,B=Yes  E=Yes,B=No  E=Yes,B=Yes
# D=No       0.90        0.30        0.20         0.10
# D=Yes      0.10        0.70        0.80         0.90
cpd_dysp = TabularCPD(
    variable="Dyspnea", variable_card=2,
    values=[[0.90, 0.30, 0.20, 0.10],
            [0.10, 0.70, 0.80, 0.90]],
    evidence=["Either", "Bronchitis"], evidence_card=[2, 2],
    state_names={
        "Dyspnea": ["No", "Yes"],
        "Either": ["No", "Yes"],
        "Bronchitis": ["No", "Yes"]
    }
)

# Attach all CPTs to the model
model.add_cpds(cpd_asia, cpd_smoking, cpd_tb, cpd_lc,
               cpd_bron, cpd_either, cpd_xray, cpd_dysp)

# Validate the model
is_valid = model.check_model()
print(f"Model validation: {'✓ PASSED' if is_valid else '✗ FAILED'}")

# Print CPT summary
print("\nCPT Summary:")
for cpd in model.cpds:
    parents = cpd.variables[1:]
    parent_str = f"| {', '.join(parents)}" if parents else "(prior)"
    print(f"   P({cpd.variable} {parent_str})")


# ─────────────────────────────────────────────────────────────
# STEP 3: Exact Inference — Variable Elimination
# ─────────────────────────────────────────────────────────────
print("\n─── STEP 3: Inference — Variable Elimination ──────────────────")
print("Variable Elimination computes exact posterior probabilities.\n")

ve = VariableElimination(model)

# ── Query 1: Prior probability of Dyspnea (no evidence) ──
q1 = ve.query(variables=["Dyspnea"])
print("Query 1 – P(Dyspnea) [no evidence]:")
p_dysp_yes = q1.values[1]
p_dysp_no  = q1.values[0]
print(f"   P(Dyspnea=No)  = {p_dysp_no:.4f}")
print(f"   P(Dyspnea=Yes) = {p_dysp_yes:.4f}")

# ── Query 2: P(LungCancer | Dyspnea=Yes, Smoking=Yes) ──
q2 = ve.query(
    variables=["LungCancer"],
    evidence={"Dyspnea": "Yes", "Smoking": "Yes"}
)
print("\nQuery 2 – P(LungCancer | Dyspnea=Yes, Smoking=Yes):")
print(f"   P(LungCancer=No)  = {q2.values[0]:.4f}")
print(f"   P(LungCancer=Yes) = {q2.values[1]:.4f}")

# ── Query 3: P(Tuberculosis | Asia=Yes, XRay=Abnormal) ──
q3 = ve.query(
    variables=["Tuberculosis"],
    evidence={"Asia": "Yes", "XRay": "Abnormal"}
)
print("\nQuery 3 – P(Tuberculosis | Asia=Yes, XRay=Abnormal):")
print(f"   P(Tuberculosis=No)  = {q3.values[0]:.4f}")
print(f"   P(Tuberculosis=Yes) = {q3.values[1]:.4f}")

# ── Query 4: Most likely cause of dyspnea (MAP) ──
print("\nQuery 4 – MAP: Most probable explanation for (Dyspnea=Yes, XRay=Abnormal):")
map_result = ve.map_query(
    variables=["Tuberculosis", "LungCancer", "Bronchitis"],
    evidence={"Dyspnea": "Yes", "XRay": "Abnormal"}
)
for var, state in map_result.items():
    print(f"   {var} = {state}")

# ── Query 5: Effect of Smoking on multiple outcomes ──
print("\nQuery 5 – Smoking's causal effect on outcomes:")
outcomes = ["LungCancer", "Bronchitis", "Dyspnea"]
for smoking_state in ["No", "Yes"]:
    print(f"\n   Given Smoking={smoking_state}:")
    for outcome in outcomes:
        q = ve.query(variables=[outcome], evidence={"Smoking": smoking_state})
        print(f"     P({outcome}=Yes | Smoking={smoking_state}) = {q.values[1]:.4f}")


# ─────────────────────────────────────────────────────────────
# STEP 4: Approximate Inference — Belief Propagation
# ─────────────────────────────────────────────────────────────
print("\n─── STEP 4: Belief Propagation (Approximate Inference) ────────")
print("Belief Propagation passes messages along the graph.\n")

bp = BeliefPropagation(model)
bp.calibrate()

# Compare VE vs BP on a query
q_ve = ve.query(variables=["LungCancer"],
                evidence={"Smoking": "Yes", "Dyspnea": "Yes"})
q_bp = bp.query(variables=["LungCancer"],
                evidence={"Smoking": "Yes", "Dyspnea": "Yes"})

print("Comparison — P(LungCancer | Smoking=Yes, Dyspnea=Yes):")
print(f"   Variable Elimination : P(Yes) = {q_ve.values[1]:.4f}")
print(f"   Belief Propagation   : P(Yes) = {q_bp.values[1]:.4f}")
print(f"   Difference           : {abs(q_ve.values[1] - q_bp.values[1]):.6f}")


# ─────────────────────────────────────────────────────────────
# STEP 5: Visualisation
# ─────────────────────────────────────────────────────────────
print("\n─── STEP 5: Visualisation ──────────────────────────────────────")

fig, axes = plt.subplots(1, 2, figsize=(18, 9))
fig.patch.set_facecolor("#0d1117")

# ── Plot 1: DAG Structure ──
ax1 = axes[0]
ax1.set_facecolor("#0d1117")

G_dag = nx.DiGraph(model.edges())
pos = {
    "Asia":          (0.2, 0.9),
    "Smoking":       (0.8, 0.9),
    "Tuberculosis":  (0.2, 0.65),
    "LungCancer":    (0.65, 0.65),
    "Bronchitis":    (0.95, 0.65),
    "Either":        (0.42, 0.42),
    "XRay":          (0.25, 0.18),
    "Dyspnea":       (0.65, 0.18),
}

node_groups = {
    "Asia": "#4ecdc4", "Smoking": "#ff6b6b",
    "Tuberculosis": "#ffd93d", "LungCancer": "#ff9a3c",
    "Bronchitis": "#c77dff", "Either": "#6bcb77",
    "XRay": "#45b7d1", "Dyspnea": "#f9c74f",
}
node_colors = [node_groups[n] for n in G_dag.nodes]

nx.draw_networkx_nodes(G_dag, pos, node_color=node_colors, node_size=2200,
                       alpha=0.9, ax=ax1)
nx.draw_networkx_labels(G_dag, pos, font_size=8, font_color="#111",
                        font_weight="bold", ax=ax1)
nx.draw_networkx_edges(G_dag, pos, edge_color="#8888bb", arrows=True,
                       arrowsize=22, width=2.0,
                       connectionstyle="arc3,rad=0.08", ax=ax1)

# Annotate node types
type_labels = {
    "Asia": "Risk Factor", "Smoking": "Risk Factor",
    "Tuberculosis": "Disease", "LungCancer": "Disease",
    "Bronchitis": "Disease", "Either": "Intermediate",
    "XRay": "Observable", "Dyspnea": "Symptom",
}
for node, (x, y) in pos.items():
    ax1.text(x, y - 0.065, type_labels[node], ha='center', fontsize=6,
             color="#aaaacc", transform=ax1.transAxes,
             bbox=dict(boxstyle="round,pad=0.2", fc="#1a1a2e", ec="none", alpha=0.7))

ax1.set_title("Chest Disease Bayesian Network – DAG",
              color="white", fontsize=13, fontweight="bold", pad=10)
ax1.axis("off")

# ── Plot 2: Inference Results Bar Chart ──
ax2 = axes[1]
ax2.set_facecolor("#0d1117")

scenarios = [
    ("Prior\nP(LungCancer)",       ve.query(["LungCancer"]).values[1]),
    ("P(LC|Smoking=Yes)",          ve.query(["LungCancer"], {"Smoking":"Yes"}).values[1]),
    ("P(LC|Smoke+Dyspnea)",        ve.query(["LungCancer"], {"Smoking":"Yes","Dyspnea":"Yes"}).values[1]),
    ("P(LC|Smoke+Dysp+XRay)",      ve.query(["LungCancer"], {"Smoking":"Yes","Dyspnea":"Yes","XRay":"Abnormal"}).values[1]),
    ("Prior\nP(Tuberculosis)",     ve.query(["Tuberculosis"]).values[1]),
    ("P(TB|Asia=Yes)",             ve.query(["Tuberculosis"], {"Asia":"Yes"}).values[1]),
    ("P(TB|Asia+XRay=Abnormal)",   ve.query(["Tuberculosis"], {"Asia":"Yes","XRay":"Abnormal"}).values[1]),
]

labels = [s[0] for s in scenarios]
values = [s[1] for s in scenarios]
colors = ["#ff9a3c"]*4 + ["#ffd93d"]*3

bars = ax2.bar(range(len(labels)), values, color=colors, alpha=0.85,
               edgecolor="#333", linewidth=0.8)

for bar, val in zip(bars, values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f"{val:.3f}", ha="center", va="bottom",
             fontsize=8.5, color="white", fontweight="bold")

ax2.set_xticks(range(len(labels)))
ax2.set_xticklabels(labels, rotation=30, ha="right", fontsize=7.5, color="#ccccee")
ax2.set_ylabel("Probability", color="#ccccee", fontsize=10)
ax2.set_ylim(0, 1.0)
ax2.set_title("Posterior Probabilities – Variable Elimination Queries",
              color="white", fontsize=12, fontweight="bold", pad=10)
ax2.tick_params(colors="#aaaaaa")
for spine in ax2.spines.values():
    spine.set_edgecolor("#333344")
ax2.set_facecolor("#0d1117")
ax2.yaxis.label.set_color("#aaaacc")
ax2.tick_params(axis='y', colors="#aaaacc")
ax2.grid(axis='y', color="#222233", linewidth=0.8, alpha=0.6)

# Legend
lc_patch = mpatches.Patch(color="#ff9a3c", label="Lung Cancer queries")
tb_patch = mpatches.Patch(color="#ffd93d", label="Tuberculosis queries")
ax2.legend(handles=[lc_patch, tb_patch], facecolor="#1a1a2e",
           edgecolor="#555", labelcolor="white", fontsize=9)

plt.tight_layout(pad=2.5)
plt.savefig("q2_bayesian_network.png", dpi=150,
            bbox_inches="tight", facecolor="#0d1117")
plt.close()
print("[pgmpy] DAG + Inference chart saved → q2_bayesian_network.png")


# ─────────────────────────────────────────────────────────────
# STEP 6: d-Separation (Conditional Independence Checks)
# ─────────────────────────────────────────────────────────────
print("\n─── STEP 6: d-Separation (Conditional Independence) ───────────")
print("d-Separation determines which variables are conditionally")
print("independent given a set of observed variables.\n")

checks = [
    ("Asia",   "Smoking",    set()),
    ("Asia",   "LungCancer", set()),
    ("Asia",   "LungCancer", {"Either"}),
    ("Asia",   "Smoking",    {"Either"}),
    ("Tuberculosis", "LungCancer", set()),
    ("Tuberculosis", "LungCancer", {"Either"}),
]
for x, y, z in checks:
    z_str = f"{{ {', '.join(z)} }}" if z else "∅"
    sep = model.local_independencies(x)
    # Use active_trail_nodes for d-separation
    active = model.active_trail_nodes([x], observed=list(z))
    is_indep = y not in active[x]
    print(f"   d-sep({x} ⊥ {y} | {z_str}) : {'INDEPENDENT' if is_indep else 'DEPENDENT'}")


# ─────────────────────────────────────────────────────────────
# STEP 7: Tools Summary
# ─────────────────────────────────────────────────────────────
print("\n─── STEP 7: BN Python Tools Comparison ────────────────────────")
bn_tools = [
    ("pgmpy",       "Discrete BNs; structure learning; VE & BP inference",  "Teaching, research, exact inference"),
    ("bnlearn",     "Structure learning from data; sklearn-style API",        "Data-driven structure discovery"),
    ("pomegranate", "Fast; continuous + discrete; HMMs; GPU support",         "High-performance applications"),
    ("PyMC",        "MCMC sampling; continuous; Bayesian regression",         "Bayesian statistics & ML"),
    ("BayesPy",     "Variational Bayesian inference; large models",           "Scalable approximate inference"),
    ("Hugin",       "Commercial; decision networks; GUI + Python API",         "Enterprise / medical decision support"),
]
print(f"\n{'Tool':<14} {'Strength':<50} {'Best For'}")
print("─" * 90)
for tool, strength, best in bn_tools:
    print(f"{tool:<14} {strength:<50} {best}")

print("\n" + "=" * 65)
print("  Q2 Complete. Output: q2_bayesian_network.png")
print("=" * 65)
