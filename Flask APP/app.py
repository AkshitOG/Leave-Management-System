from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

import os
load_dotenv()

from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.employee_routes import emp_bp
from routes.hr_routes import hr_bp
from routes.leave_routes import leave_bp

app = Flask(__name__)

app.secret_key = os.getenv("secret_key")

app.register_blueprint(auth_bp, url_prefix = "/auth")
app.register_blueprint(admin_bp, url_prefix = "/admin")
app.register_blueprint(emp_bp)
app.register_blueprint(hr_bp)
app.register_blueprint(leave_bp, url_prefix = "/leaves")

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)