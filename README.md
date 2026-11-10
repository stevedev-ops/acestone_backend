# Acestone Jewellery — Django Backend API

Production-grade Backend REST API for **Acestone Jewellery** (Nairobi, Kenya) Point of Sale and Inventory Management System.

## 🏛️ Architecture & Tech Stack
- **Framework**: Python 3.12, Django 5.x, Django REST Framework
- **Authentication**: JWT authentication with custom User roles (`OWNER`, `MANAGER`, `EMPLOYEE`) and supervisor PIN verification
- **Concurrency Protection**: Row-level locking with `select_for_update()` during sales checkout
- **Media & Documents**:
  - Pillow image optimization for macro jewellery photography
  - ReportLab PDF receipt generator (thermal 80mm & A4)
  - OpenPyXL financial & inventory report exports
- **Audit Logging**: Immutable audit trail for every price change, sale, return, discount approval, and stock relocation
- **M-Pesa Architecture**: Daraja STK Push & Webhook settlement listener

## 🚀 Setup & Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

