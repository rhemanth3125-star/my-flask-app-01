import re
from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)


# ============================================================
# DATABASE CONNECTION
# Existing local MySQL database: fieldproject
# ============================================================

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hemanth",
            database="fieldproject",
            port=3306
        )

        print("===================================")
        print("DATABASE CONNECTED SUCCESSFULLY")
        print("===================================")

        return db

    except mysql.connector.Error as err:
        print("===================================")
        print("DATABASE ERROR")
        print(err)
        print("===================================")
        return None


def render_db_error(message="Unable to connect to the database."):
    return render_template("db_error.html", message=message), 503


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# SUBJECTS - ALL
# ============================================================

@app.route("/subjects")
def subjects():

    db = get_db_connection()

    if db is None:
        return render_db_error()

    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT DISTINCT
            CASE
                WHEN software_name IN ('C Programming (GCC)', 'Turbo C++')
                    THEN 'Programming in C'

                WHEN software_name = 'Python'
                    THEN 'Python Programming'

                WHEN software_name = 'CodeBlocks (Data Structures)'
                    THEN 'Data Structures'

                WHEN software_name = 'MySQL'
                    THEN 'Database Management Systems'

                WHEN software_name = 'Java JDK'
                    THEN 'Object Oriented Programming'

                WHEN software_name = 'Logisim (DLD Tool)'
                    THEN 'Digital Logic Design'

                WHEN software_name = 'VS Code (Frontend Development)'
                    THEN 'Frontend Development'

                WHEN software_name = 'Linux (Ubuntu)'
                    THEN 'Operating Systems'

                ELSE software_name
            END AS subject_name,
            semester_id

        FROM software

        ORDER BY semester_id, subject_name
    """)

    subjects = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("subjects.html", subjects=subjects)


# ============================================================
# SUBJECTS BY SEMESTER
# ============================================================

@app.route("/subjects/<int:semester_id>")
def semester_subjects(semester_id):

    db = get_db_connection()

    if db is None:
        return render_db_error()

    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT DISTINCT
            CASE
                WHEN software_name IN ('C Programming (GCC)', 'Turbo C++')
                    THEN 'Programming in C'

                WHEN software_name = 'Python'
                    THEN 'Python Programming'

                WHEN software_name = 'CodeBlocks (Data Structures)'
                    THEN 'Data Structures'

                WHEN software_name = 'MySQL'
                    THEN 'Database Management Systems'

                WHEN software_name = 'Java JDK'
                    THEN 'Object Oriented Programming'

                WHEN software_name = 'Logisim (DLD Tool)'
                    THEN 'Digital Logic Design'

                WHEN software_name = 'VS Code (Frontend Development)'
                    THEN 'Frontend Development'

                WHEN software_name = 'Linux (Ubuntu)'
                    THEN 'Operating Systems'

                ELSE software_name
            END AS subject_name,
            semester_id

        FROM software

        WHERE semester_id = %s

        ORDER BY subject_name
    """, (semester_id,))

    subjects = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("subjects.html", subjects=subjects)


# ============================================================
# SOFTWARE FOR SELECTED SEMESTER
# ============================================================

@app.route("/software/<int:semester_id>")
def show_software(semester_id):

    db = get_db_connection()

    if db is None:
        return render_db_error()

    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT software_id, software_name, version

        FROM software

        WHERE semester_id = %s

        ORDER BY software_id
    """, (semester_id,))

    software = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("software.html", software=software)


# ============================================================
# COMMON ERRORS
# ============================================================

@app.route("/errors/<int:software_id>")
def show_errors(software_id):

    db = get_db_connection()

    if db is None:
        return render_db_error()

    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT error_message, solution, youtube_link

        FROM errors

        WHERE software_id = %s
    """, (software_id,))

    errors = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "errors.html",
        errors=errors,
        software_id=software_id
    )


# ============================================================
# ERROR CHAT / SEARCH
# ============================================================

@app.route("/errors/<int:software_id>/chat", methods=["POST"])
def errors_chat(software_id):

    db = get_db_connection()

    if db is None:
        return jsonify({
            "response": "Database is currently unavailable. Please try again."
        }), 503

    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()

    if not question:
        db.close()

        return jsonify({
            "response": "Please type a question about the error to get help."
        })


    question_words = re.findall(
        r"\w+",
        question.lower()
    )


    stopwords = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "if",
        "in",
        "on",
        "for",
        "to",
        "is",
        "it",
        "that",
        "this",
        "these",
        "those",
        "with",
        "only",
        "anytime",
        "always",
        "please",
        "correct",
        "given",
        "when"
    }


    keywords = [
        word
        for word in question_words
        if word not in stopwords
    ]


    if not keywords:

        db.close()

        return jsonify({
            "response":
            "Please ask about a specific error term, "
            "such as 'gcc', 'undefined reference', or 'path'."
        })


    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT error_message, solution

        FROM errors

        WHERE software_id = %s
    """, (software_id,))

    rows = cursor.fetchall()

    cursor.close()
    db.close()


    matches = []


    for error_message, solution in rows:

        combined = (
            f"{error_message} {solution}"
        ).lower()

        if any(
            re.search(
                rf"\b{re.escape(keyword)}\b",
                combined
            )
            for keyword in keywords
        ):
            matches.append(
                (error_message, solution)
            )


    if matches:

        response_lines = [
            "I found these related error details from the common errors list:"
        ]

        for error_message, solution in matches:

            response_lines.append(
                f"Error: {error_message}"
            )

            response_lines.append(
                f"Solution: {solution}"
            )

            response_lines.append("")


        response_text = "\n".join(
            response_lines
        ).strip()

    else:

        response_text = (
            "I couldn't find an exact match in the current list. "
            "Try a more specific keyword like 'gcc', "
            "'undefined reference', or 'path'."
        )


    return jsonify({
        "response": response_text
    })


# ============================================================
# INSTALLATION GUIDE
# Reads installation_steps directly from MySQL database
# ============================================================

@app.route("/installation/<int:software_id>")
def show_installation(software_id):

    db = get_db_connection()

    if db is None:
        return render_db_error()

    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT software_name, installation_steps

        FROM software

        WHERE software_id = %s
    """, (software_id,))

    data = cursor.fetchone()

    cursor.close()
    db.close()


    if data is None:

        return render_db_error(
            "Installation guide was not found for this software ss."
        )


    return render_template(
        "installation.html",
        data=data
    )


# ============================================================
# CONTACT
# ============================================================

@app.route("/contact")
def contact():

    return render_template("contact.html")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)