from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, expression TEXT, result TEXT)")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    init_db()
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get("expression")
    try:
        result = str(eval(expression))
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result))
        conn.commit()
        conn.close()
        return jsonify({'result': result})
    except:
        return jsonify({'result': 'Error'})

@app.route('/history')
def history():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT expression, result FROM history ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)