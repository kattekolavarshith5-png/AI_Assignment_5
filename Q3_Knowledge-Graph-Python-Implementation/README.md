# Knowledge Graph Python Implementation

## Overview

This project demonstrates the implementation of a **Knowledge Graph (KG)** using Python. A Knowledge Graph represents real-world entities and their relationships in the form of nodes and edges. The project uses multiple Python tools to build, query, visualize, and serialize knowledge graphs.

The implementation covers:

- NetworkX for graph creation and analysis
- RDFLib for RDF triples and SPARQL querying
- Knowledge Graph visualization
- RDF serialization in Turtle format

---

## Features

### Tool 1: NetworkX
- Creates a directed knowledge graph
- Represents entities as nodes
- Represents relationships as edges
- Supports graph traversal and querying
- Generates graph visualization

### Tool 2: RDFLib
- Stores knowledge as RDF triples
- Supports ontology concepts
- Executes SPARQL queries
- Exports knowledge graph in Turtle (.ttl) format

### Tool 3: Knowledge Graph Comparison
- Compares popular Knowledge Graph tools
- Highlights strengths and applications of each tool

---

## Technologies Used

- Python 3
- NetworkX
- Matplotlib
- RDFLib

---

## Installation

Install required packages:

```bash
sudo apt update
sudo apt install python3-networkx python3-matplotlib python3-rdflib
```

or

```bash
pip install networkx matplotlib rdflib
```

---

## Project Structure

```text
Q3_Knowledge_Graph_Python_Implementation/
│
├── knowledge_graph.py
├── README.md
├── q1_tool1_networkx_kg.png
└── q1_tool2_knowledge_graph.ttl
```

---

## How to Run

Execute the program:

```bash
python3 knowledge_graph.py
```

---

## Sample Output

```text
KNOWLEDGE GRAPHS – PYTHON IMPLEMENTATION

Graph built: 12 nodes, 17 edges

Query 1 – Who worked at MIT?
→ John McCarthy
→ Marvin Minsky

Query 2 – What did John McCarthy do?
John McCarthy --[workedAt]--> MIT
John McCarthy --[invented]--> LISP

SPARQL Query 3 – Sub-fields of AI:
→ MachineLearning
→ NeuralNetworks
```

---

## Generated Files

### Graph Visualization

```text
q1_tool1_networkx_kg.png
```

Contains the visual representation of the Knowledge Graph.

### RDF Turtle File

```text
q1_tool2_knowledge_graph.ttl
```

Contains the RDF representation of the Knowledge Graph in Turtle format.

---

## Knowledge Graph Concepts Covered

- Nodes and Entities
- Relationships and Edges
- RDF Triples
- SPARQL Queries
- Ontologies
- Semantic Web
- Graph Visualization

---

## Applications

- Search Engines
- Recommendation Systems
- Semantic Web
- Expert Systems
- Question Answering Systems
- Social Networks

---

## Learning Outcomes

After completing this project, users will understand:

- Knowledge Graph fundamentals
- Graph-based knowledge representation
- RDF and Semantic Web concepts
- SPARQL querying
- Knowledge Graph visualization techniques

---

## Author

Varshith Kattekola

Artificial Intelligence Laboratory Assignment – Q3 Knowledge Graph Python Implementation
