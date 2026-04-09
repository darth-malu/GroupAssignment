from flask import Flask, render_template_string, request
import mariadb
import sys

app = Flask(__name__)


# --- Database Connection Configuration ---
def get_db_connection():
    try:
        conn = mariadb.connect(
            user="admin_bob",
            password="Apt3090Password!",
            host="127.0.0.1",
            port=3306,
            database="credit_card_vault",
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)


# --- The HTML Form (The "UI") ---
html_form = """
<!DOCTYPE html>
<html>
<head><title>Credit Card Vault</title></head>
<body>
    <h2>Secure Credit Card Ingestion</h2>
    <form method="POST" action="/submit">
        <label>User ID:</label><br><input type="text" name="user_id" required><br><br>
        <label>Card Holder Name:</label><br><input type="text" name="name" required><br><br>
        <label>Card Number:</label><br><input type="text" name="card_num" required><br><br>
        <label>CVV:</label><br><input type="text" name="cvv" required><br><br>
        <label>Expiry Date:</label><br><input type="date" name="expiry" required><br><br>
        <button type="submit">Vault Encrypted Data</button>
    </form>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(html_form)


@app.route("/submit", methods=["POST"])
def submit():
    # 1. Capture data from the web form
    user_id = request.form["user_id"]
    name = request.form["name"]
    card_num = request.form["card_num"]
    cvv = request.form["cvv"]
    expiry = request.form["expiry"]

    # 2. Connect to MariaDB
    conn = get_db_connection()
    cur = conn.cursor()

    # 3. Encrypt and Insert (Using your AES logic)
    try:
        query = """
            INSERT INTO credit_cards (user_id, card_holder_name, card_num_enc, cvv_enc, expiry_date) 
            VALUES (?, ?, AES_ENCRYPT(?, 'verysecretkey'), AES_ENCRYPT(?, 'verysecretkey'), ?)
        """
        cur.execute(query, (user_id, name, card_num, cvv, expiry))
        conn.commit()
        conn.close()
        return f"<h1>Success!</h1><p>Data for {name} has been encrypted and vaulted.</p><a href='/'>Go Back</a>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"


if __name__ == "__main__":
    # Runs the web server locally on port 5000
    app.run(debug=True, port=5000)
