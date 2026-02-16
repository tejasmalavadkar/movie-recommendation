import streamlit as st
import pandas as pd
import pickle
import urllib.parse
import gdown
import os
import pickle

file_id = "1BG6zfHV-Pww78aydTTze8mq_lGlkTJua"
url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists("similarity.pkl"):
    gdown.download(url, "similarity.pkl", quiet=False)

similarity = pickle.load(open("similarity.pkl", "rb"))


# ================= PAGE CONFIG =================
st.set_page_config(page_title="Top Movies", layout="wide")

# ================= LOAD DATA =================
df = pd.read_csv("movie.csv")
from sklearn.metrics.pairwise import cosine_similarity


# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = 0

if "menu" not in st.session_state:
    st.session_state.menu = "HOME"

PAGE_SIZE = 20

# ================= CSS =================
st.markdown("""
<style>
.stApp { background-color:#0f0f0f; }
.menu-btn button {
    background:#3a3a3a;
    color:white;
    border-radius:10px;
    padding:8px 16px;
    border:none;
    font-weight:600;
}
.menu-btn button:hover {
    background:#525252;
}
.card {
    background:#1a1a1a;
    border-radius:14px;
    padding:12px;
    margin:12px;
    transition:0.3s;
}
.card:hover { transform: scale(1.05); }
.title { color:white; font-size:14px; font-weight:600; margin-top:6px; }
.meta { color:#9ca3af; font-size:12px; }
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='color:#f43f5e;'>🍿 TOP MOVIES</h1>", unsafe_allow_html=True)

# ================= MENU BAR =================
menu_cols = st.columns(7)

menus = [
    ("🏠 HOME", "HOME"),
    ("🎬 MOVIES", "MOVIES"),
    ("🎭 GENRE", "GENRE"),
    ("📅 YEAR", "YEAR"),
    ("🎞 QUALITY", "QUALITY"),
    ("📺 WEB SERIES", "WEB"),
    ("🌎 HOLLYWOOD", "HOLLYWOOD"),
]

for col, (label, key) in zip(menu_cols, menus):
    with col:
        if st.button(label):
            st.session_state.menu = key
            st.session_state.page = 0

# ================= SEARCH =================
search = st.text_input("🔍 Search", placeholder="What are you looking for?")

# ================= FILTER BASED ON MENU =================
filtered_df = df.copy()

if st.session_state.menu == "MOVIES":
    filtered_df = filtered_df[filtered_df["Type"] == "Movie"]

elif st.session_state.menu == "WEB":
    filtered_df = filtered_df[filtered_df["Type"] == "Web Series"]

elif st.session_state.menu == "HOLLYWOOD":
    filtered_df = filtered_df[filtered_df["Language"] == "English"]

elif st.session_state.menu == "GENRE":
    genre = st.selectbox("Select Genre", sorted(df["Genres"].unique()))
    filtered_df = filtered_df[filtered_df["Genres"] == genre]

elif st.session_state.menu == "YEAR":
    year = st.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))
    filtered_df = filtered_df[filtered_df["Year"] == year]

# QUALITY = UI only (acceptable for project)

# ================= SEARCH FILTER =================
if search:
    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(search, case=False)
    ]

# ================= SORT + PAGINATION =================
filtered_df = filtered_df.sort_values("Year", ascending=False).reset_index(drop=True)

start = st.session_state.page * PAGE_SIZE
end = start + PAGE_SIZE
page_df = filtered_df.iloc[start:end]

# ================= GRID DISPLAY =================
st.markdown(f"### 🔥 {st.session_state.menu} CONTENT")

cols = st.columns(5)

for idx, row in page_df.iterrows():
    with cols[idx % 5]:
        url = "https://www.google.com/search?q=" + urllib.parse.quote(row["Title"] + " movie")

        st.markdown(
            f"""
            <a href="{url}" target="_blank" style="text-decoration:none;">
                <div class="card">
                    <img src="{row.get('PosterURL','https://via.placeholder.com/300x450')}"
                         style="width:100%; border-radius:10px;">
                    <div class="title">{row['Title']}</div>
                    <div class="meta">⭐ {row['Rating']} | {row['Year']}</div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

# ================= PAGINATION =================
st.markdown("---")
c1, c2, c3 = st.columns([1,2,1])

with c1:
    if st.button("⬅ Previous") and st.session_state.page > 0:
        st.session_state.page -= 1

with c3:
    if st.button("Next ➡") and end < len(filtered_df):
        st.session_state.page += 1

st.markdown(
    f"<p style='text-align:center;color:gray;'>Showing {start+1}–{min(end,len(filtered_df))} of {len(filtered_df)}</p>",
    unsafe_allow_html=True
)
