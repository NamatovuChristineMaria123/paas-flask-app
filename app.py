from flask import Flask, render_template
from datetime import datetime
import socket
import os
import platform
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    # Generate a unique session ID for demo purposes
    session_id = str(uuid.uuid4())[:8]
    
    return render_template('index.html',
                         current_time=datetime.now().strftime("%H:%M:%S"),
                         current_date=datetime.now().strftime("%B %d, %Y"),
                         hostname=socket.gethostname(),
                         platform_info=platform.python_version(),
                         session_id=session_id,
                         message="Your application is running inside a Docker container deployed via Coolify")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)