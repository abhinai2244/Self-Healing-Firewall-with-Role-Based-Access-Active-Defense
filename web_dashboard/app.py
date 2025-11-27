from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os
import json

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rbac_manager import RBACManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock User Store with Hashed Passwords
# In production, this would be a database
users = {
    "admin": {
        "password": generate_password_hash("admin")
    }
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username]['password'], password):
            login_user(User(username))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
            
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/logs')
@login_required
def logs():
    log_content = ""
    # Use relative path safely
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'snort_alerts.log')
    try:
        with open(log_path, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        log_content = "No logs found."
    return render_template('logs.html', logs=log_content)

@app.route('/roles')
@login_required
def roles():
    rbac = RBACManager()
    roles_data = rbac.roles_data
    return render_template('roles.html', roles=roles_data)

@app.route('/bans')
@login_required
def bans():
    rbac = RBACManager()
    bans_list = {ip: data for ip, data in rbac.roles_data.items() if data['role'] == 'isolated'}
    return render_template('bans.html', bans=bans_list)

@app.route('/update_role', methods=['POST'])
@login_required
def update_role_route():
    ip = request.form['ip']
    role = request.form['role']
    rbac = RBACManager()
    rbac.update_role(ip, role)
    return redirect(url_for('roles'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
