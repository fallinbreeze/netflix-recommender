import streamlit as st
import pandas as pd
import random
from datetime import datetime



# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\falli\OneDrive\Desktop\my code\Jupyter Source File\NetFlix Project\netflix_bilingual_merged_clean.csv")
    if isinstance(df.loc[0, "genre_list"], str):
        df["genre_list"] = df["genre_list"].apply(eval)
    return df

df = load_data()

# --- Title ---
st.title("🎬 Netflix Mood-Based Recommender")
st.markdown("Find the perfect show based on your current mood and viewing time 🎧🍿")

# --- User Preferences ---
st.header("📋 User Preferences")

time_choice = st.selectbox(
    "How much time do you have for watching today?",
    ["< 1 hour", "Around 1 hour", "> 2 hours"]
)

kid_choice = st.radio(
    "Are there kids (under 18) watching with you?",
    ["Yes", "No"]
)

# --- Mood-Based Quiz ---
st.header("🧠 Mood-Based Quiz")

questions = [
    "Q1. What do you feel like doing right now?",
    "Q2. What is your current energy level?",
    "Q3. If you could drink something now, what would you choose?"
]

options = [
    ["Just chilling on the couch, no brain needed",
     "Something exciting to get my heart racing",
     "Something deep and thoughtful",
     "Something fun and cheerful"],

    ["I'm running on 3% battery – save mode please",
     "Just had an energy drink – bring it on",
     "Half-and-half, relaxed but ready",
     "Feeling down, need healing vibes"],

    ["Hot cocoa or milk tea (comfort & warmth)",
     "Black coffee (focused & alert)",
     "Juice or soda (refreshing & fun)",
     "Red wine or cocktail (immersive mood)"]
]

answers = []
for i in range(3):
    answers.append(st.radio(questions[i], options[i], key=f"q{i}"))

# --- Genre Selection ---
st.header("🎯 Genre Preference")
genre_options = {
    "None – Recommend by mood": None,
    "Comedy": ["Comedies", "Family"],
    "Horror / Thriller": ["Horror", "Thriller"],
    "Documentary": ["Documentary"],
    "Action / Adventure": ["Action", "Adventure"],
    "Mystery / Crime": ["Crime", "Mystery"],
    "Romantic / Drama": ["Romantic", "Drama"]
}
genre_choice = st.selectbox("Do you want to pick a genre?", list(genre_options.keys()))

# --- Determine mood ---
if genre_choice == "None – Recommend by mood":
    if answers.count(options[0][0]) >= 2:
        mood = "Chill Mode – Comedy"
        genres = ["Comedies", "Family"]
    elif answers.count(options[0][1]) >= 2:
        mood = "Thrill Seeker – Action"
        genres = ["Action", "Thriller", "Horror"]
    elif answers.count(options[0][2]) >= 2:
        mood = "Deep Thinker – Documentary"
        genres = ["Documentary"]
    elif answers.count(options[0][3]) >= 2:
        mood = "Dopamine Hunter – Romance"
        genres = ["Romantic", "Drama"]
    else:
        mood = "Dark Twist – Thriller"
        genres = ["Horror", "Thriller"]
else:
    mood = "Custom Genre Selected"
    genres = genre_options[genre_choice]

# --- Filtering ---
if time_choice == "< 1 hour":
    df_filtered = df[df["duration_min"] <= 30]
elif time_choice == "Around 1 hour":
    df_filtered = df[(df["duration_min"] > 30) & (df["duration_min"] <= 90)]
else:
    df_filtered = df[df["duration_min"] > 90]

if kid_choice == "Yes":
    excluded = ["Horror", "Thriller", "Crime"]
    df_filtered = df_filtered[~df_filtered["genre_list"].apply(
        lambda g: any(tag in g for tag in excluded) if isinstance(g, list) else False)]

df_filtered = df_filtered[df_filtered["genre_list"].apply(
    lambda g: any(tag in g for tag in genres))]

# --- Show Results ---
st.subheader(f"🎭 Your Viewing Mood: {mood}")
st.write("Based on your answers, here are some recommendations:")

if not df_filtered.empty:
    recommended = df_filtered.sample(min(5, len(df_filtered)), random_state=42)
    for i, row in recommended.iterrows():
        st.markdown(f"**📌 {row['title_zh']} ({row['title_en']})**")
        st.markdown(f"🗓️ {row['release_year']}｜{row['listed_in_zh_en']}｜{row['rating']}｜⏱️ 約 {row['duration_min']} 分鐘")
        st.markdown(f"{row['description']}")
        st.markdown("---")
else:
    st.warning("😥 Sorry, no matching recommendations found.")
