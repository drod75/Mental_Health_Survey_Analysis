import streamlit as st

st.set_page_config(
    page_title="Studet Survey Analysis",
    page_icon="🏫",
)
pages = [
    st.Page("pages\streamilt-form.py", title="Form Submission", default=True),
    st.Page("pages\streamlit-dashboard.py", title="Survey Analytics"),
]


pg = st.navigation(pages, position="top")
pg.run()
