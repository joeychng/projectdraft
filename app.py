from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/profile",methods=["GET","POST"])
def profile():
    return(render_template("profile.html"))

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    balance = request.form.get("balance")
    goal = request.form.get("goal")
    try:
        balance = float(balance)
        goal = float(goal)
        if goal > 0:
            progress = (balance / goal) * 100
        else:
            progress = 0  # Avoid division by zero if goal is zero
    except ValueError:
        # Handle case where input is not a valid number
        balance = 0
        goal = 0
        progress = 0
    return render_template("dashboard.html", balance=round(balance, 2), progress=round(progress, 2))

@app.route("/goal",methods=["GET","POST"])
def profile():
    return(render_template("goal.html"))

if __name__ == "__main__":
    app.run()