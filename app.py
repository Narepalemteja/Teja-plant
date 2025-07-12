from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_class TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    search = request.args.get('search', '')
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    if search:
        c.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students, search=search)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    student_class = request.form['class']
    age = request.form['age']

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, student_class, age) VALUES (?, ?, ?)", (name, student_class, age))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        student_class = request.form['class']
        age = request.form['age']
        c.execute("UPDATE students SET name=?, student_class=?, age=? WHERE id=?", (name, student_class, age, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        c.execute("SELECT * FROM students WHERE id=?", (id,))
        student = c.fetchone()
        conn.close()
        return render_template('edit.html', student=student)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
import os

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
