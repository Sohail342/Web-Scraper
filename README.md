# 🕷️ FastAPI Web Scraper

A web scraper API built with **FastAPI**, featuring authentication using **JWT access & refresh tokens**.

## 🚀 Features
- Scrapes data from websites
- Uses **FastAPI** for a high-performance backend
- Implements **JWT authentication** (Access & Refresh Tokens)
- Asynchronous database support with **SQLAlchemy + PostgreSQL**
- Secure password hashing & verification

---

## 📥 Installation & Setup

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/Sohail342/Web-Scraper.git
cd Web-Scraper
```

### 2️⃣ Create & Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On MacOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables (.env)
```bash
Create a .env file in the root directory or edit .env_example:
DATABASE_URL=YOURDATABASEURL
SECRET_KEY=YourSecretKey

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=YOUREMAIL
EMAIL_PASSWORD=YOURGENERATEDPASSWORD

POSTGRES_USER=DBUSER
POSTGRES_PASSWORD=DBPASSWORD
POSTGRES_DB=DATABASENAME
```
### 5️⃣ Run the Application
```bash
uvicorn main:app --reload
```
API Docs will be available at http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc

## Contact
If you have any questions or feedback, feel free to reach out:
<p align="left">
<a href="https://wa.me/+923431285354" target="blank"><img align="center" src="https://img.icons8.com/color/48/000000/whatsapp.png" alt="WhatsApp" height="30" width="40" /></a>
<a href="https://www.hackerrank.com/sohail_ahmad342" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/hackerrank.svg" alt="sohail_ahmad342" height="30" width="40" /></a>
<a href="https://www.linkedin.com/in/sohailahmad3428041928/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="sohail-ahmad342" height="30" width="40" /></a>
<a href="https://instagram.com/sohail_ahmed113" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="sohail_ahmed113" height="30" width="40" /></a>
<a href="mailto:sohailahmed34280@gmail.com" target="blank"><img align="center" src="https://img.icons8.com/ios-filled/50/000000/email-open.png" alt="Email" height="30" width="40" /></a>
</p>