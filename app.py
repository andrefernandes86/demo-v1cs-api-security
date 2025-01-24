from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("vulnerable.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Helper function for database queries
def query_db(query, args=(), one=False):
    conn = sqlite3.connect("vulnerable.db")
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")  # Plaintext password
    query_db("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    return jsonify({"message": f"User {username} registered!"})

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = query_db("SELECT * FROM users WHERE username = ? AND password = ?", (username, password), one=True)
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author_id = request.form.get("author_id")
        # SQL Injection vulnerability
        query_db(f"INSERT INTO posts (title, content, author_id) VALUES ('{title}', '{content}', {author_id})")
        return jsonify({"message": "Post created!"})
    elif request.method == "GET":
        posts = query_db("SELECT * FROM posts")
        # XSS vulnerability
        return jsonify([{"id": p[0], "title": p[1], "content": p[2]} for p in posts])

@app.route("/delete_post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    # Broken Object-Level Authorization (BOLA)
    query_db(f"DELETE FROM posts WHERE id = {post_id}")
    return jsonify({"message": "Post deleted!"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=80)
