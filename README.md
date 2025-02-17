# 💌 Serenade

✨ Inspired by [Receiptify](https://receiptify.herokuapp.com/ "Receiptify"), Serenade is a multipurpose tool that allows users to create 'virtual date cards' for their loved individual and their dates, and displays a user's top most played tracks on Spotify & Last.fm (soon).

---

<div align=center>

[![Serenade - 0.0.4 beta](https://img.shields.io/badge/Serenade-0.0.4_beta-2ea44f)](https://serenade.thetwlight.xyz) [![dependency - django](https://img.shields.io/badge/dependency-django-blue?logo=django&logoColor=white)](https://pypi.org/project/django) [![Instagram - @raianxh_](https://img.shields.io/badge/Instagram-%40raianxh__-2ea44f?logo=instagram&logoColor=white)](https://instagram.com/raianxh_)

</div>

## 🌟 What is Serenade?  
- **Serenade** is a web applications that can create personalized **date invitations**, and create your ultimate music recap from Spotify & Last.fm. It has two parts:
  - 💌 **Will You Date Me? (WYDM)** – Create personalized and digitalized date invitations that truly stand out. Will you date me?
  - 🎧 **Serenade Recap** – Display your top tracks, artists, genres, and top trends with many colors to choose. Style your recap as if it will impress someone!

<div align=center>
<i>Music meets connection. 🎶 </i>
</div>


---

## ✨ Features  
✅ **Spotify Recap, with variations!** – View your top tracks, artists, genres, & trends in a simple yet lovely design. Choose up to 5 colors for your preference!
✅ **Custom Date Invitations** – Send personalized **date invitations** with unique slugs, which your other half can access it uniquely.  
✅ **Beautiful Auto-Generated Images** – Every recap & invite is instantly converted into a **shareable image** that can be accessible in your gallery. Save the moment!
✅ **Fully Mobile-Friendly** – Designed to **look & feel amazing** on any device.  

<div align=center>
<i>Your song, their spark.</i>
</div>

---

## 🎨 Screenshots
<div align=center>
    <img src='https://cdn.discordapp.com/attachments/758981769923657758/1340955677337583637/image.png?ex=67b43dcb&is=67b2ec4b&hm=40d3a24e32357812589e23dd44adfe0ddefbbcbaeed81f271c5171dda94e3a14&' width=80% height=80% alt='Preview #1'/>
    <img src='https://cdn.discordapp.com/attachments/758981769923657758/1340956029461987418/image.png?ex=67b43e1f&is=67b2ec9f&hm=99c6a2900c5844988b02fd64683c282ffc67acfc23ef81c9509664bdd31918fb&' width=80% height=80% alt='Preview #2'>
    <img src='https://cdn.discordapp.com/attachments/758981769923657758/1340957010862145566/image.png?ex=67b43f09&is=67b2ed89&hm=604190e85ef770d9102e95967673808d48839fae632145b402073c9ee4835b91&' width=80% height=80% alt='Preview #3'>
    <img src='https://cdn.discordapp.com/attachments/758981769923657758/1340956906545610752/image.png?ex=67b43ef0&is=67b2ed70&hm=5758b4ff397dfaf58a9e700d66dc60b59792c3af6a2f12ee83d5dfe2f39216d8&' width=80% height=80% alt='Preview #4'>
    <img src='https://cdn.discordapp.com/attachments/758981769923657758/1340956573216014387/image.png?ex=67b43ea0&is=67b2ed20&hm=af43e5252c7374caa3f8cb05a047befcf2570359abac78f5203dc02bdd89638f&' width=80% height=80% alt='Preview #5'>
</div>

---

## 🚀 Installation & Setup  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/raianah/serenade.git
cd serenade
```

- If you know how to deal with django, you can do
```sh
django-admin startproject <folder-name>
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Your Environment
- Spotify clients can be generated [here](https://developer.spotify.com/).
- Last.fm clients can be generated [here](https://www.last.fm/api/authentication).
- `.env` should be in root folder
```sh
export SPOTIPY_CLIENT_ID="your-client-id"
export SPOTIPY_CLIENT_SECRET="your-client-secret"
export SPOTIPY_REDIRECT_URI="http://localhost:8000/callback/"

export LASTFM_API_KEY = "your-api-key"
export LASTFM_API_SECRET = "your-api-secret"

export DB_USER = 'your-database-username'
export DB_PASS = 'your-database-password'
export DB_HOST = '127.0.0.1' # or your IP if you are hosting on a different server
export DB_PORT = '8000' # Default: 8000. Change this if you are hosting on a different server
```

### 4️⃣ Set Up Your Database Information
- You can pick between PostgreSQL, MySQL / MariaDB, or SQLite. You can name your database anything you want. Consider the checks that the project can use.
  - There should be atleast one (1) table.
  - There should be atleast five (5) columns inside the table.
  - If PostgreSQL was used, you must name the database first.

### 4️⃣ Connect Your Database Information
- `wydm_project/settings.py` - PostgreSQL
  - `psycopg[binary]` library must be installed.
```py
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name', # Change this to your database name
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASS"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}
```
- `wydm_project/settings.py` - MySQL / MariaDB
  - `mysqlclient` library must be installed.
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name', # Change this to your database name
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASS"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}
```
- `wydm_project/settings.py` - SQLite3
  - `sqlite3` must be installed (should be pre-installed along with python).
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3", # change db.sqlite3 to your SQLite DB name
    }
}
```
- After modifying `wydm_project/settings.py`, head to `wydm_app/models.py` and begin modifying the columns and tables you have created.
```py
from django.db import models
import uuid

class Invitation(models.Model):
    sender_name = models.CharField(max_length=100, db_column="your-table-column")
    recipient_name = models.CharField(max_length=100, db_column="your-table-column")
    slug = models.SlugField(unique=True, default=uuid.uuid4, db_column="your-table-column", primary_key=True)
    option = models.IntegerField(db_column="your-table-column")
    message = models.TextField(db_column="your-table-column", default="")

    class Meta:
        db_table = "your-table-name"
```

### 4️⃣ Run the Server
```sh
python manage.py migrate
python manage.py runserver
```

---

## 🚀 Official Website
- [Click me!](https://www.serenade.thetwlight.xyz)