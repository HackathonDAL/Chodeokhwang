import pandas as pd


# =========================
# 1. Load CSV files
# =========================

courses_df = pd.read_csv("../data/courses.csv")
fields_df = pd.read_csv("../data/course_field_matrix.csv")


# =========================
# 2. Test student data
# =========================

student_courses = [
    {"course_code": "COSE211", "grade": 4.0, "interest": 5},
    {"course_code": "COSE213", "grade": 4.5, "interest": 4},
    {"course_code": "COSE214", "grade": 3.5, "interest": 5},
]


# =========================
# 3. Calculate course score
# =========================

def calculate_course_score(grade, interest):
    normalized_grade = grade / 4.5
    normalized_interest = interest / 5

    course_score = (
        normalized_grade * 0.4
        + normalized_interest * 0.6
    )

    return course_score


# =========================
# 4. Calculate student profile
# =========================

def calculate_student_profile(student_courses):
    fields = [
        column for column in fields_df.columns
        if column != "course_code"
    ]

    total_scores = {
        field: 0.0
        for field in fields
    }

    total_relevance = {
        field: 0.0
        for field in fields
    }

    for student_course in student_courses:

        course_code = student_course["course_code"]
        grade = student_course["grade"]
        interest = student_course["interest"]

        course_score = calculate_course_score(
            grade,
            interest
        )

        course_rows = fields_df[
            fields_df["course_code"] == course_code
        ]

        if course_rows.empty:
            print(f"Warning: Course {course_code} not found.")
            continue

        course_row = course_rows.iloc[0]

        for field in fields:
            relevance = course_row[field]

            total_scores[field] += course_score * relevance
            total_relevance[field] += relevance

    results = []

    for field in fields:
        if total_relevance[field] > 0:
            final_score = (
                total_scores[field]
                / total_relevance[field]
            )
        else:
            final_score = 0

        results.append({
            "field": field,
            "score": final_score,
            "percentage": round(final_score * 100, 2)
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="score",
        ascending=False
    ).reset_index(drop=True)

    return results_df


# =========================
# 5. Run recommendation
# =========================

recommendations = calculate_student_profile(student_courses)


print("\n" + "=" * 50)
print("RECOMMENDED ACADEMIC FIELDS")
print("=" * 50)

print(
    recommendations[
        ["field", "percentage"]
    ].to_string(index=False)
)


print("\n" + "=" * 50)
print("TOP 3 RECOMMENDATIONS")
print("=" * 50)

for index, row in recommendations.head(3).iterrows():
    print(
        f"{index + 1}. {row['field']} "
        f"({row['percentage']}%)"
    )
