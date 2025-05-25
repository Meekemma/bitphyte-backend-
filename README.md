

````markdown
# Bitphyte

**Bitphyte** is a robust financial backend system built with Django and Django REST Framework. It handles core functionalities like user management, wallet operations, deposits, withdrawals, and interest accrual via scheduled cron jobs. Designed with scalability, security, and flexibility in mind, it powers financial applications with ease.

---

## 🚀 Features

- User Authentication & Profile Management  
- Deposit & Withdrawal Management  
- Interest Calculation (via daily cron jobs using [cron-job.org](https://cron-job.org))  
- Admin Dashboard Support  
- Swagger UI for API documentation  
- Secure and modular Django architecture  

---

## 🛠 Tech Stack

- Python 3.11+
- Django 4+
- Django REST Framework
- PostgreSQL (or your DB of choice)
- [cron-job.org](https://cron-job.org) for scheduled tasks (no need for Redis/Celery)

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Meekemma/bitphyte-backend-.git

# Navigate to the project
cd bitphyte-backend-

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
````

---

## 🔐 Environment Variables

Create a `.env` file and add the following:

```env
SECRET_KEY=your_generated_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=your_database_connection_url
```

### 🔑 Generate a Secret Key

To generate a Django secret key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 🌐 API Documentation

API docs are available at:

```
/swagger/
```

Login via the Django admin or obtain a token via `/api/token/`.

---

## 📬 Contact

For questions or support, reach out:

**Developer:** Meekemma
**Email:** [ibehemmanuel32@gmail.com](mailto:ibehemmanuel32@gmail.com)

---

## 📝 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---
