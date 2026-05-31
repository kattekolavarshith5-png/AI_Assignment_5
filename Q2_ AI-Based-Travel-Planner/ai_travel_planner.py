# ==============================================
# AI BASED TRAVEL PLANNER
# ==============================================

import random

# ==============================================
# KNOWLEDGE BASE
# ==============================================

travel_kb = {
    "Goa": {
        "type": ["beach", "nightlife", "relaxation"],
        "budget": "medium",
        "food": ["Seafood", "Goan Curry", "Bebinca"],
        "activities": [
            "Beach Visit",
            "Water Sports",
            "Night Clubs",
            "Boat Cruise"
        ],
        "hotel_cost": 3000,
        "food_cost": 1200,
        "transport_cost": 4000
    },

    "Manali": {
        "type": ["mountain", "adventure", "nature"],
        "budget": "medium",
        "food": ["Himachali Thali", "Trout Fish", "Momos"],
        "activities": [
            "Paragliding",
            "Snow Activities",
            "Camping",
            "River Rafting"
        ],
        "hotel_cost": 2500,
        "food_cost": 1000,
        "transport_cost": 5000
    },

    "Jaipur": {
        "type": ["history", "culture", "royal"],
        "budget": "low",
        "food": ["Dal Baati", "Ghewar", "Laal Maas"],
        "activities": [
            "Fort Visit",
            "Museum Tour",
            "Shopping",
            "Camel Ride"
        ],
        "hotel_cost": 2000,
        "food_cost": 900,
        "transport_cost": 3500
    },

    "Kerala": {
        "type": ["nature", "backwaters", "relaxation"],
        "budget": "high",
        "food": ["Appam", "Puttu", "Kerala Fish Curry"],
        "activities": [
            "Houseboat",
            "Ayurvedic Spa",
            "Tea Garden Visit",
            "Backwater Cruise"
        ],
        "hotel_cost": 4500,
        "food_cost": 1500,
        "transport_cost": 6000
    },

    "Ladakh": {
        "type": ["adventure", "mountain", "nature"],
        "budget": "high",
        "food": ["Thukpa", "Momos", "Butter Tea"],
        "activities": [
            "Bike Riding",
            "Lake Visit",
            "Monastery Tour",
            "Trekking"
        ],
        "hotel_cost": 5000,
        "food_cost": 1600,
        "transport_cost": 8000
    }
}

# ==============================================
# USER INPUT MODULE
# ==============================================

print("=" * 50)
print("      AI BASED TRAVEL PLANNER")
print("=" * 50)

name = input("Enter your name: ")
interest = input(
    "Enter your interest (beach/mountain/history/adventure/nature/nightlife): "
).lower()

budget = input(
    "Enter your budget (low/medium/high): "
).lower()

travel_days = int(input("Enter number of travel days: "))

# ==============================================
# AI RECOMMENDATION ENGINE
# ==============================================

recommended_places = []

for place, details in travel_kb.items():

    # Rule-Based Matching
    if interest in details["type"]:

        # Budget Matching
        if budget == details["budget"] or budget == "high":
            recommended_places.append(place)

# ==============================================
# IF NO EXACT MATCH FOUND
# ==============================================

if len(recommended_places) == 0:
    print("\nNo exact match found.")
    print("Showing closest recommendations...\n")

    for place in travel_kb:
        recommended_places.append(place)

# ==============================================
# DISPLAY RECOMMENDATIONS
# ==============================================

print("\nRecommended Destinations:")
print("-" * 40)

for i, place in enumerate(recommended_places, start=1):
    print(f"{i}. {place}")

# ==============================================
# SELECT DESTINATION
# ==============================================

choice = int(input("\nSelect destination number: "))
selected_place = recommended_places[choice - 1]

place_data = travel_kb[selected_place]

# ==============================================
# COST ESTIMATION
# ==============================================

hotel_total = place_data["hotel_cost"] * travel_days
food_total = place_data["food_cost"] * travel_days
transport_total = place_data["transport_cost"]

estimated_total = hotel_total + food_total + transport_total

# ==============================================
# GENERATE ITINERARY
# ==============================================

activities = place_data["activities"]

print("\n" + "=" * 50)
print(f"      PERSONALIZED TOUR PLAN FOR {selected_place.upper()}")
print("=" * 50)

print(f"\nTraveler Name : {name}")
print(f"Destination   : {selected_place}")
print(f"Travel Days   : {travel_days}")
print(f"Interest Type : {interest}")

# ==============================================
# FOOD RECOMMENDATION
# ==============================================

print("\nRecommended Foods:")
for food in place_data["food"]:
    print(f"- {food}")

# ==============================================
# DAY WISE PLAN
# ==============================================

print("\nDay-wise Itinerary:")

for day in range(1, travel_days + 1):

    activity = random.choice(activities)

    print(f"Day {day}: {activity}")

# ==============================================
# BUDGET REPORT
# ==============================================

print("\nEstimated Cost Breakdown")
print("-" * 35)

print(f"Hotel Cost      : Rs. {hotel_total}")
print(f"Food Cost       : Rs. {food_total}")
print(f"Transport Cost  : Rs. {transport_total}")
print(f"Total Estimated : Rs. {estimated_total}")

# ==============================================
# SMART AI SUGGESTIONS
# ==============================================

print("\nAI Suggestions")
print("-" * 35)

if interest == "adventure":
    print("- Carry safety equipment and trekking shoes")

if budget == "low":
    print("- Use public transport to reduce expenses")

if selected_place == "Goa":
    print("- Best season: November to February")

if selected_place == "Ladakh":
    print("- Carry warm clothes and altitude medication")

print("\nThank you for using AI Travel Planner!")
