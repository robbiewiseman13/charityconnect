# CharityConnect – Final Year Project

## Overview
CharityConnect is a web platform built with Django that enables event organisers to create verified fundraising events, manage donations, and improve transparency for donors. It integrates **Stripe** for secure payments, **Redis + Celery** for background task processing, and **OpenAI** for AI-assisted content generation.

## Technologies
- Django / Python 3.14
- PostgreSQL
- Redis + Celery
- Stripe API
- OpenAI GPT
- Django REST Framework + drf-spectacular

## Setup (Windows)
```powershell
cd backend
python -m venv ..\.venv
& "..\.\.venv\Scripts\Activate.ps1"
pip install -r requirements.txt
Copy-Item .\.env.example .\.env
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
