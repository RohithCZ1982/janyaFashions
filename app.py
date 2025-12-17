from flask import Flask, render_template, request, jsonify
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

@app.route("/rename")
def rename():
    kids_folder = "static/images/kids"
    women_folder = "static/images/women"
    
    kids_images = []
    women_images = []
    
    if os.path.exists(kids_folder):
        kids_images = [
            {"name": img, "folder": "kids"}
            for img in os.listdir(kids_folder)
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"))
        ]
    
    if os.path.exists(women_folder):
        women_images = [
            {"name": img, "folder": "women"}
            for img in os.listdir(women_folder)
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"))
        ]
    
    return render_template("rename.html", kids_images=kids_images, women_images=women_images)

@app.route("/rename_file", methods=["POST"])
def rename_file():
    try:
        data = request.json
        folder = data.get("folder")
        old_name = data.get("old_name")
        new_name = data.get("new_name")
        amount = data.get("amount")
        
        if not folder or not old_name or not new_name or not amount:
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        # Construct new filename: name - amount.extension
        file_ext = os.path.splitext(old_name)[1]
        new_filename = f"{new_name} - {amount}{file_ext}"
        
        old_path = os.path.join("static/images", folder, old_name)
        new_path = os.path.join("static/images", folder, new_filename)
        
        if not os.path.exists(old_path):
            return jsonify({"success": False, "error": "File not found"}), 404
        
        os.rename(old_path, new_path)
        
        return jsonify({"success": True, "new_name": new_filename})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


