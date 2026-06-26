from flask import Flask, render_template, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

def db():

    conn = sqlite3.connect("quotes.db")

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    author TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS favorites(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    author TEXT
    )
    """)

    conn.commit()
    conn.close()

db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_quote')
def get_quote():

    try:

        response = requests.get(
        "https://api.quotable.io/random"
        )

        data = response.json()

        quote = data['content']
        author = data['author']

    except:

        quote = "Success is built one day at a time."
        author = "QuoteVerse"

    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()

    cur.execute(
    "INSERT INTO history(quote,author) VALUES(?,?)",
    (quote,author)
    )

    conn.commit()
    conn.close()

    return jsonify({
    "quote":quote,
    "author":author
    })

@app.route('/history')
def history():

    conn = sqlite3.connect("quotes.db")

    cur = conn.cursor()

    cur.execute("""
    SELECT quote,author
    FROM history
    ORDER BY id DESC
    LIMIT 20
    """)

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

@app.route('/favorite',methods=['POST'])
def favorite():

    data=request.json

    conn=sqlite3.connect("quotes.db")

    cur=conn.cursor()

    cur.execute(
    "INSERT INTO favorites(quote,author) VALUES(?,?)",
    (
    data['quote'],
    data['author']
    )
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})

if __name__=="__main__":
    app.run(debug=True)