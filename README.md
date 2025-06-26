# 🐵 Monkey Bytes

Monkey Bytes is a clean newsletter web app that lets users subscribe to specific news categories like Tech, Sports, and Entertainment. It features email verification via OTP, a dashboard for managing subscriptions, and a dark/light theme switch — all built with Flask and PostgreSQL.

## 📽 Demo Video

[Watch the Demo](https://youtu.be/ASr6aP6JxlU)  

## 🌐 Live Demo

Try it live: [https://monkey-bytes.onrender.com](https://monkey-bytes.onrender.com)

## 💡 Features

- 📧 Email Signup with OTP Verification
- 🔐 Login with Password or OTP
- 📰 Category-specific Subscriptions
- 📋 User Dashboard with Dynamic News Preferences
- 🌗 Dark/Light Mode Toggle
- 🗃 Archive for Previous News Posts
- ⚠️ Form Alerts and Notifications

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: PostgreSQL with psycopg2
- **Frontend**: HTML, Custom CSS (Bootstrap-like), JavaScript
- **Email**: Flask-Mail
- **Environment**: `.env` configuration for credentials

## 🚀 How to Run (Localhost)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sricharan106/Monkey-bytes.git
   cd monkey-bytes
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Set Environment Variables**
   Create a .env file with:
    EMAIL_USER=your_email@example.com
    EMAIL_PASS=your_password_or_app_password
    DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/yourdbname

4. **Run the App**
   ```bash
   flask run

Parsi Sricharan
Final Project for CS50x 2025
Built with ❤️ using Flask, PostgreSQL, and CSS.
