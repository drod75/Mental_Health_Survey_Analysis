from datetime import datetime
import streamlit as st
from util.supabase import SupabaseScript


@st.cache_resource
def get_supabase_client():
    return SupabaseScript()


supabase = get_supabase_client()

st.title("Student Survey Form:")

with st.form("Student Survey"):
    st.markdown("## Personal Information:")

    with st.expander("Click to expand/collapse Personal Information section"):
        st.markdown("### Age")
        age = st.number_input(
            "Please input your Age!",
            min_value=1,
            max_value=100,
            value=None,
            placeholder="Type something here...",
            icon=":material/person:",
        )

        st.markdown("### Gender")
        gender = st.selectbox(
            "What is your Gender?",
            ("Male", "Female", "They/Them", "Other"),
            placeholder="Select your gender...",
        )

        st.markdown("### Marital Status")
        martial_status = st.selectbox(
            "What is your Marital Status?",
            ("Single", "Married", "Divorced", "Widowed", "Other"),
            placeholder="Select your marital status...",
        )

    st.markdown("## Academic Information:")

    with st.expander("Click to expand/collapse Academic Information section"):
        st.markdown("### College")
        college = st.text_input(
            "Which College are you enrolled in?",
            placeholder="Type your college here...",
            icon=":material/school:",
        )

        st.markdown("### Degree Type")
        degree = st.selectbox(
            "What is your Degree Type?",
            ("Undergraduate", "Graduate", "PhD"),
            placeholder="Select your degree type...",
        )

        st.markdown("### Additional Information")
        year = st.selectbox(
            "What is your Year of Study?",
            ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "Other"),
            placeholder="Select your year of study...",
        )

        st.markdown("### Major")
        major = st.text_input(
            "What is your Major?",
            placeholder="Type your major here...",
            icon=":material/book:",
        )

        st.markdown("### Minor")
        minor = st.text_input(
            "What is your Minor?",
            placeholder="Type your minor here...",
            icon=":material/book:",
        )

        st.markdown("### GPA")
        gpa = st.number_input(
            "What is your GPA?",
            min_value=0.0,
            max_value=4.0,
            value=None,
            step=0.01,
            format="%.2f",
            placeholder="Type your GPA here...",
            icon=":material/percent:",
        )

        st.markdown("### Extracurricular Activities")
        extracurricular = st.selectbox(
            "Are you involved in any Extracurricular Activities?",
            ("Yes", "No"),
            placeholder="Select an option...",
        )

    submitted = st.form_submit_button("Submit")
    if submitted:
        if (
            age is None
            or gender is None
            or martial_status is None
            or college is None
            or degree is None
            or year is None
            or major is None
            or gpa is None
            or extracurricular is None
        ):
            st.error(
                "Please fill in all the required fields!", icon=":material/warning:"
            )
        else:
            st.success("Form submitted successfully!", icon=":material/check:")
            with st.expander("See your submitted information:"):
                st.markdown(
                    f"""
                    - **Age:** {age}
                    - **Gender:** {gender}
                    - **Marital Status:** {martial_status}
                    - **College:** {college}
                    - **Degree Type:** {degree}
                    - **Year of Study:** {year}
                    - **Major:** {major}
                    - **Minor:** {minor if minor else "N/A"}
                    - **GPA:** {gpa}
                    - **Extracurricular Activities:** {extracurricular}
                    
                    """
                )

                entry_data = {
                    "created_at": datetime.now().isoformat(),
                    "Age": age,
                    "Gender": gender,
                    "Marital_Status": martial_status,
                    "College": college,
                    "Degree": degree,
                    "Year": year,
                    "Major": major,
                    "Minor": minor,
                    "GPA": gpa,
                    "Extracurricular": extracurricular,
                }

                supabase.insert_data(table_name="survey_data", data=entry_data)
