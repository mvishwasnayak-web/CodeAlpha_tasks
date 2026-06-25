from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------------------------
# Database Initialization
# ---------------------------

def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT UNIQUE
        )
    """)

    # Stats table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            duplicates_prevented INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO stats
        (id, duplicates_prevented)
        VALUES (1, 0)
    """)

    conn.commit()
    conn.close()


init_db()

# ---------------------------
# Home Dashboard
# ---------------------------

@app.route("/")
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Total Records
    cursor.execute("SELECT COUNT(*) FROM records")
    total_records = cursor.fetchone()[0]

    # Unique Records
    unique_records = total_records

    # Duplicates Prevented
    cursor.execute("""
        SELECT duplicates_prevented
        FROM stats
        WHERE id = 1
    """)

    duplicates_prevented = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        total_records=total_records,
        unique_records=unique_records,
        duplicates_prevented=duplicates_prevented
    )

# ---------------------------
# Add Record
# ---------------------------

@app.route("/add", methods=["GET", "POST"])
def add_record():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO records
                (name, email, phone)
                VALUES (?, ?, ?)
            """,
            (name, email, phone))

            conn.commit()

            message = "Record Added Successfully"

        except sqlite3.IntegrityError:

            cursor.execute("""
                UPDATE stats
                SET duplicates_prevented =
                duplicates_prevented + 1
                WHERE id = 1
            """)

            conn.commit()

            message = "Duplicate Record Detected"

        conn.close()

        return render_template(
            "result.html",
            message=message,
            success=(message == "Record Added Successfully")
        )

    return render_template("add.html")

# ---------------------------
# View Records
# ---------------------------

@app.route("/records")
def records():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM records
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "records.html",
        records=records
    )

# ---------------------------
# Search Records
# ---------------------------

@app.route("/search", methods=["GET", "POST"])
def search():

    results = []

    if request.method == "POST":

        keyword = request.form["search"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM records
            WHERE
            name LIKE ?
            OR email LIKE ?
            OR phone LIKE ?
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        results = cursor.fetchall()

        conn.close()

    return render_template(
        "search.html",
        results=results
    )

# ---------------------------
# Run Application
# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)