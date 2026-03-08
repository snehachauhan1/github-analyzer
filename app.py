from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    username = request.form["username"]

    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url)

    if response.status_code == 404:
        return "User not found"

    repos = response.json()

    # Top 5 repos by stars
    top_repos = sorted(
        repos,
        key=lambda repo: repo["stargazers_count"],
        reverse=True
    )[:5]

    # Language statistics
    languages = {}

    for repo in repos:
        lang = repo["language"]
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    return render_template(
        "index.html",
        repos=top_repos,
        languages=languages,
        username=username
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)