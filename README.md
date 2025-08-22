# Simple Password Manager

A small Python program that helps you save and manage your passwords.

---

## What it Does

- Save usernames and passwords based on the site. 
- Find your saved passwords easily  
- Update your username or password
- Delete your password record by passing the site name and username.
- You could save multiple username with passwords for each site.  

---

## What You Need

- **Python 3**  
- The libraries in `requirements.txt`

---

## How to Install

1. Download (clone) this project:

   ```bash
   git clone https://github.com/farshadahn7/Simple_password_manager.git
   cd Simple_password_manager
2. optional, Make virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Install the needed libraries:
   ```bash
   pip install -r requirements.txt
4. Modify the .env file with your own DB information
   ```bash
   DB_NAME = "your db name"
   DB_USER = "your db user name"
   DB_PASS = "your db password"
   DB_HOST = "localhost"
   DB_PORT = "default value is 5432"
6. Run the main file
   ```bash
   python main.py
## Licences
- This project uses the MIT License.
- Created by Farshad ahn
