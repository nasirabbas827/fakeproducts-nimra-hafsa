# fakeproducts-nimra-hafsa  

A small Django‑based web application that demonstrates a fake‑product catalogue with comment handling, IP tracking, and basic CRUD operations. The project is structured for easy extension and serves as a learning reference for Django fundamentals.

---  

## Overview  

`fakeproducts-nimra-hafsa` is a starter Django project that:

* Serves a catalogue of dummy products.  
* Allows visitors to leave comments on each product.  
* Tracks the IP address of each comment (via the `IPTracking` model).  
* Includes basic admin integration for managing products and comments.  

The repository contains the full Django project (`fakeproducts`) and a single app (`myapp`) where the core logic lives.

---  

## Features  

| Feature | Description |
|---------|-------------|
| **Product catalogue** | Simple static pages rendered with HTML templates. |
| **Comment system** | Users can submit comments; each comment stores the author, text, timestamp, and IP address. |
| **IP tracking** | A dedicated `IPTracking` model records the IP address of each comment for audit purposes. |
| **Admin interface** | Full Django admin support for products, comments, and IP logs. |
| **Migrations** | Incremental migrations illustrate schema evolution (e.g., adding unique constraints). |
| **ASGI/WSGI ready** | Both `asgi.py` and `wsgi.py` are provided for flexible deployment. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Framework** | Django 4.x |
| **Language** | Python 3.9+ |
| **Database** | SQLite (default) – can be swapped for PostgreSQL, MySQL, etc. |
| **Frontend** | HTML5 + minimal CSS (served via Django templates) |
| **Deployment** | ASGI (`asgi.py`) & WSGI (`wsgi.py`) entry points |
| **Version Control** | Git |

---  

## Installation  

> **Prerequisites**  
> - Python 3.9 or newer  
> - `pip` (or `pipenv` / `poetry` if you prefer)  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/fakeproducts-nimra-hafsa.git
cd fakeproducts-nimra-hafsa

# 2️⃣ Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt   # (Create this file if not present: Django>=4.0)

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Create a superuser for the admin site
python manage.py createsuperuser
# Follow the prompts – use YOUR_OWN_API_KEY for any placeholder fields if required.

# 6️⃣ Run the development server
python manage.py runserver
```

The site will be reachable at `http://127.0.0.1:8000/`.  
Access the admin panel at `http://127.0.0.1:8000/admin/`.

---  

## Usage  

### Basic workflow  

1. **Visit the homepage** – browse the list of fake products.  
2. **Open a product detail page** – view product information and existing comments.  
3. **Add a comment** – fill out the comment form; the server automatically records your IP address.  
4. **Admin management** – log in to `/admin/` to add/edit products, moderate comments, or view IP logs.  

### Customising the project  

* **Add new products** – edit `myapp/models.py` to extend the `Product` model, then run `makemigrations` & `migrate`.  
* **Switch database** – modify `fakeproducts/settings.py` → `DATABASES` section with