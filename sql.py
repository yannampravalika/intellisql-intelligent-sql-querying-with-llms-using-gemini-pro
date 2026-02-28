import sqlite3

# Connect to SQLite DB (creates new data.db)
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    student_class TEXT,
    marks INTEGER,
    company TEXT
)
""")

# Insert data
students = [
    ("Sijo", "BTech", 75, "JSM"),
    ("Lijo", "MTech", 69, "TCS"),
    ("Rijo", "BSc", 79, "WIPRO"),
    ("Sibin", "MSc", 89, "INFOSYS"),
    ("Disha", "MCom", 99, "Cyient")
]

cursor.executemany(
    "INSERT INTO students VALUES (?, ?, ?, ?)",
    students
)

# Fetch and display
print("Inserted records:")
for row in cursor.execute("SELECT * FROM students"):
    print(row)
connection.commit()
connection.close()
