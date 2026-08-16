from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3

app = Flask(__name__)
# Set a secret key to enable secure session tracking
app.secret_key = 'security-lab-super-secret-key-12345'

# Initialize the SQLite database in memory and seed it with a user
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT,
            secret_note TEXT
        )
    ''')
    # Add multiple accounts with secrets
    cursor.execute("INSERT INTO users (username, password, role, secret_note) VALUES ('admin', 'SuperSecretAdmin123!', 'administrator', 'Master server SSH key is: ssh-rsa AAAAB3N... [FLAG_ADMIN_SECRET]')")
    cursor.execute("INSERT INTO users (username, password, role, secret_note) VALUES ('alice', 'alicepassword123', 'user', 'Remind Bob to check firewall settings.')")
    cursor.execute("INSERT INTO users (username, password, role, secret_note) VALUES ('bob', 'bobpassword456', 'user', 'My dog name is Buster.')")
    conn.commit()
    conn.close()

# Run database setup
init_db()

# Simple HTML login form template string
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Lab Login</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; }
        .login-card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 300px; }
        h2 { margin-top: 0; color: #1a1a1a; text-align: center; }
        .input-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; color: #666; font-size: 0.9rem; }
        input[type="text"], input[type="password"] { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 0.7rem; background: #007bff; border: none; color: white; font-weight: bold; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { color: red; text-align: center; margin-bottom: 1rem; font-size: 0.9rem; }
        .success { color: green; text-align: center; margin-bottom: 1rem; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>Security Lab</h2>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if success %}<div class="success">{{ success }}</div>{% endif %}
        <form method="POST" action="/login">
            <div class="input-group">
                <label>Username</label>
                <input type="text" name="username" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return '<p>Welcome to the Security Lab. Go to <a href="/login">/login</a> to log in.</p>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # SECURE: Store user session details
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[3]
                success = f"Login successful! Welcome back, {user[1]} (Role: {user[3]})."
            else:
                error = "Invalid credentials."
        except Exception as e:
            error = f"Database Error: {e}"
            
    return render_template_string(LOGIN_HTML, error=error, success=success)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # SECURE: Changed f""" to a normal """ string.
    # Changed {query} to Jinja2's {{ query }}.
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Security Lab Search</title>
        <style>
            body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding-top: 50px; background: #f0f2f5; }
            .search-box { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 400px; text-align: center; }
            input[type="text"] { width: 80%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 0.5rem 1rem; background: #007bff; border: none; color: white; border-radius: 4px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="search-box">
            <h2>Search Users</h2>
            <form method="GET" action="/search">
                <input type="text" name="q" placeholder="Enter username..." value="{{ query }}">
                <button type="submit">Search</button>
            </form>
            <br>
            <p>Results for: <b>{{ query }}</b></p>
            <p><i>No users found matching that query.</i></p>
        </div>
    </body>
    </html>
    """
    # SECURE: Pass query=query as an argument so Jinja2 auto-escapes it
    return render_template_string(html, query=query)

@app.route('/profile')
def profile():
    # 1. Check if the visitor is logged in
    if 'user_id' not in session:
        return "<h3>Access Denied: Please <a href='/login'>login</a> first.</h3>", 401
        
    requested_id = request.args.get('id', '')
    if not requested_id:
        return f"<p>Please specify a user ID, e.g., <a href='/profile?id={session['user_id']}'>/profile?id={session['user_id']}</a></p>"
    
    # Convert inputs to integers to compare them accurately
    try:
        requested_id = int(requested_id)
        current_user_id = int(session['user_id'])
    except ValueError:
        return "Invalid ID format", 400

    # 2. ENFORCE ACCESS CONTROL:
    # A user can only view their own profile, UNLESS they are an administrator.
    if requested_id != current_user_id and session.get('role') != 'administrator':
        return "<h3>Access Denied: You do not have permission to view this profile.</h3>", 403

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, secret_note FROM users WHERE id = ?", (requested_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return f"""
            <h2>User Profile</h2>
            <p><b>User ID:</b> {user[0]}</p>
            <p><b>Username:</b> {user[1]}</p>
            <p><b>Role:</b> {user[2]}</p>
            <p><b>Private Secret Note:</b> {user[3]}</p>
            """
        else:
            return "User not found", 404
    except Exception as e:
        return f"Database error: {e}", 500
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)