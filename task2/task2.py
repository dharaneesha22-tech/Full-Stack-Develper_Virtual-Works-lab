from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    profile = None

    if request.method == "POST":

        profile = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "college": request.form.get("college"),
            "department": request.form.get("department"),
            "bio": request.form.get("bio"),
            "image": request.form.get("image"),
            "linkedin": request.form.get("linkedin"),
            "github": request.form.get("github"),
            "skills": request.form.get("skills").split(",")
        }

    return render_template("index.html", profile=profile)

if __name__ == "__main__":
    app.run(debug=True)