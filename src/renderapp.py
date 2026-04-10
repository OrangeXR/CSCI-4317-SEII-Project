from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from renderdatabase import get_all_assignments, add_assignment, update_assignment, delete_assignment, get_assignment, get_user_by_username, get_user_by_id, update_profile_picture 
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "super-secret-key"   # required for session

# ============================================================================================================================
# Login - handles user login using username and password; successful login redirects to index, if login fails returns to login
# ============================================================================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)

        if user and check_password_hash(user["password_hash"], password): # <---------------- checks password with hashed password stored in astra.db
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")



# ===================================================
# Logout - clears session and redirects user to login
# ===================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



# =====================================================================================
# PROFILE PAGE + UPLOAD - profile page for user that allows user to upload profile_pic
# =====================================================================================
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    user = get_user_by_id(user_id)

    if request.method == "POST":
        file = request.files.get("profile_pic")

        if file and file.filename != "":
            # Ensure folder exists
            upload_folder = os.path.join(BASE_DIR, "static", "profile_pics")  # <------------------  Path to profile_pic upload folder
            os.makedirs(upload_folder, exist_ok=True)

            filename = f"user_{user_id}.png"
            filepath = os.path.join(upload_folder, filename) # <------------------ adds full path together

            file.save(filepath)
            update_profile_picture(user_id, filename)  # <-----------------------  passes info to database.py to be saved to user in astra.db

        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)




# =======================================================================================
# Site Index - main page - grabs all assignments for user and determines  status of each
# =======================================================================================

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    assignments = get_all_assignments(session["user_id"])


    for a in assignments:
        print(dict(a))


    today = datetime.today().date() # <--------------------------- gets todays date for comparison 

    processed = []
    for a in assignments:
        status = a["status"]

        if status == 1:
            tag = "done"
        else:
            raw_due = a["due_date"]

            if not raw_due or "-" not in raw_due:
                raw_due = a["category"]

            if not raw_due or "-" not in raw_due:
                tag = ""
                processed.append((a, tag))
                continue

            due = datetime.strptime(raw_due, "%Y-%m-%d").date() # <------------------- Logic for when assignments are due - check style.css for styling
            days_left = (due - today).days

            if days_left < 0:
                tag = "overdue"
            elif days_left == 0:
                tag = "due-today"
            elif days_left <= 3:
                tag = "due-3"
            elif days_left <= 5:
                tag = "due-5"
            elif days_left <= 7:
                tag = "due-7"
            elif days_left <= 14:
                tag = "due-14"  
            elif days_left <= 30:
                tag = "due-30"                                
            else:
                tag = "due-xxxx"

        processed.append((a, tag))


    return render_template("index.html", assignments=processed)


# ===============================================================================================================
# Add Assignment - displays for to insert a new assignment (for user) in the database and redirects to the index
# ===============================================================================================================

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        class_name = request.form["class_name"]
        category = request.form["category"]
        due_date = request.form["due_date"]

        add_assignment(
            session["user_id"],
            name,
            class_name,
            category,
            due_date
        )

        return redirect(url_for("index"))

    return render_template("add_assignment.html")


# ==========================================================================================
# Edit Assignment - allows user to edit the selected assignment and post it to the database
# ==========================================================================================

@app.route("/edit/<int:assignment_id>", methods=["GET", "POST"])
def edit(assignment_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        class_name = request.form["class_name"]
        category = request.form["category"]
        due_date = request.form["due_date"]
        update_assignment(assignment_id, name, class_name, category, due_date)
        return redirect(url_for("index"))
 
    assignment = get_assignment(assignment_id)
    return render_template("edit_assignment.html", assignment=assignment)


# =======================================================================
# Delete Assignment - deletes selected assignment and redirects to index
# =======================================================================

@app.route("/delete/<int:assignment_id>")
def delete(assignment_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_assignment(assignment_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
