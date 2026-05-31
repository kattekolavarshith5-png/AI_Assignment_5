# Bayesian Networks – Medical Diagnosis Example

## Overview

This project demonstrates the implementation of a **Bayesian Network (BN)** using Python and the **pgmpy** library. Bayesian Networks are probabilistic graphical models that represent variables and their conditional dependencies using a Directed Acyclic Graph (DAG).

The project models a medical diagnosis problem involving diseases, symptoms, and risk factors, and performs probabilistic inference using Bayesian reasoning.

---

## Features

- Construction of a Bayesian Network (DAG)
- Definition of Conditional Probability Tables (CPTs)
- Exact probabilistic inference
- Posterior probability computation
- MAP (Most Probable Explanation) inference
- D-Separation analysis
- Bayesian Network visualization
- Comparison of popular Bayesian Network tools

---

## Technologies Used

- Python 3
- pgmpy
- NumPy
- NetworkX
- Matplotlib

---

## Bayesian Network Structure

The network consists of the following variables:

```text
Asia → Tuberculosis
Tuberculosis → Either
Smoking → LungCancer
Smoking → Bronchitis
LungCancer → Either
Either → XRay
Either → Dyspnea
Bronchitis → Dyspnea
```

---

## Installation

### Create Virtual Environment

```bash
python3 -m venv bn_env
source bn_env/bin/activate
```

### Install Required Libraries

```bash
pip install pgmpy numpy matplotlib networkx
```

---

## How to Run

Execute the program using:

```bash
python bayesian_network.py
```

---

## Sample Output

```text
BAYESIAN NETWORKS – MEDICAL DIAGNOSIS EXAMPLE

STEP 1: Define the DAG

Model validation: PASSED

Query 1 – P(Dyspnea)

P(Dyspnea=No) = 0.6025
P(Dyspnea=Yes) = 0.3975

Query 2 – P(LungCancer | Dyspnea=Yes, Smoking=Yes)

P(LungCancer=No) = 0.8293
P(LungCancer=Yes) = 0.1707
```

---

## Inference Queries Performed

### Query 1

Probability of Dyspnea without evidence:

```text
P(Dyspnea)
```

### Query 2

Probability of Lung Cancer given:

```text
Dyspnea = Yes
Smoking = Yes
```

### Query 3

Probability of Tuberculosis given:

```text
Asia = Yes
XRay = Abnormal
```

### Query 4

Most Probable Explanation (MAP)

```text
MAP(Dyspnea = Yes, XRay = Abnormal)
```

### Query 5

Smoking's causal effect on outcomes

- Lung Cancer
- Bronchitis
- Dyspnea

---

## D-Separation Analysis

The project demonstrates conditional independence concepts such as:

```text
Tuberculosis ⊥ LungCancer

Tuberculosis ⊥̸ LungCancer | Either
```

This illustrates dependency and independency relationships in Bayesian Networks.

---

## Generated Output

The program generates:

```text
q2_bayesian_network.png
```

This image contains the visual representation of the Bayesian Network.

---

## Project Structure

```text
Q2_Bayesian_Network_Implementation/
│
├── bayesian_network.py
├── README.md
└── q2_bayesian_network.png
```

---

## Applications

Bayesian Networks are widely used in:

- Medical Diagnosis
- Risk Analysis
- Fault Detection
- Decision Support Systems
- Artificial Intelligence
- Machine Learning
- Expert Systems

---

## Learning Outcomes

After completing this project, users will understand:

- Bayesian Networks
- Directed Acyclic Graphs (DAGs)
- Conditional Probability Tables (CPTs)
- Bayesian Inference
- MAP Queries
- D-Separation
- Probabilistic Reasoning

---

## Results

- Bayesian Network successfully created
- CPTs defined and validated
- Exact inference performed
- MAP explanation computed
- D-Separation analyzed
- Network visualization generated

---

## Author

Varshith Kattekola

Artificial Intelligence Laboratory Assignment – Q2 Bayesian Networks Implementation
