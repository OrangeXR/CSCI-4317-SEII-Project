from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database import get_all_assignments, add_assignment, update_assignment, delete_assignment, get_assignment, get_user_by_username, get_user_by_id, update_profile_picture 
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "super-secret-key"   # required for session

# ===============
# Login
# ===============

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")



# ===============
# Logout
# ===============

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



# ==========================
# PROFILE PAGE + UPLOAD
# ==========================
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
            upload_folder = os.path.join(BASE_DIR, "static", "profile_pics")
            os.makedirs(upload_folder, exist_ok=True)

            filename = f"user_{user_id}.png"
            filepath = os.path.join(upload_folder, filename)

            file.save(filepath)
            update_profile_picture(user_id, filename)

        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)




# ===============
# Site Index
# ===============

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    assignments = get_all_assignments(session["user_id"])


    for a in assignments:
        print(dict(a))


    today = datetime.today().date()
    soon_threshold = today + timedelta(days=3)

    processed = []
    for a in assignments:
        status = a["status"]

        if status == 1:
            tag = "done"
        else:
            raw_due = a["due_date"]

            # SAFETY: if due_date is invalid, swap with category
            if not raw_due or "-" not in raw_due:
                raw_due = a["category"]

            # SAFETY: if STILL invalid, skip date parsing entirely
            if not raw_due or "-" not in raw_due:
                tag = ""
                processed.append((a, tag))
                continue

            due = datetime.strptime(raw_due, "%Y-%m-%d").date()

            if due < today:
                tag = "overdue"
            elif due == today:
                tag = "due-today"
            elif due <= soon_threshold:
                tag = "due-soon"
            else:
                tag = ""

        processed.append((a, tag))


    return render_template("index.html", assignments=processed)


# ===============
# Add Assignment
# ===============

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


# ===============
# Edit Assignment
# ===============

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
    # You’ll add a DB helper to fetch a single assignment
    assignment = get_assignment(assignment_id)
    return render_template("edit_assignment.html", assignment=assignment)


# ===============
# Delete Assignment
# ===============

@app.route("/delete/<int:assignment_id>")
def delete(assignment_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_assignment(assignment_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

