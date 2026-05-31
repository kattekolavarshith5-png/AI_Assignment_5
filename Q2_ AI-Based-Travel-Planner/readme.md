# AI Based Travel Planner

## Overview

AI Based Travel Planner is a Python-based intelligent travel recommendation system that suggests tourist destinations based on user interests, budget, and travel duration.

The system uses a rule-based recommendation approach to match user preferences with destinations stored in a knowledge base and generates a personalized travel itinerary.

---

## Features

- Travel destination recommendation
- Interest-based matching
- Budget-based filtering
- Personalized travel itinerary
- Cost estimation
- Food recommendations
- Smart travel suggestions
- Day-wise activity planning

---

## Technologies Used

- Python 3
- Rule-Based Artificial Intelligence
- Knowledge-Based System

---

## Knowledge Base

The system contains information about the following destinations:

- Goa
- Manali
- Jaipur
- Kerala
- Ladakh

For each destination, the knowledge base stores:

- Travel type
- Budget category
- Local foods
- Activities
- Hotel cost
- Food cost
- Transport cost

---

## How It Works

### Step 1: User Input

The user enters:

- Name
- Travel interest
- Budget
- Number of travel days

Example:

```text
Enter your name: Varshith
Enter your interest: adventure
Enter your budget: high
Enter number of travel days: 5
```

### Step 2: Recommendation Engine

The system:

- Matches user interest with destination type
- Filters destinations according to budget
- Generates recommended destinations

### Step 3: Destination Selection

The user selects a destination from the recommended list.

### Step 4: Tour Plan Generation

The system generates:

- Food recommendations
- Day-wise itinerary
- Budget report
- Travel suggestions

---

## Installation

Ensure Python 3 is installed:

```bash
python3 --version
```

---

## Running the Program

Execute:

```bash
python3 ai_travel_planner.py
```

---

## Sample Input

```text
Enter your name: Varshith
Enter your interest: adventure
Enter your budget: high
Enter number of travel days: 5
Select destination number: 2
```

---

## Sample Output

```text
Recommended Destinations:
1. Manali
2. Ladakh

PERSONALIZED TOUR PLAN FOR LADAKH

Traveler Name : Varshith
Destination   : Ladakh
Travel Days   : 5
Interest Type : adventure

Recommended Foods:
- Thukpa
- Momos
- Butter Tea

Day-wise Itinerary:
Day 1: Trekking
Day 2: Bike Riding
Day 3: Lake Visit
Day 4: Monastery Tour
Day 5: Trekking

Estimated Cost Breakdown:
Hotel Cost      : Rs. 25000
Food Cost       : Rs. 8000
Transport Cost  : Rs. 8000
Total Estimated : Rs. 41000

AI Suggestions:
- Carry safety equipment and trekking shoes
- Carry warm clothes and altitude medication
```

---

## Cost Calculation

Total Trip Cost:

```text
Total Cost =
(Hotel Cost × Travel Days)
+ (Food Cost × Travel Days)
+ Transport Cost
```

---

## Project Structure

```text
AI-Based-Travel-Planner/
│
├── ai_travel_planner.py
├── README.md
└── screenshots/
```

---

## Applications

- Tourism Recommendation Systems
- Travel Planning Assistants
- Personalized Vacation Planning
- AI-Based Recommendation Systems

---

## Future Enhancements

- Weather Forecast Integration
- Hotel Booking System
- Transportation Booking
- GUI Interface
- Machine Learning-Based Recommendations
- Real-Time Travel Data

---

## Learning Outcomes

This project demonstrates:

- Knowledge-Based Systems
- Rule-Based AI
- Recommendation Systems
- User Interaction in Python
- Cost Estimation Algorithms

---

## Author

Varshith Kattekola

Artificial Intelligence Laboratory Assignment
