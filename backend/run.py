import os
from app import create_app, db
from app.models.phone_analysis import PhoneAnalysis
from app.models.risk_factor import RiskFactor

app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'PhoneAnalysis': PhoneAnalysis,
        'RiskFactor': RiskFactor
    }

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    # Add sample data here if needed
    print('Database seeded!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
