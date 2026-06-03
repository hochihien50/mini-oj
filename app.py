from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# ======================
# Home
# ======================

@app.route("/")
def home():
    try:
        with open("problems.json", "r", encoding="utf-8") as f:
            problems = json.load(f)
    except:
        problems = []

    return render_template("home.html", problems=problems)

# ======================
# Submit
# ======================

@app.route("/submit", methods=["GET", "POST"])
def submit():

    if request.method == "POST":

        username = request.form.get("username")
        problem = request.form.get("problem")
        code = request.form.get("code")

        verdict = "AC"

        submission = {
            "username": username,
            "problem": problem,
            "verdict": verdict
        }

        try:
            with open("submissions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []

        data.append(submission)

        with open("submissions.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return render_template(
            "submit.html",
            verdict=verdict
        )

    return render_template("submit.html")

# ======================
# Ranking
# ======================

@app.route("/rank")
def rank():

    try:
        with open("submissions.json", "r", encoding="utf-8") as f:
            submissions = json.load(f)
    except:
        submissions = []

    score = {}

    for sub in submissions:

        if sub["verdict"] == "AC":

            user = sub["username"]

            if user not in score:
                score[user] = 0

            score[user] += 1

    ranking = sorted(
        score.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return render_template(
        "rank.html",
        ranking=ranking
    )

# ======================
# Run
# ======================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
