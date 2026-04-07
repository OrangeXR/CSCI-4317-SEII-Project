from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database import get_all_assignments, add_assignment, update_assignment, delete_assignment, get_assignment, get_user_by_username


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
# Site Index
# ===============

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    assignments = get_all_assignments(session["user_id"])
    return render_template("index.html", assignments=assignments)


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







# ============================================================

# ======================
# Uncomment this section
# to serve over network
# ngrok http 5000
# ======================

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=5000)


# ======================
# Uncomment this section 
# to only serve locally
# ======================

if __name__ == "__main__":
    app.run(debug=True)

# ===============
# ngrok http 5000
# ===============

# ================
# for render.com
# gunicorn app:app
# ================


