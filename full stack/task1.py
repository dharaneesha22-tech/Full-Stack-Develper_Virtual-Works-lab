from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()

    conn.close()

    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    note = request.form['note']

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO notes (content) VALUES (?)", (note,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)