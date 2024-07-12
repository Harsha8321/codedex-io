from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '7adf55a2a254b81dcc6aab517e66158e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def serve_index():
    user_name = session.get('user_name')
    return render_template('index.html', user_name=user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_name'] = user.name
            flash('Login successful!', category='success')
            return redirect(url_for('serve_index'))
        else:
            flash('Login failed. Check your email and password.', category='error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', category='error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            new_user = User(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please sign in.', category='success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    flash('You have been logged out.', category='success')
    return redirect(url_for('serve_index'))

@app.route('/dashboard')
def dashboard():
    if 'user_name' in session:
        return f'Welcome to the dashboard, {session["user_name"]}!'
    return redirect(url_for('login'))

@app.route('/generate_graphs', methods=['POST'])
def generate_graphs():
    data = request.get_json()
    sport = data['sport']

    python_interpreter = '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3'
    script_path = os.path.join(os.getcwd(), 'generate_graphs.py')

    result = subprocess.run([python_interpreter, script_path, sport], capture_output=True, text=True)

    if result.returncode == 0:
        return jsonify({'status': 'success', 'sport': sport}), 200
    else:
        return jsonify({'status': 'error', 'message': result.stderr}), 500

@app.route('/view_insights/<sport>')
def view_insights(sport):
    return render_template('view_insights.html', sport=sport)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This line creates the database tables
    app.run(debug=True)
