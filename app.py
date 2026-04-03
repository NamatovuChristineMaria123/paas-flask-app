from flask import Flask, render_template, request
from datetime import datetime
import socket
import os
import platform
import uuid
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///visits.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# A simple model for tracking visits
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    # Record this visit
    visit = Visit(ip_address=request.remote_addr)
    db.session.add(visit)
    db.session.commit()
    
    # Get total visit count
    total_visits = Visit.query.count()
    
    # Generate a unique session ID for demo purposes
    session_id = str(uuid.uuid4())[:8]
    
    return render_template('index.html',
                         current_time=datetime.now().strftime("%H:%M:%S"),
                         current_date=datetime.now().strftime("%B %d, %Y"),
                         hostname=socket.gethostname(),
                         platform_info=platform.python_version(),
                         session_id=session_id,
                         visit_count=total_visits,  # NEW: pass visit count to template
                         message="Your application is running inside a Docker container deployed via Railway")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)