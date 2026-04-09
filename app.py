from flask import Flask, render_template_string, request
import pymysql
import sys
import os  # IMPORTANT: You were missing this for os.environ

app = Flask(__name__)

# --- Database Connection Configuration ---
def get_db_connection():
    try:
        # On Railway, you must use Environment Variables. 
        # Replace '127.0.0.1' with the Host Railway gives you in the DB tab.
        conn = pymysql.connect(
            user=os.environ.get("DB_USER", "admin_bob"),
            password=os.environ.get("DB_PASS", "Apt3090Password!"),
            host=os.environ.get("DB_HOST", "127.0.0.1"), 
            port=int(os.environ.get("DB_PORT", 3306)),
            database=os.environ.get("DB_NAME", "credit_card_vault")
        )
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to pymysql: {e}")
        # On a server, don't use sys.exit(1) or the whole container crashes.
        # Just return None and handle the error in the route.
        return None

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
    user_id = request.form["user_id"]
    name = request.form["name"]
    card_num = request.form["card_num"]
    cvv = request.form["cvv"]
    expiry = request.form["expiry"]

    conn = get_db_connection()
    if conn is None:
        return "<h1>Error</h1><p>Could not connect to database.</p>"
    
    cur = conn.cursor()

    try:
        # IMPORTANT: PyMySQL uses %s as placeholders, NOT ?
        query = """
            INSERT INTO credit_cards (user_id, card_holder_name, card_num_enc, cvv_enc, expiry_date) 
            VALUES (%s, %s, AES_ENCRYPT(%s, 'verysecretkey'), AES_ENCRYPT(%s, 'verysecretkey'), %s)
        """
        cur.execute(query, (user_id, name, card_num, cvv, expiry))
        conn.commit()
        conn.close()
        return f"<h1>Success!</h1><p>Data for {name} has been encrypted and vaulted.</p><a href='/'>Go Back</a>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    # Get port from Railway environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is required so Railway can route traffic to the container
    app.run(host='0.0.0.0', port=port, debug=False)
