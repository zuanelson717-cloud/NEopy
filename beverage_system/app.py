from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Database setup
DATABASE = 'beverage_store.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                company_name TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                invoice_number TEXT UNIQUE NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id)
            );
        ''')
        db.commit()
        print("Database initialized successfully!")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        company_name = data.get('company_name')
        phone = data.get('phone')
        
        if not all([username, email, password, full_name]):
            return jsonify({'error': 'Todos os campos obrigatórios devem ser preenchidos'}), 400
        
        try:
            db = get_db()
            db.execute(
                'INSERT INTO users (username, email, password, full_name, company_name, phone) VALUES (?, ?, ?, ?, ?, ?)',
                (username, email, generate_password_hash(password), full_name, company_name, phone)
            )
            db.commit()
            return jsonify({'message': 'Usuário registrado com sucesso!'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Usuário ou email já existem'}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            return jsonify({'message': 'Login bem-sucedido!'}), 200
        else:
            return jsonify({'error': 'Usuário ou senha inválidos'}), 401
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    invoices = db.execute(
        'SELECT * FROM invoices WHERE user_id = ? ORDER BY issue_date DESC',
        (session['user_id'],)
    ).fetchall()
    
    total_invoices = len(invoices)
    total_amount = sum(inv['total_amount'] for inv in invoices)
    pending_amount = sum(inv['total_amount'] for inv in invoices if inv['status'] == 'pending')
    
    return render_template('dashboard.html', 
                         invoices=invoices,
                         total_invoices=total_invoices,
                         total_amount=total_amount,
                         pending_amount=pending_amount)

@app.route('/profile')
@login_required
def profile():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return render_template('profile.html', user=user)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    data = request.get_json() if request.is_json else request.form
    full_name = data.get('full_name')
    company_name = data.get('company_name')
    phone = data.get('phone')
    
    db = get_db()
    db.execute(
        'UPDATE users SET full_name = ?, company_name = ?, phone = ? WHERE id = ?',
        (full_name, company_name, phone, session['user_id'])
    )
    db.commit()
    return jsonify({'message': 'Perfil atualizado com sucesso!'}), 200

@app.route('/invoice/<int:invoice_id>')
@login_required
def view_invoice(invoice_id):
    db = get_db()
    invoice = db.execute(
        'SELECT * FROM invoices WHERE id = ? AND user_id = ?',
        (invoice_id, session['user_id'])
    ).fetchone()
    
    if not invoice:
        return jsonify({'error': 'Fatura não encontrada'}), 404
    
    items = db.execute(
        'SELECT * FROM invoice_items WHERE invoice_id = ?',
        (invoice_id,)
    ).fetchall()
    
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    return render_template('invoice_detail.html', invoice=invoice, items=items, user=user)

@app.route('/api/invoices', methods=['POST'])
@login_required
def create_invoice():
    data = request.get_json()
    invoice_number = data.get('invoice_number')
    total_amount = data.get('total_amount')
    description = data.get('description')
    items = data.get('items', [])
    
    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO invoices (user_id, invoice_number, total_amount, description) VALUES (?, ?, ?, ?)',
            (session['user_id'], invoice_number, total_amount, description)
        )
        invoice_id = cursor.lastrowid
        
        for item in items:
            db.execute(
                'INSERT INTO invoice_items (invoice_id, product_name, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)',
                (invoice_id, item['product_name'], item['quantity'], item['unit_price'], item['total_price'])
            )
        
        db.commit()
        return jsonify({'message': 'Fatura criada com sucesso!', 'invoice_id': invoice_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Número de fatura já existe'}), 400

@app.route('/api/invoices/<int:invoice_id>/status', methods=['PUT'])
@login_required
def update_invoice_status(invoice_id):
    data = request.get_json()
    new_status = data.get('status')
    
    db = get_db()
    db.execute(
        'UPDATE invoices SET status = ? WHERE id = ? AND user_id = ?',
        (new_status, invoice_id, session['user_id'])
    )
    db.commit()
    return jsonify({'message': 'Status atualizado com sucesso!'}), 200

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
