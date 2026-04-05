from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# ================= DATABASE CONNECTION (AIVEN) =================
db = mysql.connector.connect(
    host="mysql-e848005-rhemanth3125-d59b.c.aivencloud.com",
    user="avnadmin",
    password="AVNS_LPZg06nD745cyaq4S-D",   # 🔴 paste your Aiven password here
    database="defaultdb",
    port=27568
)

# ================= HOME =================
@app.route('/')
def home():
    return render_template('index.html')


# ================= SUBJECTS =================
@app.route('/subjects')
def subjects():
    cursor = db.cursor()
    cursor.execute("SELECT software_id, software_name, version FROM software")
    software = cursor.fetchall()
    return render_template('software.html', software=software)


# ================= TROUBLESHOOT =================
@app.route('/troubleshoot')
def troubleshoot():
    cursor = db.cursor()
    cursor.execute("SELECT error_message, solution, youtube_link FROM errors")
    errors = cursor.fetchall()
    return render_template('errors.html', errors=errors)


# ================= CONTACT =================
@app.route('/contact')
def contact():
    return render_template('contact.html')


# ================= SEMESTER BASED SOFTWARE =================
@app.route('/software/<int:semester_id>')
def show_software(semester_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT software_id, software_name, version FROM software WHERE semester_id = %s",
        (semester_id,)
    )
    software = cursor.fetchall()
    return render_template("software.html", software=software)


# ================= ERRORS =================
@app.route('/errors/<int:software_id>')
def show_errors(software_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT error_message, solution, youtube_link FROM errors WHERE software_id = %s",
        (software_id,)
    )
    errors = cursor.fetchall()
    return render_template("errors.html", errors=errors)


# ================= INSTALLATION =================
@app.route('/installation/<int:software_id>')
def show_installation(software_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT software_name, installation_steps FROM software WHERE software_id = %s",
        (software_id,)
    )
    data = cursor.fetchone()
    return render_template("installation.html", data=data)


# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
