import streamlit as st
from food_tracker import daily_summary,select_and_log_food, search_food_options, extract_nutrients,log_food_streamlit,estimate_nutrition_ai,estimate_grams_ai
from workout_tracker import log_workout, workout_summary,log_workout_streamlit
from charts import calorie_chart, protein_chart, carbs_chart, workout_chart
import pandas as pd
from datetime import date
from database import get_connection
import streamlit as st
from auth import signup, login
from calorie_calculator import calculate_maintenance_streamlit
from database import init_db
init_db()


st.set_page_config(page_title="FitTrack", page_icon="💪")

# Initialize session state for login tracking
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# If not logged in, show login/signup form and stop here
if st.session_state.user_id is None:
    st.title("💪 FitTrack Login")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user_id = login(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_username = st.text_input("Choose a username", key="signup_user")
        new_password = st.text_input("Choose a password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            success = signup(new_username, new_password)
            if success:
                st.success("Account created! Please login.")
            else:
                st.error("Username already taken")
    
    st.stop()  # ← stops the script here if not logged in, rest of app won't run


st.title("💪 FitTrack")
st.write("Your personal fitness & nutrition tracker")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Home", "🍽️ Log Meal", "💪 Log Workout", "📊 Charts", "📅 Daily Summary","📅 Workout Summary","🔥 Calorie Calculator"]
)

if page == "🏠 Home":
    st.write("### Welcome to FitTrack!")
    st.write("Use the sidebar to navigate.")

elif page == "🍽️ Log Meal":
    st.write("### 🍽️ Log a Meal")
    meal_name = st.text_input("Enter meal name:")
    
    if st.button("Search"):
        st.session_state.search_results = search_food_options(meal_name)
    
    if "search_results" in st.session_state:
        foods = st.session_state.search_results
        
        if len(foods) == 0:
            st.info("No USDA match found. Describe what you ate:")
            description = st.text_input("Description (e.g. '1 plate of dosa')", key="ai_desc_noresults")
            
            if st.button("Get AI Estimate", key="ai_btn_noresults"):
                nutrition = estimate_nutrition_ai(description)
                st.session_state.ai_nutrition = nutrition
        else:
            options = [f["description"] for f in foods] + ["None of these"]
            selected = st.selectbox("Select closest match:", options)
            
            if selected != "None of these":
                grams = st.number_input("How many grams did you eat?", min_value=1, value=100)
                
                if st.button("Log this meal"):
                    selected_food = foods[options.index(selected)]
                    nutrients = selected_food["foodNutrients"]
                    calories, protein, carbs, fibre, fat = extract_nutrients(nutrients)
                    
                    calories = (calories / 100) * grams
                    protein = (protein / 100) * grams
                    carbs = (carbs / 100) * grams
                    fibre = (fibre / 100) * grams
                    fat = (fat / 100) * grams
                    
                    result = log_food_streamlit(selected, calories, protein, carbs, fibre, fat, st.session_state.user_id)
                    st.success(f"✅ Logged: {result['meal']} - {calories:.0f} kcal")
                    del st.session_state.search_results
            else:
                st.info("Describe what you ate instead:")
                description = st.text_input("Description (e.g. '2 slices of bread')", key="ai_desc_noneofthese")
                
                if st.button("Get AI Estimate", key="ai_btn_noneofthese"):
                    nutrition = estimate_nutrition_ai(description)
                    st.session_state.ai_nutrition = nutrition
    
    if "ai_nutrition" in st.session_state:
        nutrition = st.session_state.ai_nutrition
        st.write(f"### {nutrition['food']}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Calories", f"{nutrition['calories']} kcal")
        col2.metric("Protein", f"{nutrition['protein']} g")
        col3.metric("Carbs", f"{nutrition['carbs']} g")
        
        if st.button("Confirm & Log", key="confirm_ai_log"):
            result = log_food_streamlit(nutrition['food'], nutrition['calories'], nutrition['protein'],
                                          nutrition['carbs'], nutrition['fibre'], nutrition['fat'], 
                                          st.session_state.user_id)
            st.success(f"✅ Logged: {result['meal']}")
            del st.session_state.ai_nutrition
            if "search_results" in st.session_state:
                del st.session_state.search_results

         
elif page == "💪 Log Workout":
    st.write("### 💪 Log a Workout")
    
    exercise = st.text_input("Exercise name:")
    sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
    reps = st.number_input("Reps", min_value=1, max_value=50, value=10)
    weight = st.number_input("Weight (kg)", min_value=0, value=20)
    
    if st.button("Log Workout"):
        if exercise:
             result = log_workout_streamlit(exercise, sets, reps, weight, user_id=st.session_state.user_id)
             st.success(f"✅ Logged: {exercise} - {sets} sets x {reps} reps @ {weight}kg")
        else:
         st.warning("Please enter exercise name!")

elif page == "📊 Charts":
    st.write("### 📊 Progress Charts")
    
    chart_choice = st.selectbox(
        "Choose a chart",
        ["Calories", "Protein", "Carbs", "Workout Volume"]
    )
    
    if st.button("Show Chart"):
        if chart_choice == "Calories":
            calorie_chart(st.session_state.user_id)
        elif chart_choice == "Protein":
            protein_chart(st.session_state.user_id)
        elif chart_choice == "Carbs":
            carbs_chart(st.session_state.user_id)
        elif chart_choice == "Workout Volume":
            workout_chart(st.session_state.user_id)
elif page == "📅 Daily Summary":
    st.write("### 📅 Today's Summary")
    
    st.write("#### 🍽️ Meals")
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM food_log WHERE user_id=?", conn, params=(st.session_state.user_id ,))
    conn.close()
    
    df["date"] = df["date"].astype(str)
    today = str(date.today())
    today_df = df[df["date"] == today]
        
    if today_df.empty:
        st.info("No meals logged today!")
    else:
        st.dataframe(today_df[["meal", "calories", "protein", "carbs"]])
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Calories", f"{today_df['calories'].sum()}kcal ")
        col2.metric("Total Protein", f"{today_df['protein'].sum()} g")
        col3.metric("Total Carbs", f"{today_df['carbs'].sum()} g")
    


elif page == "📅 Workout Summary":
    st.write("### 📅 Today's Workout Summary")
    
    st.write("#### Workout")
    conn=get_connection()
    df=pd.read_sql_query("SELECT * FROM workout_log WHERE user_id=?",conn, params=(st.session_state.user_id,))
    conn.close()
    
    df["date"] = df["date"].astype(str)
    today = str(date.today())
    today_df = df[df["date"] == today]
        
    if today_df.empty:
         st.info("No Workout logged today!")
    else:
         st.dataframe(today_df[["exercise", "sets", "reps", "weight"]])
            
         today_df["volume"] = today_df["sets"] * today_df["reps"] * today_df["weight"]
            
         col1, col2 = st.columns(2)
         col1.metric("Total Sets", today_df["sets"].sum())
         col2.metric("Total Volume", f"{today_df['volume'].sum()} kg")
        
    


elif page == "🔥 Calorie Calculator":
    st.write("### 🔥 Maintenance Calorie Calculator")
    
    weight = st.number_input("Weight (kg)", min_value=1.0, value=60.0)
    height = st.number_input("Height (cm)", min_value=1.0, value=170.0)
    age = st.number_input("Age", min_value=1, value=20)
    gender = st.selectbox("Gender", ["M", "F"])
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Very Active"])
    
    if st.button("Calculate"):
        result = calculate_maintenance_streamlit(weight, height, age, gender, activity_level)
        
        st.metric("BMR", f"{result['bmr']:.0f} kcal/day")
        st.metric("Maintenance (TDEE)", f"{result['tdee']:.0f} kcal/day")
        
        st.write("#### 🔼 Bulk")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{result['bulk_calories']:.0f}")
        col2.metric("Protein", f"{result['bulk_protein']:.0f}g")
        col3.metric("Carbs", f"{result['bulk_carbs']:.0f}g")
        col4.metric("Fat", f"{result['bulk_fat']:.0f}g")
        
        st.write("#### 🔽 Cut")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{result['cut_calories']:.0f}")
        col2.metric("Protein", f"{result['cut_protein']:.0f}g")
        col3.metric("Carbs", f"{result['cut_carbs']:.0f}g")
        col4.metric("Fat", f"{result['cut_fat']:.0f}g")