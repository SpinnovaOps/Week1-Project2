from datetime import timedelta, datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = b"23triu23g47tr23728437ft82bx87t32rv2t3%$&!*%E^(!*"
app.permanent_session_lifetime = timedelta(seconds=30)

tasks = []

# ----- Home Route -----
@app.route("/")
def index():
    return render_template("index.html")

# ----- Login Route -----
@app.route("/login", methods=["GET", "POST"])
def login():
    session.permanent = True 
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "password":  # Sample credentials
            session["user"] = username
            session["Login_Time"] = datetime.now()
            return redirect(url_for("view_tasks"))
        else:
            return "Invalid Credentials"
    return render_template("login.html")

# ----- Logout -----
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("Login_Time", None)
    return redirect(url_for("index"))

# ----- View Tasks (Requires Login) -----
@app.route("/tasks", methods=['GET','POST'])
def view_tasks():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("tasks.html", tasks=tasks)

# ----- Add Task -----
@app.route("/add", methods=["POST"])
def add_task():
    if "user" in session:
        task = request.form.get("task")
        if task:
            tasks.append(task)
            session["recent_added"] = task  # Store recent added task in session
            return redirect(url_for("view_tasks"))
    return redirect(url_for("login"))

# ----- Delete Task -----
@app.route("/delete/<int:index>")
def delete_task(index):
    if "user" in session and 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        session["recent_deleted"] = deleted_task  # Store recent deleted task in session
        return redirect(url_for("view_tasks"))
    return redirect(url_for("login"))

# ----- Recent Added Task -----
@app.route("/recent-added")
def show_recent_added():
    recent_added = session.get("recent_added", None)
    return render_template("recent_added.html", task=recent_added)

# ----- Recent Deleted Task -----
@app.route("/recent-deleted")
def show_recent_deleted():
    recent_deleted = session.get("recent_deleted", None)
    return render_template("recent_deleted.html", task=recent_deleted)

@app.route("/checkIn")
def checkin():
    return redirect(url_for('login'))

@app.route('/checkout')
def checkout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/showme')
def showme():
    if 'user' in session:
        return redirect(url_for('view_tasks'))
    return "Invalid Credentials"
    

@app.before_request
def session_timeout():
    if 'user' in session:
        login_time = session['Login_Time']
        
        # Make both datetimes naive
        if login_time.tzinfo is not None:
            login_time = login_time.replace(tzinfo=None)
        
        # Compare with a naive datetime (datetime.now() is naive)
        if datetime.now() - login_time > timedelta(seconds=30):
            flash('Session Timeout. Please Login...')
            session.pop('user', None)
            session.pop('Login_Time', None)
            return redirect(url_for('session_timeout_page'))


@app.route('/session-timeout')
def session_timeout_page():
    return render_template('session_timeout_page.html')  # Create a page to show session timeout message.

if __name__ == "__main__":
    app.run(debug=True)

