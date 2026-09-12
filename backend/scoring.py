import pandas as pd

# Leer los archivos CSV
courses_df = pd.read_csv("data/courses.csv")
fields_df = pd.read_csv("data/course_field_matrix.csv")

# Mostrar los datos
print("COURSES:")
print(courses_df.head())

print("\nFIELD MATRIX:")
print(fields_df.head())
