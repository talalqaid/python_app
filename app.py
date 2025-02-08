from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection helper function
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the students table if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            major TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

# Routes
@app.route("/")
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/show", methods=["GET","POST"])
def show_students():
    students=[]
    if request.method=="POST":
        major = request.form["major"]
        conn = get_db_connection()
        students = conn.execute("SELECT * FROM students WHERE major LIKE ?", ('%' + major + '%',)).fetchall()
        conn.close()
    return render_template("show_students.html", students=students)

@app.route("/add", methods=["GET","POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        major = request.form["major"]

        conn = get_db_connection()
        conn.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_student.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        major = request.form["major"]

        conn.execute("UPDATE students SET name = ?, age = ?, major = ? WHERE id = ?", (name, age, major, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("edit_student.html", student=student)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
