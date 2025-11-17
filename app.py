from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/women")
def women():
    image_folder = "static/images/women"
    images = [
        img for img in os.listdir(image_folder)
        if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"))
    ]
    return render_template("women.html", images=images)

@app.route("/kids")
def kids():
    image_folder = "static/images/kids"
    images = [
        img for img in os.listdir(image_folder)
        if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"))
    ]
    return render_template("kids.html", images=images)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


