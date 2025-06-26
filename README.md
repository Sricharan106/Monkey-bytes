# 🐵 Monkey Bytes

Monkey Bytes is a clean newsletter web app that lets users subscribe to specific news categories like Tech, Sports, and Entertainment. It features email verification via OTP, a dashboard for managing subscriptions, and a dark/light theme switch — all built with Flask and PostgreSQL.

## 📽 Demo Video

[Watch the Demo](https://youtu.be/ASr6aP6JxlU)

## 🌐 Live Demo

Try it live: [https://monkey-bytes.onrender.com](https://monkey-bytes.onrender.com)

##  Description

Monkey Bytes is a full-featured newsletter web application that allows users to subscribe to curated news categories like Tech, Sports, and Entertainment. It features email verification using OTP, and lets users log in securely and manage their dynamic news preferences via a dashboard. This project was built using Flask and PostgreSQL to handle backend logic and database storage. I built this as part of CS50x to explore full-stack development, improve my skills with Python web frameworks, and work with user authentication and theming features. Users can toggle between light/dark modes, view archived news, and receive real-time alerts for form actions.
- 📧 **Email Signup with OTP Verification**
  Users verify their identity through a one-time password sent via email, enhancing security without relying solely on traditional passwords.

- 🔐 **Login with Password or OTP**
  Offers flexibility by allowing users to either log in using a saved password or request a new OTP each time.

- 📰 **Customizable Category Subscriptions**
  Users can select one or more news categories (Tech, Anime and Both) during registration or through their dashboard. Future emails only include their selected preferences.

- 📋 **Personalized Dashboard**
  Logged-in users get access to a dashboard where they can manage their subscription settings, switch themes, and view their archive.

- 🌗 **Dark/Light Mode Toggle**
  A clean UI with an accessible toggle for theme preference. Your preference persists between sessions.

- 🗃 **Archive System**
  View previous newsletter posts in a dedicated archive section — useful for catching up or revisiting important updates.

- ⚠️ **Alerts and Notifications**
  Friendly form validations, flash messages, and UI alerts for every major user action (e.g., signup errors, login success, subscription changes).


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
