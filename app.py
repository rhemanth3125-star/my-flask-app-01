from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
try:
    db = mysql.connector.connect(
        host="localhost",   # will fail on Render but handled
        user="root",
        password="hemanth",
        database="fieldproject"
    )
    print("Database Connected")
except:
    db = None
    print("Database NOT connected")

# ================= HOME =================
@app.route('/')
def home():
    return render_template('index.html')

# ================= SUBJECTS =================
@app.route('/subjects')
def subjects():
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT software_id, software_name, version FROM software")
        software = cursor.fetchall()
    else:
        software = [(1, "Demo Software", "1.0")]  # fallback data
    return render_template('software.html', software=software)

# ================= TROUBLESHOOT =================
@app.route('/troubleshoot')
def troubleshoot():
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT error_message, solution, youtube_link FROM errors")
        errors = cursor.fetchall()
    else:
        errors = [("Sample Error", "Sample Solution", "#")]
    return render_template('errors.html', errors=errors)

# ================= CONTACT =================
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ================= SEMESTER SOFTWARE =================
@app.route('/software/<int:semester_id>')
def show_software(semester_id):
    if db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT software_id, software_name, version FROM software WHERE semester_id = %s",
            (semester_id,)
        )
        software = cursor.fetchall()
    else:
        software = [(1, "Demo Software", "1.0")]
    return render_template("software.html", software=software)

# ================= ERRORS =================
@app.route('/errors/<int:software_id>')
def show_errors(software_id):
    if db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT error_message, solution, youtube_link FROM errors WHERE software_id = %s",
            (software_id,)
        )
        errors = cursor.fetchall()
    else:
        errors = [("Sample Error", "Sample Solution", "#")]
    return render_template("errors.html", errors=errors)

# ================= INSTALLATION =================
@app.route('/installation/<int:software_id>')
def show_installation(software_id):
    if db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT software_name, installation_steps FROM software WHERE software_id = %s",
            (software_id,)
        )
        data = cursor.fetchone()
    else:
        data = ("Demo Software", "Step 1: Install\nStep 2: Run")
    return render_template("installation.html", data=data)

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)