from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Funzione di connessione al database
def get_db_connection():
    conn = sqlite3.connect('chat_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Creazione delle tabelle nel database (solo una volta)
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_id INTEGER UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        user_id INTEGER,
        contact_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(contact_id) REFERENCES users(user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        sender_id INTEGER,
        receiver_id INTEGER,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sender_id) REFERENCES users(id),
        FOREIGN KEY(receiver_id) REFERENCES users(id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Funzione di registrazione dell'utente
def register_user(username, password):
    user_id = random.randint(10000, 99999)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO users (username, password, user_id) 
    VALUES (?, ?, ?)
    ''', (username, password, user_id))
    conn.commit()
    conn.close()
    return user_id

# Funzione di login
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = login_user(username, password)
    
    if user:
        return jsonify(success=True, user_id=user['user_id'])
    else:
        user_id = register_user(username, password)
        return jsonify(success=True, user_id=user_id)

@app.route('/main')
def main():
    return render_template('main.html')  # Qui va la pagina principale dell'app

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
