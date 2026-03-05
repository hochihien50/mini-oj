from flask import Flask,render_template,request,redirect,session
import json
import judge

app = Flask(__name__)
app.secret_key="oj_secret"

def load(file):
    return json.load(open(file))

def save(file,data):
    json.dump(data,open(file,"w"))

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    problems=load("problems.json")
    return render_template("home.html",problems=problems)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]
        users=load("users.json")
        if u in users and users[u]==p:
            session["user"]=u
            return redirect("/")
    return render_template("login.html")

@app.route("/submit/<pid>",methods=["GET","POST"])
def submit(pid):
    if request.method=="POST":
        code=request.form["code"]
        user=session["user"]

        result=judge.run(pid,code)

        subs=load("submissions.json")
        subs.append({
            "user":user,
            "problem":pid,
            "result":result
        })
        save("submissions.json",subs)

        return "Result: "+result

    return render_template("submit.html",pid=pid)

@app.route("/rank")
def rank():
    subs=load("submissions.json")
    score={}

    for s in subs:
        if s["result"]=="AC":
            score[s["user"]]=score.get(s["user"],0)+1

    ranking=sorted(score.items(),key=lambda x:-x[1])
    return render_template("rank.html",ranking=ranking)

app.run(host="0.0.0.0",port=10000)
