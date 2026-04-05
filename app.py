from flask import Flask, render_template

app = Flask(__name__)

# ================= STATIC DATA =================

software_data = [
    (1, "CodeBlocks (Data Structures)", "20.03", 1),
    (2, "MySQL", "8.0", 1),
    (3, "Java JDK", "21", 1),
    (4, "Logisim (DLD Tool)", "2.7", 1)
]

errors_data = {
    1: [("Compiler Error", "Check compiler settings", "#")],
    2: [("Connection Error", "Check MySQL service", "#")],
    3: [("JDK Not Found", "Set JAVA_HOME properly", "#")],
    4: [("Circuit Error", "Check connections", "#")]
}

installation_data = {
    1: ("CodeBlocks (Data Structures)", "Step 1: Download CodeBlocks\nStep 2: Install\nStep 3: Run"),
    2: ("MySQL", "Step 1: Download MySQL\nStep 2: Install\nStep 3: Configure"),
    3: ("Java JDK", "Step 1: Download JDK\nStep 2: Install\nStep 3: Set Path"),
    4: ("Logisim", "Step 1: Download Logisim\nStep 2: Run .jar file")
}

# ================= HOME =================
@app.route('/')
def home():
    return render_template('index.html')

# ================= SUBJECTS =================
@app.route('/subjects')
def subjects():
    return render_template('software.html', software=software_data)

# ================= TROUBLESHOOT =================
@app.route('/troubleshoot')
def troubleshoot():
    all_errors = []
    for e in errors_data.values():
        all_errors.extend(e)
    return render_template('errors.html', errors=all_errors)

# ================= CONTACT =================
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ================= SEMESTER SOFTWARE =================
@app.route('/software/<int:semester_id>')
def show_software(semester_id):
    filtered = [s[:3] for s in software_data if s[3] == semester_id]
    return render_template("software.html", software=filtered)

# ================= ERRORS =================
@app.route('/errors/<int:software_id>')
def show_errors(software_id):
    errors = errors_data.get(software_id, [])
    return render_template("errors.html", errors=errors)

# ================= INSTALLATION =================
@app.route('/installation/<int:software_id>')
def show_installation(software_id):
    data = installation_data.get(software_id, ("Demo Software", "No data available"))
    return render_template("installation.html", data=data)

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
