def calculate_maintenance():
    weight = float(input("Enter weight (kg): "))
    height = float(input("Enter height (cm): "))
    age = int(input("Enter age: "))
    gender = input("Gender (M/F): ")
    
    if(gender.upper()=="M"):
        bmr=10*weight+6.25*height-5*age +5
        
    else:
        bmr=10*weight+6.25*height-5*age -161
    print("\nActivity Level:")
    print("1. Sedentary (little/no exercise)")
    print("2. Light activity (1-3 days/week)")
    print("3. Moderate activity (3-5 days/week)")
    print("4. Very active (6-7 days/week)")
    activity_choice = input("Choose (1/2/3/4): ")

    if activity_choice == "1":
       tdee = bmr * 1.2
    elif activity_choice == "2":
       tdee = bmr * 1.375
    elif activity_choice == "3":
       tdee = bmr * 1.55
    elif activity_choice == "4":
       tdee = bmr * 1.725
    else:
        tdee = bmr * 1.2  # default to sedentary if invalid input
    # Protein based on bodyweight (works for both bulk/cut)
    protein_grams = weight * 1.8

# For bulk target
    bulk_calories = tdee + 400
    bulk_protein_cals = protein_grams * 4        # protein has 4 cal/gram
    bulk_fat_cals = bulk_calories * 0.25
    bulk_fat_grams = bulk_fat_cals / 9            # fat has 9 cal/gram
    bulk_carbs_cals = bulk_calories - bulk_protein_cals - bulk_fat_cals
    bulk_carbs_grams = bulk_carbs_cals / 4        # carbs have 4 cal/gram
    
    # For cut target
    cut_calories = tdee - 400
    cut_protein_cals = protein_grams * 4
    cut_fat_cals = cut_calories * 0.25
    cut_fat_grams = cut_fat_cals / 9
    cut_carbs_cals = cut_calories - cut_protein_cals - cut_fat_cals
    cut_carbs_grams = cut_carbs_cals / 4


    print(f"\nYour maintenance calories (TDEE): {tdee:.0f} kcal/day")
    
    print(f"Your BMR is:{bmr}kcal/day")
    print(f"\n🔼 BULK: {bulk_calories:.0f} kcal")
    print(f"   Protein: {protein_grams:.0f}g | Carbs: {bulk_carbs_grams:.0f}g | Fat: {bulk_fat_grams:.0f}g")
    print(f"\n🔽 CUT: {cut_calories:.0f} kcal")
    print(f"   Protein: {protein_grams:.0f}g | Carbs: {cut_carbs_grams:.0f}g | Fat: {cut_fat_grams:.0f}g")



def calculate_maintenance_streamlit(weight, height, age, gender, activity_level):
    if gender.upper() == "M":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161
    
    activity_multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Very Active": 1.725
    }
    tdee = bmr * activity_multipliers[activity_level]
    
    protein_grams = weight * 1.8
    
    bulk_calories = tdee + 400
    bulk_protein_cals = protein_grams * 4
    bulk_fat_cals = bulk_calories * 0.25
    bulk_fat_grams = bulk_fat_cals / 9
    bulk_carbs_grams = (bulk_calories - bulk_protein_cals - bulk_fat_cals) / 4
    
    cut_calories = tdee - 400
    cut_fat_cals = cut_calories * 0.25
    cut_fat_grams = cut_fat_cals / 9
    cut_carbs_grams = (cut_calories - bulk_protein_cals - cut_fat_cals) / 4
    
    return {
        "bmr": bmr,
        "tdee": tdee,
        "bulk_calories": bulk_calories,
        "bulk_protein": protein_grams,
        "bulk_carbs": bulk_carbs_grams,
        "bulk_fat": bulk_fat_grams,
        "cut_calories": cut_calories,
        "cut_protein": protein_grams,
        "cut_carbs": cut_carbs_grams,
        "cut_fat": cut_fat_grams
    }