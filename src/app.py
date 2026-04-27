from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_all_assignments, add_assignment, update_assignment, delete_assignment, get_assignment, get_user_by_username, get_user_by_id, update_profile_picture, get_db 
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "super-secret-key"   # required for session





# ============================================================================================================================
# Create new user
# ============================================================================================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password) # hash user password to insert into astra.db

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO users (name, username, password_hash, profile_picture)
                VALUES (?, ?, ?, ?)
            """, (name, username, password_hash, "default.png"))
            conn.commit()
        except Exception as e:
            return render_template("register.html", error=str(e))
    
        #except Exception as e:
        #    return render_template("register.html", error="Username already exists")

        return redirect(url_for("login"))

    return render_template("register.html")



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

    done_assignments = get_db().execute(
        "SELECT * FROM assignments WHERE user_id = ? AND status = 1 ORDER BY due_date DESC",
        (session["user_id"],)
    ).fetchall()


    return render_template(
        "profile.html",
        #user=user,
        user_name=session["username"],
        done_assignments=done_assignments
    )





# =======================================================================================
# Site Index - main page - grabs all assignments for user and determines  status of each
# =======================================================================================

@app.route("/")
def index():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # NEW: read sort option from query string
    sort = request.args.get("sort", "due")  # default = due date

    assignments = get_all_assignments(session["user_id"])
    assignments = [dict(a) for a in assignments]  # convert Row → dict

    today = datetime.today().date()

    active_assignments = []
    done_assignments = []

    # ============================
    # PROCESS ASSIGNMENTS
    # ============================
    for a in assignments:
        status = a["status"]

        # -------------------------
        # DONE ASSIGNMENTS
        # -------------------------
        if status == 1:
            done_assignments.append((a, "done"))
            continue

        # Keep only the 4 most recent completed assignments
        done_assignments.sort(key=lambda x: x[0]["due_date"], reverse=True)
        done_assignments = done_assignments[:4]
        
        # -------------------------
        # ACTIVE ASSIGNMENTS
        # -------------------------
        raw_due = a["due_date"]

        if not raw_due or "-" not in raw_due:
            raw_due = a["category"]

        if not raw_due or "-" not in raw_due:
            tag = ""
            active_assignments.append((a, tag))
            continue

        due = datetime.strptime(raw_due, "%Y-%m-%d").date()
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

        active_assignments.append((a, tag))

    # ============================
    # SORT ACTIVE ASSIGNMENTS
    # ============================
    if sort == "class_name":
        active_assignments.sort(key=lambda x: x[0]["class_name"].lower())
    elif sort == "due":
        active_assignments.sort(key=lambda x: x[0]["due_date"])
    elif sort == "type":
        active_assignments.sort(key=lambda x: x[0]["category"])

    # ============================
    # OVERVIEW COUNTERS (Sunday-based weeks)
    # ============================

    today = datetime.today().date()

    # Find this upcoming Sunday
    days_until_sunday = (6 - today.weekday()) % 7
    this_sunday = today + timedelta(days=days_until_sunday)

    # Next week boundaries
    next_monday = this_sunday + timedelta(days=1)
    next_sunday = next_monday + timedelta(days=6)

    def parse_date(d):
        try:
            return datetime.strptime(d, "%Y-%m-%d").date()
        except:
            return None

    due_this_week = sum(
        1 for a, tag in active_assignments
        if parse_date(a["due_date"]) is not None
        and today <= parse_date(a["due_date"]) <= this_sunday
    )

    due_next_week = sum(
        1 for a, tag in active_assignments
        if parse_date(a["due_date"]) is not None
        and next_monday <= parse_date(a["due_date"]) <= next_sunday
    )

    return render_template(
        "index.html",
        assignments=active_assignments,
        done_assignments=done_assignments,
        sort=sort,
        user_name=session["username"],
        due_this_week=due_this_week,
        due_next_week=due_next_week
    )



# =====================
# set user call globaly
# =====================
@app.context_processor
def inject_user():
    if "user_id" in session:
        user = get_user_by_id(session["user_id"])
        return {"user": user}
    return {"user": None}



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
        notes = request.form.get("notes", "")

        
        assignment_id = add_assignment(
            session["user_id"],
            name,
            class_name,
            category,
            due_date,
            notes,
            None
        )

        # ==================
        # Handle file upload
        # ==================
        
        files = request.files.getlist("file_uploads")
        file_paths = []

        if files:
            user_id = session["user_id"]
            upload_folder = os.path.join(BASE_DIR, "static", "assignment_files", str(user_id))
            os.makedirs(upload_folder, exist_ok=True)

            for file in files:
                if file and file.filename != "":
                    filename = f"{assignment_id}_{file.filename}"
                    file_path = f"assignment_files/{user_id}/{filename}"

                    file.save(os.path.join(upload_folder, filename))
                    file_paths.append(file_path)

        # Save comma-separated list
        file_paths_str = ",".join(file_paths)

        db = get_db()
        db.execute("UPDATE assignments SET file_path = ? WHERE id = ?", (file_paths_str, assignment_id))
        db.commit()

        return redirect(url_for("index"))

    return render_template("add_assignment.html", user_name=session["username"])



# ==========================================================================================
# Edit Assignment - allows user to edit the selected assignment and post it to the database
# ==========================================================================================

@app.route("/edit/<int:assignment_id>", methods=["GET", "POST"])
def edit(assignment_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    assignment = get_assignment(assignment_id)
    
    if request.method == "POST":
        name = request.form["name"]
        class_name = request.form["class_name"]
        category = request.form["category"]
        due_date = request.form["due_date"]
        notes = request.form.get("notes", "")

        # =============================
        # file uploads
        # =============================
        files = request.files.getlist("file_uploads")

        # Start with existing files
        existing_paths = assignment["file_path"].split(",") if assignment["file_path"] else []
        new_paths = []

        if files:
            user_id = session["user_id"]
            upload_folder = os.path.join(BASE_DIR, "static", "assignment_files", str(user_id))
            os.makedirs(upload_folder, exist_ok=True)

            for file in files:
                if file and file.filename != "":
                    filename = f"{assignment_id}_{file.filename}"
                    file_path = f"assignment_files/{user_id}/{filename}"

                    file.save(os.path.join(upload_folder, filename))
                    new_paths.append(file_path)

        # Combine old + new
        final_paths = existing_paths + new_paths
        file_paths_str = ",".join(final_paths)

        update_assignment(
            assignment_id,
            name,
            class_name,
            category,
            due_date,
            notes,
            file_paths_str
        )

        return redirect(url_for("index"))
    
    return render_template("edit_assignment.html", assignment=assignment, user_name=session["username"])


# =======================================================================
# Delete Assignment - deletes selected assignment and redirects to index
# =======================================================================

@app.route("/delete/<int:assignment_id>")
def delete(assignment_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_assignment(assignment_id)

    next_page = request.args.get("next")
    if next_page:
        return redirect(next_page)

    return redirect(url_for("index"))


# =========================================================
# Delete Assignment File - deletes selected assignment file 
# =========================================================
@app.route("/remove_file/<int:assignment_id>")
def remove_file(assignment_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    file_path = request.args.get("file_path")
    next_page = request.args.get("next", url_for("index"))

    if not file_path:
        return redirect(next_page)

    # Get assignment
    assignment = get_assignment(assignment_id)
    if not assignment:
        return redirect(next_page)

    # Remove file from disk
    full_path = os.path.join(BASE_DIR, "static", file_path)
    if os.path.exists(full_path):
        os.remove(full_path)

    # Remove file from DB list
    paths = assignment["file_path"].split(",") if assignment["file_path"] else []
    updated_paths = [p for p in paths if p != file_path]
    new_file_path_str = ",".join(updated_paths)

    # Update DB
    db = get_db()
    db.execute("UPDATE assignments SET file_path = ? WHERE id = ?", (new_file_path_str, assignment_id))
    db.commit()

    return redirect(next_page)

# =======================================================================
# Finish Assignment - Mark assignment as Done
# =======================================================================

@app.route("/done/<int:assignment_id>")
def mark_done(assignment_id):
    db = get_db()
    db.execute("UPDATE assignments SET status = 1 WHERE id = ?", (assignment_id,))
    db.commit()
    return redirect(url_for("index"))















if __name__ == "__main__":
    app.run(debug=True)

