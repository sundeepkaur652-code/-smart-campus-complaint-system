from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return "<h1>Welcome to Smart Campus Complaint Management System</h1>"


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        roll_no = request.form['roll_no']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()

        try:

            cursor.execute(
                '''
                INSERT INTO users
                (name, roll_no, email, password)
                VALUES (?, ?, ?, ?)
                ''',
                (name, roll_no, email, password)
            )

            conn.commit()

            return '''
            <h2>✅ Registration Successful!</h2>
            <a href="/login">Go To Login</a>
            '''

        except sqlite3.IntegrityError:

            return '''
            <h2>⚠ Email already registered!</h2>
            <a href="/login">Login Here</a>
            '''

        finally:
            conn.close()

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return render_template(
                'dashboard.html',
                name=user[1]
            )
        else:
            return "Invalid Email or Password"

    return render_template('login.html')


# Complaint Page
@app.route('/complaint', methods=['GET', 'POST'])
def complaint():

    if request.method == 'POST':

        complaint_type = request.form['type']
        description = request.form['description']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO complaints
            (complaint_type, description, status)
            VALUES (?, ?, ?)
            ''',
            (complaint_type, description, "Pending")
        )

        conn.commit()
        conn.close()

        return render_template('success.html')

    return render_template('complaint.html')


# Student View Complaints
@app.route('/mycomplaints')
def mycomplaints():

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")

    complaints = cursor.fetchall()

    conn.close()

    return render_template(
        'view_complaints.html',
        complaints=complaints
    )


# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            return redirect('/admin_dashboard')

        return "Invalid Admin Credentials"

    return render_template('admin_login.html')


# Admin Dashboard


# Resolve Complaint
@app.route('/admin_dashboard')
def admin_dashboard():

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin_dashboard.html',
        complaints=complaints,
        total=total,
        pending=pending,
        resolved=resolved
    )
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
