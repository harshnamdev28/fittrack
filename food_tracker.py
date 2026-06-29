import requests
import pandas as pd
import os
from datetime import date
from database import get_connection
from google import genai
import json
from dotenv import load_dotenv
load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")

def extract_nutrients(nutrients_list):
    calories = protein = carbs = fibre = fat = 0
    for n in nutrients_list:
        name = n["nutrientName"]
        value = n["value"]
        unit = n.get("unitName", "")
        if name == "Energy" and unit == "KCAL":
            calories = value
        elif name == "Protein":
            protein = value
        elif name == "Carbohydrate, by difference":
            carbs = value
        elif name == "Fiber, total dietary":
            fibre = value
        elif name == "Total lipid (fat)":
            fat = value
    return calories, protein, carbs, fibre, fat
    
 
def daily_summary(user_id):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM food_log WHERE user_id=?", conn,params=(user_id,))
    conn.close()
    
    
    # filter only today's entries
    today = str(date.today())
    df["date"] = df["date"].astype(str)
    today_df = df[df["date"] == today]
    
    if today_df.empty:
        print("No meals logged today!")
        return
    
    print("\n📊 Today's Meals:")
    print(today_df[["meal", "calories", "protein"]].to_string(index=False))
    
    print("\n📈 Today's Totals:")
    print(f"Calories : {today_df['calories'].sum()} kcal")
    print(f"Protein  : {today_df['protein'].sum()} g")
    print(f"Carbs    : {today_df['carbs'].sum()} g")
    print(f"Fibre    : {today_df['fibre'].sum()} g")
    print(f"Fat      : {today_df['fat'].sum()} g")
     


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def estimate_nutrition_ai(meal_name):
   
    prompt = f"""
    A user ate: {meal_name}

    Estimate the nutrition for this. Identify what food this is and give it a clean, short name.

    Respond ONLY in this exact JSON format, no other text:
    {{   
        "food": "<short, clean name of the food, e.g. 'Bread' not '2 slices'>",
        "calories": <number>,
        "protein": <number in grams>,
        "carbs": <number in grams>,
        "fibre": <number in grams>,
        "fat": <number in grams>
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    
    nutrition = json.loads(text)
    
    
    return nutrition


def estimate_grams_ai(description, food_name):
    prompt = f"""
    Estimate the weight in grams for: {description} of {food_name}
    
    Respond ONLY with a single number representing grams, no units, no other text.
    Example response: 50
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    text = response.text.strip()
    grams = float(text)
    
    return grams




def search_food_options(meal_name):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    
    params = {
        "query": meal_name,
        "api_key": USDA_API_KEY,
        "pageSize": 5,
        "dataType": ["Foundation", "SR Legacy"]
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data["foods"]



def select_and_log_food(meal_name,user_id):
    foods = search_food_options(meal_name)
    
    if len(foods) == 0:
        # AI fallback (reuse existing logic)
        nutrition = estimate_nutrition_ai(meal_name)
        food_name = nutrition["food"]
        calories = nutrition["calories"]
        protein = nutrition["protein"]
        carbs = nutrition["carbs"]
        fibre = nutrition["fibre"]
        fat = nutrition["fat"]
    else:
        print("\nSelect the closest match:")
        for idx, food in enumerate(foods):
            print(f"{idx + 1}. {food['description']}")
        print(f"{len(foods) + 1}. None of these - use AI estimate instead")
        
        choice = int(input("Enter number: ")) - 1
        
        if choice == len(foods):
            # fall back to AI with full description
            description = input("Describe what you ate (e.g. '2 slices of bread'): ")
            nutrition = estimate_nutrition_ai(description)
            food_name = nutrition["food"]
            calories = nutrition["calories"]
            protein = nutrition["protein"]
            carbs = nutrition["carbs"]
            fibre = nutrition["fibre"]
            fat = nutrition["fat"]
        else:
            food = foods[choice]
            food_name = food["description"]
            nutrients = food["foodNutrients"]
            
            calories = protein = carbs = fibre = fat = 0
            for n in nutrients:
                name = n["nutrientName"]
                value = n["value"]
                unit = n["unitName"]
                if name == "Energy" and unit == "KCAL":
                    calories = value
                elif name == "Protein":
                    protein = value
                elif name == "Carbohydrate, by difference":
                    carbs = value
                elif name == "Fiber, total dietary":
                    fibre = value
                elif name == "Total lipid (fat)":
                    fat = value
            
            print("\nHow much did you eat?")
            print("1. Enter exact grams")
            print("2. Describe it (e.g. '2 slices', '1 bowl') - AI will estimate")
            qty_choice = input("Choose (1/2): ")
            
            if qty_choice == "1":
                grams = float(input("Enter grams: "))
            else:
                portion_description = input("Describe how much (e.g. '2 slices'): ")
                grams = estimate_grams_ai(portion_description, food_name)
                print(f"Estimated weight: {grams}g")
            
            calories = (calories / 100) * grams
            protein = (protein / 100) * grams
            carbs = (carbs / 100) * grams
            fibre = (fibre / 100) * grams
            fat = (fat / 100) * grams
        
        
    # rest stays the same - print, save to db, return
    print(f"\n🍽️  {food_name}")
    print(f"Calories : {calories} kcal")
    print(f"Protein  : {protein} g")
    print(f"Carbs    : {carbs} g")
    print(f"Fibre    : {fibre} g")
    print(f"Fat      : {fat} g")
    
    entry = {
        "date": date.today(),
        "meal": food_name,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fibre": fibre,
        "fat": fat
    }
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO food_log (user_id, date, meal, calories, protein, carbs, fibre, fat)
        VALUES (?, ?, ?, ?, ?, ?, ?,?)
    """, (user_id, entry["date"].isoformat() if hasattr(entry["date"], 'isoformat') else entry["date"], 
          entry["meal"], entry["calories"], entry["protein"], 
          entry["carbs"], entry["fibre"], entry["fat"]))
    conn.commit()
    conn.close()
    
    return entry

def log_food_streamlit(food_name, calories, protein, carbs, fibre, fat, user_id):
    entry = {
        "date": date.today(),
        "meal": food_name,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fibre": fibre,
        "fat": fat
    }
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO food_log (user_id, date, meal, calories, protein, carbs, fibre, fat)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, entry["date"].isoformat() if hasattr(entry["date"], 'isoformat') else entry["date"], 
          entry["meal"], entry["calories"], entry["protein"], 
          entry["carbs"], entry["fibre"], entry["fat"]))
    conn.commit()
    conn.close()
    
    return entry