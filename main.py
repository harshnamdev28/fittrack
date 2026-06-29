from food_tracker import daily_summary,select_and_log_food
from workout_tracker import log_workout, workout_summary
from charts import calorie_chart, protein_chart, carbs_chart, workout_chart
from calorie_calculator import calculate_maintenance
from auth import signup, login

print("========= Welcome to FitTrack =========")
print("1. Login")
print("2. Sign up")
auth_choice = input("Choose (1/2): ")

username = input("Username: ")
password = input("Password: ")

if auth_choice == "2":
    success = signup(username, password)
    if not success:
        print("Username already taken! Try logging in instead.")
        exit()
    print("Account created!")

user_id = login(username, password)

if user_id is None:
    print("Invalid username or password!")
    exit()

print(f"\nWelcome back! 💪")
while True:
    print("\n========= FitTrack =========")
    print("1. Log your Workout")
    print("2. Log Your Meal")
    print("3. View today's Workout ")
    print("4. View today's meal")
    print("5. View Progress chart")
    print("6. Maintenance calorie")
    print("7.Exit")
    
    choice = input("\nEnter choice (1/2/3/4/5/6/7): ")
    
    if choice == "1":
        log_workout(user_id)
    elif choice == "2":
        meal=input("Enter Your Meal")
        select_and_log_food(meal,user_id)
    elif choice == "3":
        workout_summary(user_id)
    elif choice=="4":
        daily_summary(user_id)
    elif choice == "5":
       print("\n📊 Which chart?")
       print("1. Calories")
       print("2. Protein")
       print("3. Carbs")
       print("4. Workout Volume")
       chart_choice = input("Choose (1/2/3/4): ")
    
       if chart_choice == "1":
            calorie_chart(user_id, use_streamlit=False)
       elif chart_choice == "2":
            protein_chart(user_id, use_streamlit=False)
       elif chart_choice == "3":
           carbs_chart(user_id, use_streamlit=False)
       elif chart_choice == "4":
            workout_chart(user_id, use_streamlit=False)
       else:
           print("Invalid choice!")
    elif choice =="6":
        calculate_maintenance()
    elif choice == "7":
        print("\nStay consistent! 💪")
        break    

    else:
        print("Invalid choice, try again!")


