import streamlit as st
import pandas as pd
import urllib.parse

# ================= PAGE CONFIG =================
st.set_page_config(page_title="MovieVerse", layout="wide")

# ================= LOAD DATA =================
df = pd.read_csv("movie.csv")

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = 0

if "menu" not in st.session_state:
    st.session_state.menu = "HOME"

PAGE_SIZE = 20

# ================= NETFLIX STYLE CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #0f172a, #020617);
}

/* Header */
.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #ff4b6e;
    margin-bottom: 5px;
}

.subtitle {
    color: #9ca3af;
    margin-bottom: 30px;
}

/* Menu Buttons */
.stButton > button {
    background: #1e293b;
    color: white;
    border-radius: 25px;
    padding: 8px 18px;
    border: none;
    font-weight: 600;
    transition: 0.3s;
}
.stButton > button:hover {
    background: #ff4b6e;
    transform: scale(1.05);
}

/* Movie Card */
.card {
    background: #1e293b;
    border-radius: 16px;
    padding: 12px;
    transition: 0.3s ease-in-out;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}
.card:hover {
    transform: scale(1.07);
    box-shadow: 0 10px 30px rgba(255,75,110,0.6);
}

/* Title */
.title {
    color: white;
    font-size: 16px;
    font-weight: 700;
    margin-top: 8px;
}

/* Meta */
.meta {
    color: #9ca3af;
    font-size: 13px;
}

/* Search */
.stTextInput > div > div > input {
    background-color: #1e293b;
    color: white;
    border-radius: 20px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<div class='main-title'>🎬 MovieVerse</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Discover Top Movies & Web Series</div>", unsafe_allow_html=True)

# ================= MENU =================
menu_cols = st.columns(6)

menus = [
    ("🏠 HOME", "HOME"),
    ("🎬 MOVIES", "MOVIES"),
    ("📺 WEB SERIES", "WEB"),
    ("🌎 HOLLYWOOD", "HOLLYWOOD"),
    ("🎭 GENRE", "GENRE"),
    ("📅 YEAR", "YEAR"),
]

for col, (label, key) in zip(menu_cols, menus):
    with col:
        if st.button(label):
            st.session_state.menu = key
            st.session_state.page = 0

# ================= SEARCH =================
search = st.text_input("🔍 Search movies...")

# ================= FILTER =================
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

# Search filter
if search:
    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(search, case=False, na=False)
    ]

# Sort
filtered_df = filtered_df.sort_values("Year", ascending=False).reset_index(drop=True)

# Pagination
start = st.session_state.page * PAGE_SIZE
end = start + PAGE_SIZE
page_df = filtered_df.iloc[start:end]

# ================= DISPLAY =================
st.markdown(f"### 🔥 {st.session_state.menu} CONTENT")

cols = st.columns(5)

for idx, row in page_df.iterrows():
    with cols[idx % 5]:
        google_url = "https://www.google.com/search?q=" + urllib.parse.quote(row["Title"] + " movie")

        st.markdown(
            f"""
            <a href="{google_url}" target="_blank" style="text-decoration:none;">
                <div class="card">
                    <img src="{row.get('PosterURL','https://via.placeholder.com/300x450')}"
                         style="width:100%; border-radius:12px;">
                    <div class="title">{row['Title']}</div>
                    <div class="meta">⭐ {row['Rating']} | 📅 {row['Year']}</div>
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
