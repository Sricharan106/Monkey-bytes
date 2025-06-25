import os
import random
import psycopg2
from dotenv import load_dotenv
import sqlite3
import smtplib
from email.mime.text import MIMEText
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message

load_dotenv()
app = Flask(__name__)
app.secret_key = 'dev_secret_12345'  
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'monkeybytes.verify@gmail.com'
app.config['MAIL_PASSWORD'] = 'usvd kkgy zzpl jyxj'
mail = Mail(app)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        session['pending_email'] = email
        return redirect('/form')

    return render_template("index.html")


@app.route('/form', methods=['GET', 'POST'])
def form():
    email = session.get('pending_email')
    if not email:
        flash('Please enter your email first!', 'danger')
        return redirect('/')
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        news = request.form.get('news')
        email = session.get('pending_email')
        if not email:
            flash('Please enter your email first!', 'danger')
            return redirect('/')
        if not name or not dob:
            flash('All fields are required!', 'danger')
            return redirect('/form')

        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (name, email, password, news_type) VALUES (%s, %s, %s, %s)',
                    (name, email, None, news))
            conn.commit()
            flash('Registration successful!', 'success')
            send_newsletter_email(email, user_name=name)
            return redirect('/login')
        except psycopg2.IntegrityError as e:
            flash('Email already exists!', 'danger')
            print("❌ DB Error:", e)
            return redirect('/')
        finally:
            conn.close()
    return render_template("form.html", pending_email=email)


def send_newsletter_email(to_email, user_name):
    sender_email = "newsletter.monkeybytes@gmail.com"       # your second email
    sender_password = 'idet fkqg lhqk czmj'             # app password
    subject = "🎉 Thanks for Registering to Monkey Bytes!"
    
    body = f"""
    Hi {user_name},

    Thanks for joining Monkey Bytes 🐒!
    Stay tuned for weekly updates on tech and anime. 💌

    — Monkey Bytes Team
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            print("✅ Thank you email sent.")
    except Exception as e:
        print("❌ Failed to send newsletter email:", e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=%s', (email,))
        user = c.fetchone()
        conn.close()
        if user:
            if user[3]:  # Check if password is set
                flash('This account has a password.', 'info')
                session['email'] = email
                session['user_id'] = user[0]  # Store user ID in session for later use
                return redirect('/password')
            else:
                otp = generate_otp()
                session['otp'] = otp
                session['email'] = email
                session['user_id'] = user[0]  # Store user ID in session for later use
                msg = Message('Your OTP Code', sender='monkeybytes.verify@gmail.com',
                              recipients=[email])
                msg.body = f'Your OTP is {otp}'
                mail.send(msg)
                flash('OTP sent to your email!', 'info')
                return redirect('/verify')
        else:
            flash('Email not found. Please register first.', 'danger')
            return redirect('/')

    return render_template("login.html")


@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        email = session.get('email')
        if not email:
            flash('Please log in first!', 'danger')
            return redirect('/login')
        action = request.form.get('action')
        if action == 'otp':
            otp = generate_otp()
            session['otp'] = otp
            msg = Message('Your OTP Code', sender='monkeybytes.verify@gmail.com',
                          recipients=[email])
            msg.body = f'Your OTP is {otp}'
            mail.send(msg)
            flash('OTP sent to your email!', 'info')
            return redirect('/verify')
        elif action == 'login':
            password_entered = request.form.get('password')
            if not password_entered:
                flash('Password cannot be empty!', 'danger')
                return redirect('/password')
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('SELECT password FROM users WHERE email=%s', (email,))
            password = c.fetchone()
            conn.close()
            if not check_password_hash(password[0], password_entered):
                flash('Incorrect password. Please try again.', 'danger')
                return redirect('/login')
            if 'user_id' not in session:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute('SELECT id FROM users WHERE email = %s', (session['email'],))
                user = c.fetchone()
                conn.close()
                if user:
                    session['user_id'] = user[0]
            return redirect('/Dashboard')

    return render_template("password.html")


@app.route('/Dashboard', methods=['GET', 'POST'])
def dashboard():
    email = session.get('email')
    if not email:
        flash('Please log in first to continue.', 'danger')
        return redirect('/login')

    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT name, news_type FROM users WHERE email = %s', (email,))
    user = c.fetchone()
    subscriptions = [row[0] for row in c.fetchall()]
    conn.close()

    if user:
        name = user[0]
        name2 = user[0]
        news = user[1]
        return render_template('dashboard.html', name=name, subscriptions=subscriptions, name2=name2, news=news)
    else:
        flash('User not found!', 'danger')
        return redirect('/login')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    conn = get_db_connection()
    c = conn.cursor()
    email = session.get('email')
    c.execute('SELECT name FROM users WHERE email = %s', (email,))
    name = c.fetchone()
    name2 = name[0]
    if request.method == 'POST':
        email = session.get('email')
        form_type = request.form.get('action')

        if form_type == 'preferences':
            selected_news = request.form.get('news')
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE users SET news_type = %s WHERE email = %s', (selected_news, email))
            conn.commit()
            conn.close()
            flash('Preferences updated!', 'success')
            return redirect('/Dashboard')

        elif form_type == 'unsubscribe':
            unsubscribe_email = request.form.get('unsubscribe_email')
            if email == unsubscribe_email:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute('DELETE FROM users WHERE email = %s', (email,))
                conn.commit()
                conn.close()
                flash('Unsubscribed successfully!', 'success')
                return redirect('/')
            else:
                flash('Email does not match!', 'danger')
                return redirect('/settings')

        elif form_type == 'change_password':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            if not new_password or not confirm_password:
                flash('New password cannot be empty!', 'danger')
                return redirect('/settings')
            if new_password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect('/settings')
            print("✅ Passwords match.")
            hashed_password = generate_password_hash(new_password)
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE users SET password = %s WHERE email = %s', (hashed_password, email))
            print("✅ Password updated successfully.")
            conn.commit()
            conn.close()
            flash('Password updated successfully!', 'success')
            return redirect('/Dashboard')

    return render_template('settings.html', name=name2)


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if entered_otp == session.get('otp'):
            flash('OTP verified successfully!', 'success')
            if 'user_id' not in session:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute('SELECT id FROM users WHERE email = %s', (session['email'],))
                user = c.fetchone()
                conn.close()
                if user:
                    session['user_id'] = user[0]
            return redirect('/Dashboard')
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect('/verify')
        
    return render_template("verify.html")


def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def init_db():
    try:
        print("✅ Running init_db()...")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT,
                news_type TEXT DEFAULT 'tech'
            )
        ''')

        c.execute("""
            CREATE TABLE IF NOT EXISTS archives (
                id SERIAL PRIMARY KEY,
                subject TEXT,
                body TEXT,
                category TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ Tables created or verified.")
    except Exception as e:
        print("❌ Error in init_db():", e)
    finally:
        conn.close()


@app.context_processor
def inject_user_name():
    name = None
    if 'email' in session:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT name FROM users WHERE email = %s', (session['email'],))
        user = c.fetchone()
        conn.close()
        if user:
            name = user[0]
    return dict(name=name)


app.context_processor(inject_user_name)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect('/')


@app.route('/resend', methods=['GET', 'POST'])
def resend():
    email = session.get('email')
    if email:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE email = %s', (email,))
        user = c.fetchone()
        conn.close()
        if user:
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            msg = Message('Your OTP Code', sender='monkeybytes.verify@gmail.com',
                          recipients=[email])
            msg.body = f'Your OTP is {otp}'
            mail.send(msg)
            flash('OTP resent!', 'info')
            return redirect('/verify')
        else:
            flash('Email not found!', 'danger')
            return redirect('/login')
    flash('Session expired. Please log in again.', 'danger')
    return redirect('/login')

init_db()
@app.route('/initdb')
def trigger_init_db():
    init_db()
    return "✅ Database initialised!"

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/archives')
def archives():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM archives ORDER BY sent_at DESC')
    archives = c.fetchall()
    conn.close()
    return render_template('archives.html', archives=archives)


@app.route('/archives/<int:archive_id>')
def archive_detail(archive_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT subject, body, category, sent_at FROM archives WHERE id = %s", (archive_id,))
    archive = c.fetchone()
    conn.close()

    if not archive:
        return "Newsletter not found", 404

    subject, body, category, sent_at = archive
    return render_template('archive_detail.html', subject=subject, body=body, category=category, sent_at=sent_at)
