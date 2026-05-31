"""
=============================================================================
QUESTION 1: Knowledge Graphs – Description & Python Tools
=============================================================================

WHAT IS A KNOWLEDGE GRAPH?
---------------------------
A Knowledge Graph (KG) is a structured representation of real-world entities
and the relationships between them. It stores information as a graph where:
  - NODES (vertices) represent entities (people, places, concepts, events)
  - EDGES represent relationships (directed links between entities)
  - PROPERTIES/ATTRIBUTES annotate nodes and edges with metadata

Knowledge Graphs underpin major AI systems:
  - Google Knowledge Graph (powers search results)
  - Facebook's Social Graph
  - Amazon Product Graph
  - Wikidata / DBpedia (open knowledge bases)

KEY CONCEPTS:
  - Triple Store: (Subject, Predicate, Object) → e.g., (Einstein, bornIn, Germany)
  - Ontology: Formal schema defining classes, relationships, and constraints
  - RDF (Resource Description Framework): W3C standard for encoding triples
  - SPARQL: Query language for RDF/KG stores
  - OWL (Web Ontology Language): Richer ontology language with inference rules

PYTHON TOOLS FOR BUILDING KNOWLEDGE GRAPHS:
--------------------------------------------
1. NetworkX       – General-purpose graph library; great for KG construction/traversal
2. RDFLib         – Python RDF/OWL library; supports SPARQL queries and serialization
3. PyVis          – Interactive KG visualisation in HTML
4. Owlready2      – OWL ontology loading and reasoning
5. Neo4j (py2neo) – Property graph database backend
6. GraphDB        – Enterprise triple store (SPARQL endpoint)

This script demonstrates Tools 1, 2, and 3 with a self-contained example.
=============================================================================
"""

# ─────────────────────────────────────────────────────────────
# TOOL 1: NetworkX — Build and Query a KG as a Directed Graph
# ─────────────────────────────────────────────────────────────
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

print("=" * 65)
print("  KNOWLEDGE GRAPHS – PYTHON IMPLEMENTATION")
print("=" * 65)

print("\n─── TOOL 1: NetworkX ──────────────────────────────────────────")
print("NetworkX models a KG as a directed multi-graph.")
print("Each edge carries a 'relation' attribute (the predicate).\n")

# Build the KG: domain = Academic World
G = nx.MultiDiGraph()

# --- Nodes (Entities) ---
entities = {
    "Alan Turing":       {"type": "Person",       "born": 1912, "field": "Computer Science"},
    "John McCarthy":     {"type": "Person",       "born": 1927, "field": "AI"},
    "Marvin Minsky":     {"type": "Person",       "born": 1927, "field": "AI"},
    "MIT":               {"type": "University",   "location": "Cambridge, MA"},
    "Stanford":          {"type": "University",   "location": "Stanford, CA"},
    "Cambridge":         {"type": "University",   "location": "Cambridge, UK"},
    "Turing Award":      {"type": "Award",        "field": "Computing"},
    "Artificial Intelligence": {"type": "Field"},
    "Machine Learning":  {"type": "Field"},
    "Neural Networks":   {"type": "Field"},
    "LISP":              {"type": "ProgrammingLanguage"},
    "Perceptron":        {"type": "Concept"},
}
G.add_nodes_from(entities.items())

# --- Edges (Triples: Subject → Predicate → Object) ---
triples = [
    ("Alan Turing",   "studiedAt",    "Cambridge"),
    ("Alan Turing",   "pioneered",    "Artificial Intelligence"),
    ("Alan Turing",   "pioneered",    "Machine Learning"),
    ("John McCarthy", "workedAt",     "MIT"),
    ("John McCarthy", "workedAt",     "Stanford"),
    ("John McCarthy", "invented",     "LISP"),
    ("John McCarthy", "pioneered",    "Artificial Intelligence"),
    ("John McCarthy", "won",          "Turing Award"),
    ("Marvin Minsky", "workedAt",     "MIT"),
    ("Marvin Minsky", "pioneered",    "Neural Networks"),
    ("Marvin Minsky", "pioneered",    "Artificial Intelligence"),
    ("Marvin Minsky", "won",          "Turing Award"),
    ("Neural Networks", "subFieldOf", "Artificial Intelligence"),
    ("Machine Learning","subFieldOf", "Artificial Intelligence"),
    ("Machine Learning","uses",       "Neural Networks"),
    ("Perceptron",    "conceptIn",    "Neural Networks"),
    ("Marvin Minsky", "invented",     "Perceptron"),
]
for subj, pred, obj in triples:
    G.add_edge(subj, obj, relation=pred)

print(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges\n")

# ── KG Query 1: Who worked at MIT? ──
print("Query 1 – Who worked at MIT?")
mit_workers = [u for u, v, d in G.edges(data=True)
               if v == "MIT" and d["relation"] == "workedAt"]
for w in mit_workers:
    print(f"   → {w}")

# ── KG Query 2: What did John McCarthy contribute? ──
print("\nQuery 2 – What did John McCarthy do?")
for u, v, d in G.edges("John McCarthy", data=True):
    print(f"   John McCarthy --[{d['relation']}]--> {v}")

# ── KG Query 3: Multi-hop – who pioneered a subfield of AI? ──
print("\nQuery 3 – Multi-hop: who pioneered a sub-field of Artificial Intelligence?")
subfields = [u for u, v, d in G.edges(data=True)
             if v == "Artificial Intelligence" and d["relation"] == "subFieldOf"]
for sf in subfields:
    pioneers = [u for u, v, d in G.edges(data=True)
                if v == sf and d["relation"] == "pioneered"]
    for p in pioneers:
        print(f"   {p} --[pioneered]--> {sf} --[subFieldOf]--> Artificial Intelligence")

# ── KG Statistics ──
print("\nKG Statistics:")
print(f"   Nodes : {G.number_of_nodes()}")
print(f"   Edges : {G.number_of_edges()}")
print(f"   Most connected entity: "
      f"{max(G.nodes, key=lambda n: G.degree(n))} "
      f"(degree {max(dict(G.degree()).values())})")

# ── Visualise with matplotlib ──
fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor("#0f0f1a")
ax.set_facecolor("#0f0f1a")

pos = nx.spring_layout(G, seed=42, k=2.5)

# Colour by entity type
type_colors = {
    "Person":              "#ff6b6b",
    "University":          "#4ecdc4",
    "Award":               "#ffd93d",
    "Field":               "#6bcb77",
    "ProgrammingLanguage": "#c77dff",
    "Concept":             "#ff9a3c",
}
node_colors = [type_colors.get(G.nodes[n].get("type",""), "#aaaaaa") for n in G.nodes]

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1600,
                       alpha=0.92, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7.5, font_color="white",
                        font_weight="bold", ax=ax)

# Draw edges with relation labels
edge_labels = {(u, v): d["relation"]
               for u, v, d in G.edges(data=True)}
nx.draw_networkx_edges(G, pos, edge_color="#8888aa", arrows=True,
                       arrowsize=18, width=1.5,
                       connectionstyle="arc3,rad=0.15", ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                              font_size=6, font_color="#ccccee", ax=ax)

# Legend
legend_handles = [mpatches.Patch(color=c, label=t)
                  for t, c in type_colors.items()]
ax.legend(handles=legend_handles, loc="upper left",
          facecolor="#1a1a2e", edgecolor="#555", labelcolor="white",
          fontsize=8, title="Entity Type", title_fontsize=9)

ax.set_title("Academic Knowledge Graph – NetworkX", color="white",
             fontsize=14, fontweight="bold", pad=12)
ax.axis("off")
plt.tight_layout()
plt.savefig("q1_tool1_networkx_kg.png", dpi=150,
            bbox_inches="tight", facecolor="#0f0f1a")
plt.close()
print("\n[NetworkX] Visualisation saved → q1_tool1_networkx_kg.png")


# ─────────────────────────────────────────────────────────────
# TOOL 2: RDFLib — Build a KG using W3C RDF Standard + SPARQL
# ─────────────────────────────────────────────────────────────
print("\n─── TOOL 2: RDFLib (RDF Triples + SPARQL) ─────────────────────")
print("RDFLib encodes knowledge as (Subject, Predicate, Object) triples.")
print("Resources are identified by URIs; SPARQL is used to query.\n")

from rdflib import Graph as RDFGraph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD

# Define our ontology namespace
BASE = Namespace("http://ai-knowledge.org/")
g = RDFGraph()
g.bind("ai", BASE)
g.bind("owl", OWL)

# ── Define Classes (Ontology Layer) ──
classes = ["Person", "University", "Award", "Field", "Concept", "Language"]
for cls in classes:
    g.add((BASE[cls], RDF.type, OWL.Class))
    g.add((BASE[cls], RDFS.label, Literal(cls)))

# ── Define Properties ──
props = {
    "studiedAt":  (BASE.Person, BASE.University),
    "workedAt":   (BASE.Person, BASE.University),
    "pioneered":  (BASE.Person, BASE.Field),
    "invented":   (BASE.Person, None),
    "won":        (BASE.Person, BASE.Award),
    "subFieldOf": (BASE.Field, BASE.Field),
    "uses":       (BASE.Field, BASE.Field),
    "conceptIn":  (BASE.Concept, BASE.Field),
}
for prop, (domain, rng) in props.items():
    g.add((BASE[prop], RDF.type, OWL.ObjectProperty))
    g.add((BASE[prop], RDFS.domain, domain))
    if rng:
        g.add((BASE[prop], RDFS.range, rng))

# ── Add Individual Triples ──
rdf_triples = [
    (BASE["AlanTuring"],   RDF.type,          BASE.Person),
    (BASE["AlanTuring"],   RDFS.label,         Literal("Alan Turing")),
    (BASE["AlanTuring"],   BASE.born,          Literal(1912, datatype=XSD.integer)),
    (BASE["AlanTuring"],   BASE.studiedAt,     BASE["Cambridge"]),
    (BASE["AlanTuring"],   BASE.pioneered,     BASE["ArtificialIntelligence"]),

    (BASE["JohnMcCarthy"], RDF.type,           BASE.Person),
    (BASE["JohnMcCarthy"], RDFS.label,         Literal("John McCarthy")),
    (BASE["JohnMcCarthy"], BASE.workedAt,      BASE["MIT"]),
    (BASE["JohnMcCarthy"], BASE.invented,      BASE["LISP"]),
    (BASE["JohnMcCarthy"], BASE.won,           BASE["TuringAward"]),
    (BASE["JohnMcCarthy"], BASE.pioneered,     BASE["ArtificialIntelligence"]),

    (BASE["MarvinMinsky"], RDF.type,           BASE.Person),
    (BASE["MarvinMinsky"], RDFS.label,         Literal("Marvin Minsky")),
    (BASE["MarvinMinsky"], BASE.workedAt,      BASE["MIT"]),
    (BASE["MarvinMinsky"], BASE.pioneered,     BASE["NeuralNetworks"]),
    (BASE["MarvinMinsky"], BASE.won,           BASE["TuringAward"]),

    (BASE["ArtificialIntelligence"], RDF.type, BASE.Field),
    (BASE["MachineLearning"],        RDF.type, BASE.Field),
    (BASE["NeuralNetworks"],         RDF.type, BASE.Field),
    (BASE["MachineLearning"], BASE.subFieldOf, BASE["ArtificialIntelligence"]),
    (BASE["NeuralNetworks"],  BASE.subFieldOf, BASE["ArtificialIntelligence"]),
    (BASE["MachineLearning"], BASE.uses,       BASE["NeuralNetworks"]),

    (BASE["MIT"],      RDF.type, BASE.University),
    (BASE["Stanford"], RDF.type, BASE.University),
    (BASE["Cambridge"],RDF.type, BASE.University),
    (BASE["TuringAward"], RDF.type, BASE.Award),
    (BASE["LISP"],     RDF.type, BASE.Language),
]
for triple in rdf_triples:
    g.add(triple)

print(f"RDF Graph: {len(g)} triples loaded\n")

# ── SPARQL Query 1: Persons and their birth years ──
q1 = """
PREFIX ai: <http://ai-knowledge.org/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?name ?born WHERE {
    ?person a ai:Person .
    ?person rdfs:label ?name .
    OPTIONAL { ?person ai:born ?born }
}
ORDER BY ?born
"""
print("SPARQL Query 1 – All Persons:")
for row in g.query(q1):
    print(f"   {row.name}  (born: {row.born})")

# ── SPARQL Query 2: Who won an award? ──
q2 = """
PREFIX ai: <http://ai-knowledge.org/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?name ?award WHERE {
    ?person a ai:Person ;
            rdfs:label ?name ;
            ai:won ?awardURI .
    BIND(STRAFTER(STR(?awardURI), "http://ai-knowledge.org/") AS ?award)
}
"""
print("\nSPARQL Query 2 – Award Winners:")
for row in g.query(q2):
    print(f"   {row.name} → {row.award}")

# ── SPARQL Query 3: Sub-fields of AI ──
q3 = """
PREFIX ai: <http://ai-knowledge.org/>
SELECT ?sub WHERE {
    ?sub ai:subFieldOf ai:ArtificialIntelligence .
}
"""
print("\nSPARQL Query 3 – Sub-fields of AI:")
for row in g.query(q3):
    field = str(row.sub).split("/")[-1]
    print(f"   → {field}")

# ─────────────────────────────────────────────────────────────
# Serialize to Turtle (standard RDF format)
# ─────────────────────────────────────────────────────────────

turtle_out = "q1_tool2_knowledge_graph.ttl"

g.serialize(destination=turtle_out, format="turtle")

print(f"\n[RDFLib] Graph serialised to Turtle → {turtle_out}")

print("   (Turtle is a human-readable RDF format used with")
print("    SPARQL endpoints, GraphDB, Apache Jena, Stardog,")
print("    and other triple stores.)")

# ─────────────────────────────────────────────────────────────
# TOOL 3: Comparison Summary
# ─────────────────────────────────────────────────────────────
print("\n─── TOOL 3: Summary – KG Tools Comparison ─────────────────────")
tools_table = [
    ("NetworkX",    "In-memory graph; rich algorithms; no RDF/SPARQL",       "Prototyping, graph analytics"),
    ("RDFLib",      "W3C RDF standard; SPARQL queries; OWL ontologies",       "Semantic Web, linked data"),
    ("PyVis",       "Interactive HTML visualisation of NetworkX/RDF graphs",  "KG exploration & demos"),
    ("Owlready2",   "OWL ontology loading + built-in HermiT/Pellet reasoner", "Ontology + automated inference"),
    ("py2neo/Neo4j","Property graph DB; Cypher query language; scalable",     "Production KG systems"),
    ("SPARQL APIs", "Query remote KGs (Wikidata, DBpedia) over HTTP",         "Linked open data integration"),
]
print(f"\n{'Tool':<14} {'Strength':<48} {'Best For'}")
print("─" * 85)
for tool, strength, best in tools_table:
    print(f"{tool:<14} {strength:<48} {best}")

print("\n" + "=" * 65)
print("  Q1 Complete. Outputs: PNG visualisation + Turtle RDF file.")
print("=" * 65)
