web: python manage.py migrate && python reset_and_init_db.py && daphne -b 0.0.0.0 -p ${PORT:-8000} grocery_store.asgi:application
