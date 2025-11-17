"""Recreate database with rich_metadata column"""
import os
from app import create_app, db

# Remove old database
db_path = 'osint_fraud.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✅ Deleted old database: {db_path}")

# Create new database with updated schema
app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Database recreated successfully with rich_metadata column!")
    print("🎯 You can now analyze phone numbers with enhanced metadata.")
