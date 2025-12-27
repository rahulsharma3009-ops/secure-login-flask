from flask import Flask, render_template, request
from datetime import datetime
from detector import detectattack
import os
app = Flask(__name__)
import time
blocked_ips={}
BLOCK_DURATION = 60
MAX_FAILS = 5
#Dummy credentials (demo only)
VALID_USERNAME = "admin"
VALID_PASSWORD= "admin123"
LOG_FILE = "logs/login.log"
#Ensure log file exists
os.makedirs("logs", exist_ok=True)
open(LOG_FILE, "a").close()
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    remaining_time = 0
    ip = request.remote_addr
    import time
    if ip in blocked_ips:
        if time.time()<blocked_ips[ip]:
            message=f"YOUR IP IS TEMPORARILY BLOCKED DUE TO SEVERAL FAILED ATTEMPTS. TRY AGAIN LATER"
            return render_template("logim.html",message=message,remaining_time=remaining_time)

        else:
            blocked_ips.pop(ip)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ip = request.remote_addr
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            status = "SUCCESS"
            message = "'Login Successful"
        else:
            status = "FAIL"
            message = "Invalid Credentials"
# Write login attempt to log
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} {ip} {status}\n")
# Detect brute-force attack
    if detectattack(LOG_FILE):
        blocked_ips[ip] = time.time() + BLOCK_DURATION
        remaining_time= BLOCK_DURATION
        message = "Suspicious brute-force activity detected!"
    return render_template("login.html", message=message,remaining_time=remaining_time)
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)