# 💪 FitTrack

A full-stack fitness and nutrition tracking application with AI-powered meal estimation, built in Python.

FitTrack lets users log meals and workouts, track daily nutrition using real USDA data, get AI-estimated nutrition for foods not in the database (like regional dishes), calculate maintenance calories for bulking/cutting, and visualize progress over time — all behind secure multi-user authentication.

Available as both a **terminal app** and a **Streamlit web app**, sharing the same backend logic and database.

---

## ✨ Features

- 🔐 **User authentication** — signup/login with hashed passwords, each user's data kept separate
- 🍽️ **Smart meal logging**
  - Searches the USDA FoodData Central database for accurate nutrition data
  - Lets you pick the closest match from real search results
  - Scales nutrition values to the exact portion you ate (by grams or natural description, e.g. "2 slices")
  - Falls back to Google Gemini AI when a food isn't in USDA's database (e.g. dosa, samosa) or no listed result fits
- 💪 **Workout logging** — log exercises with sets, reps, and weight; supports multiple exercises per session
- 🔥 **Maintenance calorie calculator** — BMR/TDEE calculation (Mifflin-St Jeor formula) with bulk/cut calorie and macro targets
- 📊 **Progress charts** — daily calories, protein, carbs, and workout volume, visualized with Matplotlib
- 📅 **Daily summaries** — see today's meals/workouts and running totals at a glance
- 🖥️ **Two interfaces** — a terminal app (`main.py`) and a Streamlit web app (`app.py`), both backed by the same SQLite database

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Web Interface | Streamlit |
| Database | SQLite |
| APIs | USDA FoodData Central API, Google Gemini API |
| Data handling | Pandas |
| Visualization | Matplotlib |
| Auth | Python `hashlib` (SHA-256 password hashing) |
| Config | `python-dotenv` for environment variables |

---

## 📂 Project Structure

```
FitTrack/
├── main.py                  # Terminal interface
├── app.py                   # Streamlit web interface
├── auth.py                  # Signup/login, password hashing
├── database.py              # SQLite connection & schema
├── food_tracker.py          # USDA API + Gemini AI fallback, meal logging
├── workout_tracker.py       # Workout logging (terminal & web)
├── charts.py                # Progress visualizations
├── calorie_calculator.py    # BMR/TDEE/macro calculator
├── requirements.txt         # Python dependencies
└── .streamlit/config.toml   # Streamlit display settings
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/fittrack.git
cd fittrack
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your API keys
- **USDA FoodData Central**: [Get a free key here](https://fdc.nal.usda.gov/api-guide.html)
- **Google Gemini**: [Get a free key here](https://aistudio.google.com/apikey)

### 4. Create a `.env` file in the project root
```
USDA_API_KEY=your_usda_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### 5. Run the app

**Terminal version:**
```bash
python main.py
```

**Web version:**
```bash
streamlit run app.py
```

The database (`fittrack.db`) and its tables are created automatically on first run.

---

## 🧠 Design Notes & Challenges Solved

A few real-world problems I ran into while building this, and how I solved them:

- **USDA's "Energy" field has two units** (kcal and kJ) under the same nutrient name — had to explicitly filter by `unitName == "KCAL"` to avoid using the wrong value.
- **USDA values are per 100g**, not per serving — added portion scaling (exact grams, or AI-estimated grams from a natural description like "2 slices").
- **Regional/international foods often aren't in USDA's database** (e.g. dosa, samosa) — added a Gemini AI fallback that estimates nutrition when there's no match, or when none of the USDA results are a good fit.
- **Terminal input vs. web input are fundamentally different** — `select_and_log_food()` (terminal) uses blocking `input()` calls, which don't work in Streamlit's rerun-based model. Built a parallel Streamlit-native flow using `st.session_state` to preserve multi-step state across reruns, while keeping shared logic (nutrient extraction, AI calls, search) in common functions to avoid duplicating business logic.
- **Multi-user data isolation** — added a `users` table with hashed passwords and a `user_id` foreign key on every log table, with all queries filtered by the logged-in user.

---

## 🔭 Future Improvements

- Daily step tracking and calories burned from workouts
- AI-generated meal suggestions based on remaining daily macros
- Migrate from SQLite to PostgreSQL for better concurrent multi-user support at scale

---

## 📸 Screenshots

*(Add screenshots of the Streamlit app here — Home, Log Meal, Charts, etc.)*

---

## 👤 Author

Built by Harsh Namdev as a personal project to learn full-stack development, API integration, and applied AI — built during semester vacation, B.Tech CSE (AIML).
