
import pandas as pd
from datetime import date
import os
from database import get_connection
def log_workout(user_id):
   
    print("1. Today")
    print("2. Enter a different date")
    day_choice = input("Choose (1/2): ")

    if day_choice == "1":
        workout_date = date.today()
    else:
         workout_date = input("Enter date (YYYY-MM-DD): ")
    print("What type of workout?")
    print("1. Push (Chest/Shoulders/Triceps)")
    print("2. Pull (Back/Biceps)")
    print("3. Legs")
    print("4. Custom")
    
    workout_type = input("Choose (1/2/3/4): ")
    while True:
        exercise = input("Enter exercise name: ")
        num_sets=int(input("Enter the no of sets you perform"))
        for i in range(1,num_sets+1):
            print(f"\nSet{i}:")
            reps=int(input("Enter the no of reps"))
            weight=int(input("Enter the weight in kg:"))
            entry = {
            "date": workout_date,
            "workout_type":workout_type,
            "exercise":exercise,
            "sets":i,
            "reps":reps,
            "weight":weight,
           }
            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute("""
           INSERT INTO workout_log(user_id, date, workout_type, exercise, sets, reps,weight)
        VALUES(?, ?, ?, ?, ?, ?,?)
     """,(user_id, entry["date"],entry["workout_type"],entry["exercise"],entry["sets"],entry["reps"],entry["weight"])
                   )
            conn.commit()
            conn.close()
            
        
        more=input("\nAdd another exercise?(yes/no):")
        if(more.lower()=="no"):
         break
    print(f"\n✅ {num_sets} sets logged for {exercise}!")
def log_workout_streamlit(exercise, sets, reps, weight, user_id, workout_type="Custom", workout_date=None):
    if workout_date is None:
        workout_date = date.today()
    
    entry = {
        "date": workout_date,
        "workout_type": workout_type,
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight
    }
    
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO workout_log(user_id, date, workout_type, exercise, sets, reps,weight)
        VALUES(?, ?, ?, ?, ?, ?,?)
     """,(user_id,entry["date"],entry["workout_type"],entry["exercise"],entry["sets"],entry["reps"],entry["weight"])
                   )
    conn.commit()
    conn.close()
    return entry
def workout_summary(user_id):  
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM workout_log WHERE user_id=?", conn,params=(user_id,))
    conn.close()
    
    
    # filter only today's entries
    today = str(date.today())
    df["date"] = df["date"].astype(str)
    today_df = df[df["date"] == today]
    
    if today_df.empty:
        print("No Workout logged today!")
        return
    
    
   
    print("\n💪 Today's Workout:")
    print(today_df[["exercise", "sets", "reps", "weight"]].to_string(index=False))

    

