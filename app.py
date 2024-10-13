from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/",methods=["GET","POST"])
def profile():
    balance = request.form("balance")
    goal = request.form("goal")
    progress = (balance / goal) * 100
    return(render_template("profile.html"))

if __name__ == "__main__":
    app.run()