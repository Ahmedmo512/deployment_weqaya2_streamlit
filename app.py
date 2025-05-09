import streamlit as st


st.set_page_config(page_title="Weqaya", layout="wide")
# Navigation
PAGES = {
    "Home": r"home_page.py",
    "Hypertension": r"first.py",
    "Diabetes":r"second.py",
    "Stroke":r"third.py"
}

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", list(PAGES.keys()))

# Display the selected page
if page == "Home":
    exec(open(PAGES["Home"], encoding="utf-8").read())
elif page == "Hypertension":
    exec(open(PAGES["Hypertension"]).read())
elif page == "Diabetes":
    with open(PAGES["Diabetes"], "r", encoding="utf-8") as f:
        content = f.read()

# Clean any bad characters like non-breaking spaces
    cleaned_content = content.replace("\u00A0", " ")

# Execute the cleaned code
    exec(cleaned_content)
else:
    exec(open(PAGES["Stroke"], encoding="utf-8").read())
