from app import db

# Database model: Submission (vehicle usage record)
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(50))  # Format like "2025-03-10 08:00 (Monday)"
    end_date = db.Column(db.String(50))    # Format like "2025-03-10 12:00 (Monday)"
    driver = db.Column(db.String(50))
    plate = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    vtype = db.Column(db.String(50))

# Database model: Note (custom note)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
