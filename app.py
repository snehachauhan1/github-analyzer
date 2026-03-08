from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/<username>")
def get_user(username):

    user_url = f"https://api.github.com/users/{username}"
    repo_url = f"https://api.github.com/users/{username}/repos"

    user_response = requests.get(user_url)

    if user_response.status_code != 200:
      return jsonify({"error": "User not found"})
    
    user_data = user_response.json()
    repos = requests.get(repo_url).json()

    total_stars = 0
    languages = {}

    top_repo = {"name": "", "stars": 0}

    # loop through repositories
    for repo in repos:

        stars = repo["stargazers_count"]
        total_stars += stars

        # find top repo
        if stars > top_repo["stars"]:
            top_repo["name"] = repo["name"]
            top_repo["stars"] = stars

        # count languages
        lang = repo["language"]
        if lang:
            languages[lang] = languages.get(lang, 0) + 1


    # most used language
    most_used_language = max(languages, key=languages.get) if languages else "None"


    # get top 5 repositories by stars
    top_repos = sorted(
        repos,
        key=lambda repo: repo["stargazers_count"],
        reverse=True
    )[:5]
    
    developer_score = (
    user_data.get("public_repos", 0) * 2 +
    user_data.get("followers", 0) * 3 +
    total_stars
)

    return jsonify({
    "user": user_data,
    "total_stars": total_stars,
    "most_used_language": most_used_language,
    "top_repo": top_repo,
    "top_repos": top_repos,
    "languages": languages
})


if __name__ == "__main__":
    app.run(debug=True)