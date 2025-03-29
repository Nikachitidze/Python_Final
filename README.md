
# 🚗 AutoRent – Final Django Project

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.1-success?style=for-the-badge&logo=django)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

---

## 📌 Overview

**AutoRent** is a full-stack Django-based platform that allows users to **rent**, **upload**, and **manage** car listings.

This project was developed as a final coursework at **IT Step Academy** and demonstrates high-level Django capabilities, clean UI/UX with Bootstrap, email integration, and real-world car management features.

🔗 GitHub Repo: [Aleksandre16/IT_Step_Final](https://github.com/Aleksandre16/IT_Step_Final)

---

## ⚙️ Features

- ✅ **User Registration with Email Verification**
- 🔐 **Forgot Password with Email Code**
- 📥 **Add Car with Multiple Images**
- 📍 **Optional Map View (Google Maps Embed)**
- 📱 **Blurred Phone Number (Reveal-on-Click)**
- 🧮 **Live Rent Calculator with Slider**
- ⭐ **Favorites System with Toggle Icon**
- 🔔 **Notification System (Bell + Page View)**
- ✉️ **Emails Sent on Rental (to Owner & Renter)**
- 🧾 **User Dashboard: Rentals, Favorites, Uploads**
- 🗑️ **Delete Car or Rent (Confirmation Required)**
- 📤 **CSV Upload Support with Faker-Generated Cars**
- 🔍 **Powerful Filtering: Brand, City, Price, Transmission, Phone**

---

## 🏗️ Installation Guide

### 🔧 Step 1: Clone & Setup

```bash
git clone https://github.com/Aleksandre16/IT_Step_Final.git
cd IT_Step_Final
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ⚙️ Step 2: Migrate Database & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 🚀 Step 3: Run Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## 📦 CSV Car Import (Faker)

Want to fill your site with 100+ cars instantly? Do this:

1. Make sure this file exists: `media/default.jpg`  
2. Place your CSV at: `media/csv/cars.csv`
3. Run the import command:

```bash
python manage.py import_cars
```

All imported cars will be assigned to the first superuser and use the default image.

---

## 🗂️ Project Structure

```
📦 IT_Step_Final/
│
├── core/                   # Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── media/                 # Uploaded images & CSVs
│   ├── csv/
│   └── default.jpg
│
├── static/                # Custom CSS / JS
├── templates/             # All HTML templates
│   ├── base.html
│   ├── car_detail.html
│   ├── rent_car.html
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 💡 Tech Stack

| Tool             | Description                                 |
|------------------|---------------------------------------------|
| 🐍 Python 3.12     | Backend programming language                |
| 🌱 Django 5.1      | Web framework with built-in admin & ORM     |
| 🗃️ SQLite           | Local database (easily switchable)         |
| 🧪 Faker           | Auto-generate fake car data for testing     |
| 💌 Django Email    | Used for email verification & password reset |
| 🔐 Django Auth     | Secure login, logout, user protection       |
| 🎨 Bootstrap 5     | Beautiful responsive frontend styling       |

---

## 👤 Developer

Made by **Aleksandre Kolbini**  
Final project for **IT Step Academy**

[![GitHub](https://img.shields.io/badge/GitHub-Aleksandre16-black?style=flat&logo=github)](https://github.com/Aleksandre16)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/aleksandre-kolbini-266219254/)  
📧 kolbinialeksandre@gmail.com

---

## 📜 License

This project is for educational purposes.  
You are free to fork, modify, and use it for learning.

---
