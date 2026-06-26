from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("coffee.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS coffee(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        votes INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vote_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coffee_name TEXT,
        vote_time TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM coffee")
    count = cur.fetchone()[0]

    if count == 0:
        coffees = [
            ("Espresso",95),
            ("Latte",120),
            ("Cappuccino",88),
            ("Mocha",70),
            ("Cold Brew",60),
            ("Americano",45)
        ]

        cur.executemany(
            "INSERT INTO coffee(name,votes) VALUES(?,?)",
            coffees
        )

    conn.commit()
    conn.close()

@app.route('/')
def home():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM coffee ORDER BY votes DESC")
    coffees = cur.fetchall()

    cur.execute("SELECT SUM(votes) FROM coffee")
    total_votes = cur.fetchone()[0]

    cur.execute("""
    SELECT * FROM vote_history
    ORDER BY id DESC
    LIMIT 10
    """)
    history = cur.fetchall()

    max_vote = coffees[0]["votes"] if coffees else 1

    conn.close()

    return render_template(
        "index.html",
        coffees=coffees,
        total_votes=total_votes,
        history=history,
        max_vote=max_vote
    )

@app.route('/vote/<int:id>')
def vote(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE coffee SET votes=votes+1 WHERE id=?",
        (id,)
    )

    cur.execute(
        "SELECT name FROM coffee WHERE id=?",
        (id,)
    )

    coffee_name = cur.fetchone()["name"]

    cur.execute(
        """
        INSERT INTO vote_history
        (coffee_name,vote_time)
        VALUES (?,?)
        """,
        (
            coffee_name,
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )
    )

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add():

    coffee = request.form['coffee']

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO coffee(name,votes) VALUES(?,0)",
        (coffee,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/reset')
def reset():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE coffee SET votes=0")

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/export')
def export():

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT name,votes FROM coffee"
    )

    data = cur.fetchall()

    conn.close()

    with open(
        "coffee_report.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["Coffee","Votes"]
        )

        for row in data:
            writer.writerow(
                [row["name"],row["votes"]]
            )

    return send_file(
        "coffee_report.csv",
        as_attachment=True
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)