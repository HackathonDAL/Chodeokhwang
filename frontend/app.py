import streamlit as st
import pandas as pd
import sys
import os


# Find the backend folder
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

from scoring import calculate_student_profile


# Page configuration
st.set_page_config(
    page_title="KU Compass",
    page_icon="🧭"
)


# Load courses
courses_df = pd.read_csv("../data/courses.csv")


# Title
st.title("🧭 KU Compass")

st.write(
    "Find academic fields that match your courses, grades, and interests."
)


# Course selection
st.header("Select your courses")

selected_courses = st.multiselect(
    "Choose the courses you have taken:",
    courses_df["course_code"].tolist()
)


student_courses = []


# Input for each selected course
for course_code in selected_courses:

    course_name = courses_df.loc[
        courses_df["course_code"] == course_code,
        "course_name"
    ].iloc[0]

    st.subheader(f"{course_code} — {course_name}")

    grade = st.number_input(
        f"Grade for {course_code}",
        min_value=0.0,
        max_value=4.5,
        value=3.5,
        step=0.5,
        key=f"grade_{course_code}"
    )

    interest = st.slider(
        f"Interest in {course_code}",
        min_value=1,
        max_value=5,
        value=3,
        key=f"interest_{course_code}"
    )

    student_courses.append({
        "course_code": course_code,
        "grade": grade,
        "interest": interest
    })


# Recommendation button
if st.button("Get Recommendations"):

    if not student_courses:

        st.warning("Please select at least one course.")

    else:

        recommendations = calculate_student_profile(
            student_courses
        )

        st.header("Your Recommended Fields")

        st.dataframe(
            recommendations[
                ["field", "percentage"]
            ],
            use_container_width=True
        )

        st.subheader("Top 3 Recommendations")

        for index, row in recommendations.head(3).iterrows():

            st.write(
                f"**{index + 1}. {row['field']}** — "
                f"{row['percentage']}%"
            )
