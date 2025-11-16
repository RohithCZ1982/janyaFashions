from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    image_folder = "images"
    images = os.listdir(image_folder)

    images = [
        img for img in images
        if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]

    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
