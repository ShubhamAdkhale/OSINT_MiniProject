import os
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'development')

with app.app_context():
    db.create_all()
    print('Database initialized successfully!')
