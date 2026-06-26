from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        status TEXT,
        workload INTEGER
    )
    """)

    cur.execute("SELECT COUNT(*) FROM employees")
    count = cur.fetchone()[0]

    if count == 0:
        employees = [
            ("Alex Rivers","Senior Developer","Available",40),
            ("Samantha Chen","UX Designer","Busy",80),
            ("Jordan Taylor","Project Manager","Available",30),
            ("Maria Garcia","Marketing Lead","Busy",75),
            ("David Lee","AI Engineer","Available",20)
        ]

        cur.executemany(
            "INSERT INTO employees(name,role,status,workload) VALUES(?,?,?,?)",
            employees
        )

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = connect_db()
    employees = conn.execute(
        "SELECT * FROM employees"
    ).fetchall()
    conn.close()

    return render_template(
        "index.html",
        employees=employees
    )

@app.route("/toggle/<int:id>", methods=["POST"])
def toggle(id):

    conn = connect_db()

    emp = conn.execute(
        "SELECT * FROM employees WHERE id=?",
        (id,)
    ).fetchone()

    new_status = "Busy"

    if emp["status"] == "Busy":
        new_status = "Available"

    conn.execute(
        "UPDATE employees SET status=? WHERE id=?",
        (new_status,id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "status": new_status
    })

@app.route("/stats")
def stats():

    conn = connect_db()

    total = conn.execute(
        "SELECT COUNT(*) FROM employees"
    ).fetchone()[0]

    available = conn.execute(
        "SELECT COUNT(*) FROM employees WHERE status='Available'"
    ).fetchone()[0]

    busy = total - available

    health = round((available/total)*100)

    conn.close()

    return jsonify({
        "total": total,
        "available": available,
        "busy": busy,
        "health": health,
        "time": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == "__main__":
    init_db()
    app.run(debug=True)