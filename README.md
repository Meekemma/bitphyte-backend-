
````markdown
# Bitphyte

**Bitphyte** is a backend system for a financial platform built using Django and Django REST Framework. It handles core financial operations such as user account management, payments, interest calculations, and withdrawals. The system also uses scheduled tasks powered by [cron-job.org](https://cron-job.org/) for periodic interest accruals.

---

## 🚀 Features

- User registration and profile management  
- Daily interest accrual on user payments  
- Secure withdrawal system (bank & crypto)  
- Role-based access & authentication  
- Swagger UI for API documentation  
- Cron-based task scheduling (via cron-job.org)

---

## ⚙️ Tech Stack

- Python 3.11  
- Django  
- Django REST Framework  
- PostgreSQL (recommended for production)  
- Swagger (for API documentation)  
- [cron-job.org](https://cron-job.org) (for scheduling)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Meekemma/bitphyte-backend-.git
cd bitphyte-backend-
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate a Django SECRET\_KEY

Run the following in your terminal or Python shell:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and set it in your `.env` file or directly in `settings.py`:

```env
SECRET_KEY=your_generated_key_here
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Start Development Server

```bash
python manage.py runserver
```

---

## 🗓️ Scheduled Tasks

Bitphyte uses [cron-job.org](https://cron-job.org) to run daily background tasks such as applying interest to user balances. This eliminates the need for Redis or Celery.

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for more information.

---

## 📢 Notes

* API documentation is available at `/swagger/`.
* No need to manually interact with endpoints; use the Swagger UI for frontend/backend collaboration.


