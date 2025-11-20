import streamlit as st
import pandas as pd
import pickle

# ---------------------------
# PAGE CONFIG + CUSTOM CSS
# ---------------------------
st.set_page_config(page_title="Book Recommender", layout="wide")

# LIGHT BLUE BACKGROUND + CLEAN CARD DESIGN
page_bg = """
<style>
    body {
        background-color: #e8f3ff !important;  /* Dim light blue */
    }
    .stApp {
        background-color: #e8f3ff !important;
    }
    .main > div {
        background-color: #e8f3ff !important;
    }

    /* Card Styling */
    .book-card {
        background: white;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.12);
        text-align: center;
        margin-bottom: 20px;
        transition: 0.2s ease;
    }
    .book-card:hover {
        transform: scale(1.03);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.18);
    }
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------------------------
# LOAD DATA
# ---------------------------
books = pd.read_csv("Books.csv", low_memory=False)
ratings = pd.read_csv("Ratings.csv")
users = pd.read_csv("Users.csv")

popular_books = pickle.load(open("popular.pkl", "rb"))
popular_books = popular_books.reset_index(drop=True)

pt = pickle.load(open("pt.pkl", "rb"))
books_final = pickle.load(open("books.pkl", "rb"))
similarity = pickle.load(open("similarity_scores.pkl", "rb"))

book_list = pt.index.tolist()

# ---------------------------
# RECOMMEND FUNCTION
# ---------------------------
def recommend(book_name):
    index = pt.index.get_loc(book_name)
    distances = similarity[index]

    book_list_indexes = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in book_list_indexes:
        temp = books_final[books_final["Book-Title"] == pt.index[i[0]]]

        recommendations.append({
            "title": pt.index[i[0]],
            "author": temp["Book-Author"].values[0],
            "image": temp["Image-URL-M"].values[0]
        })

    return recommendations

# ---------------------------
# SIDEBAR
# ---------------------------
menu = st.sidebar.radio(
    "Select Feature",
    ["Popular Books", "Recommend Books"]
)

# ---------------------------
# POPULAR BOOKS
# ---------------------------
if menu == "Popular Books":
    st.title("Popular Books")

    for i in range(len(popular_books["Book-Title"])):
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(popular_books["Image-URL-M"][i], width=120)

        with col2:
            st.markdown(f"<div class='book-card'>", unsafe_allow_html=True)
            st.subheader(popular_books["Book-Title"][i])
            st.write("Author:", popular_books["Book-Author"][i])
            st.write("Avg Rating:", str(popular_books["avg_rating"][i]))
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# RECOMMEND BOOKS
# ---------------------------
if menu == "Recommend Books":
    st.title("Book Recommendation System")

    selected_book = st.selectbox(
        "Select a Book",
        book_list,
        index=0
    )

    if st.button("Recommend"):
        st.subheader(f"Books similar to **{selected_book}**")
        data = recommend(selected_book)

        cols = st.columns(5)

        for idx, col in enumerate(cols):
            with col:
                st.markdown("<div class='book-card'>", unsafe_allow_html=True)
                st.image(data[idx]["image"])
                st.write(f"{data[idx]['title']}")
                st.write(f"{data[idx]['author']}")
                st.markdown("</div>", unsafe_allow_html=True)
