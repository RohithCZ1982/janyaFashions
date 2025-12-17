from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.secret_key = 'janya_fashions_secret_key_2025'  # Change this to a secure random key in production

BANNER_JSON_FILE = 'banner_text.json'

def get_banner_text():
    """Read banner text from JSON file"""
    try:
        if os.path.exists(BANNER_JSON_FILE):
            with open(BANNER_JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('text', '🎀 Huge Sale! Up to 40% OFF on New Arrivals! 🎀')
        else:
            # Create default file if it doesn't exist
            default_text = "🎀 Huge Sale! Up to 40% OFF on New Arrivals! 🎀"
            save_banner_text(default_text)
            return default_text
    except Exception as e:
        return "🎀 Huge Sale! Up to 40% OFF on New Arrivals! 🎀"

def save_banner_text(text):
    """Save banner text to JSON file"""
    try:
        with open(BANNER_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump({"text": text}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False

@app.route("/women")
def women():
    image_folder = "static/images/women"
    images = []
    
    if os.path.exists(image_folder):
        for img in os.listdir(image_folder):
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif")):
                number, name, amount, ext = extract_image_info(img)
                images.append({
                    "filename": img,
                    "number": number,
                    "name": name,
                    "amount": amount
                })
        # Sort by number (None values go to end)
        images.sort(key=lambda x: (x["number"] is None, x["number"] or 999999))
    
    banner_text = get_banner_text()
    return render_template("women.html", images=images, banner_text=banner_text)

@app.route("/kids")
def kids():
    image_folder = "static/images/kids"
    images = []
    
    if os.path.exists(image_folder):
        for img in os.listdir(image_folder):
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif")):
                number, name, amount, ext = extract_image_info(img)
                images.append({
                    "filename": img,
                    "number": number,
                    "name": name,
                    "amount": amount
                })
        # Sort by number (None values go to end)
        images.sort(key=lambda x: (x["number"] is None, x["number"] or 999999))
    
    banner_text = get_banner_text()
    return render_template("kids.html", images=images, banner_text=banner_text)

def extract_image_info(filename):
    """Extract number, name, and amount from filename.
    Expected format: 'number - name - amount.ext' or 'name - amount.ext' or just 'filename.ext'
    Returns: (number, name, amount, extension) where number can be None"""
    name_without_ext, ext = os.path.splitext(filename)
    
    # Try to parse: number - name - amount
    parts = name_without_ext.split(' - ')
    
    if len(parts) == 3:
        # Format: number - name - amount
        try:
            number = int(parts[0].strip())
            name = parts[1].strip()
            amount = parts[2].strip()
            return (number, name, amount, ext)
        except ValueError:
            # First part is not a number, treat as: name - amount
            pass
    
    if len(parts) == 2:
        # Format: name - amount (no number)
        name = parts[0].strip()
        amount = parts[1].strip()
        return (None, name, amount, ext)
    
    # Just filename, no structure
    return (None, name_without_ext, None, ext)

def is_admin():
    """Check if user is logged in as admin"""
    return session.get('admin_logged_in', False)

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    """Admin login page"""
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == "admin123":
            session['admin_logged_in'] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Incorrect password")
    
    # If already logged in, redirect to dashboard
    if is_admin():
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard with link to rename page"""
    if not is_admin():
        return redirect(url_for("admin_login"))
    
    banner_text = get_banner_text()
    return render_template("admin_dashboard.html", banner_text=banner_text)

@app.route("/admin/update_banner", methods=["POST"])
def update_banner():
    """Update banner text"""
    if not is_admin():
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    
    try:
        data = request.json
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"success": False, "error": "Banner text cannot be empty"}), 400
        
        if save_banner_text(text):
            return jsonify({"success": True, "message": "Banner text updated successfully"})
        else:
            return jsonify({"success": False, "error": "Failed to save banner text"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/logout")
def admin_logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    return redirect(url_for("admin_login"))

@app.route("/rename")
def rename():
    # Check if user is admin before allowing access
    if not is_admin():
        return redirect(url_for("admin_login"))
    kids_folder = "static/images/kids"
    women_folder = "static/images/women"
    
    kids_images = []
    women_images = []
    
    if os.path.exists(kids_folder):
        for img in os.listdir(kids_folder):
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif")):
                number, name, amount, ext = extract_image_info(img)
                kids_images.append({
                    "name": img,
                    "folder": "kids",
                    "number": number,
                    "parsed_name": name,
                    "parsed_amount": amount
                })
        # Sort by number (None values go to end)
        kids_images.sort(key=lambda x: (x["number"] is None, x["number"] or 999999))
    
    if os.path.exists(women_folder):
        for img in os.listdir(women_folder):
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif")):
                number, name, amount, ext = extract_image_info(img)
                women_images.append({
                    "name": img,
                    "folder": "women",
                    "number": number,
                    "parsed_name": name,
                    "parsed_amount": amount
                })
        # Sort by number (None values go to end)
        women_images.sort(key=lambda x: (x["number"] is None, x["number"] or 999999))
    
    return render_template("rename.html", kids_images=kids_images, women_images=women_images)

@app.route("/rename_file", methods=["POST"])
def rename_file():
    # Check if user is admin before allowing access
    if not is_admin():
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    try:
        data = request.json
        folder = data.get("folder")
        old_name = data.get("old_name")
        new_name = data.get("new_name")
        amount = data.get("amount")
        number = data.get("number")
        
        if not folder or not old_name or not new_name or not amount:
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        # Get file extension
        file_ext = os.path.splitext(old_name)[1]
        
        # Construct new filename: number - name - amount.extension
        # Format number as 3-digit string (001, 002, etc.)
        if number is not None and number != "":
            try:
                num = int(number)
                num_str = f"{num:03d}"  # Format as 001, 002, etc.
                new_filename = f"{num_str} - {new_name} - {amount}{file_ext}"
            except ValueError:
                # Invalid number, use without number
                new_filename = f"{new_name} - {amount}{file_ext}"
        else:
            new_filename = f"{new_name} - {amount}{file_ext}"
        
        old_path = os.path.join("static/images", folder, old_name)
        new_path = os.path.join("static/images", folder, new_filename)
        
        if not os.path.exists(old_path):
            return jsonify({"success": False, "error": "File not found"}), 404
        
        os.rename(old_path, new_path)
        
        return jsonify({"success": True, "new_name": new_filename})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/delete_image", methods=["POST"])
def delete_image():
    """Delete an image file"""
    # Check if user is admin before allowing access
    if not is_admin():
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    
    try:
        data = request.json
        folder = data.get("folder")
        filename = data.get("filename")
        
        if not folder or not filename:
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        if folder not in ("kids", "women"):
            return jsonify({"success": False, "error": "Invalid folder"}), 400
        
        file_path = os.path.join("static/images", folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "error": "File not found"}), 404
        
        os.remove(file_path)
        
        return jsonify({"success": True, "message": "Image deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/upload_image", methods=["POST"])
def upload_image():
    """
    Upload a new image into either the kids or women folder.
    """
    # Check if user is admin before allowing access
    if not is_admin():
        return redirect(url_for("admin_login"))
    folder = request.form.get("folder")
    file = request.files.get("file")

    # Basic validation
    if folder not in ("kids", "women") or file is None or file.filename == "":
        # Just go back to the page; you can add flash messages later if needed
        return redirect(url_for("rename"))

    filename = secure_filename(file.filename)
    if filename == "":
        return redirect(url_for("rename"))

    upload_dir = os.path.join("static", "images", folder)
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    return redirect(url_for("rename"))

@app.route("/")
def index():
    banner_text = get_banner_text()
    return render_template("index.html", banner_text=banner_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


