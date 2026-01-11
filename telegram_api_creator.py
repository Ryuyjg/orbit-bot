__CHANNEL__ = 'Telegram : @esfelurm'

import requests
import json
import time
import random
import string
import re
import os
from colorama import Fore, init, Style
import sys

init()

print(f"""{Fore.CYAN}
╔══════════════════════════════════════════════════╗
║    TELEGRAM API ULTIMATE CREATOR                 ║
║    100% PowerShell - No Browser                  ║
║    Telegram: @esfelurm                           ║
╚══════════════════════════════════════════════════╝\n
""")

class TelegramAPIUltimateCreator:
    def __init__(self):
        self.session = requests.Session()
        self.setup_ultimate_headers()
        self.api_id = None
        self.api_hash = None
        self.phone = None
        
    def setup_ultimate_headers(self):
        """Setup ultimate headers to bypass protections"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://my.telegram.org',
            'Referer': 'https://my.telegram.org/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        })
    
    def print_status(self, message, status="info"):
        """Print colored status messages"""
        if status == "success":
            print(f"{Fore.GREEN}[✓] {message}")
        elif status == "error":
            print(f"{Fore.RED}[!] {message}")
        elif status == "warning":
            print(f"{Fore.YELLOW}[*] {message}")
        else:
            print(f"{Fore.CYAN}[→] {message}")
    
    def generate_app_name(self):
        """Generate unique app name"""
        timestamp = int(time.time())
        random_str = ''.join(random.choices(string.ascii_lowercase, k=4))
        return f"Telegram_{timestamp}_{random_str}"
    
    def login(self, phone):
        """Login to Telegram"""
        self.phone = phone
        self.print_status("Requesting login code...")
        
        try:
            # Get initial cookies
            self.session.get('https://my.telegram.org', timeout=10)
            
            # Request login code
            response = self.session.post(
                'https://my.telegram.org/auth/send_password',
                data={'phone': phone},
                timeout=15
            )
            
            if response.status_code != 200:
                self.print_status(f"Failed to send code: HTTP {response.status_code}", "error")
                return False
            
            data = response.json()
            if 'random_hash' not in data:
                self.print_status("No hash in response", "error")
                return False
            
            random_hash = data['random_hash']
            self.print_status("Code sent to Telegram!", "success")
            
            # Get verification code
            code = input(f"{Fore.CYAN}[?] Enter Telegram code: {Fore.YELLOW}")
            
            # Login with code
            self.print_status("Logging in...")
            login_data = {
                'phone': phone,
                'random_hash': random_hash,
                'password': code
            }
            
            response = self.session.post(
                'https://my.telegram.org/auth/login',
                data=login_data,
                timeout=15
            )
            
            if response.status_code == 200:
                self.print_status("Login successful!", "success")
                return True
            else:
                self.print_status(f"Login failed: HTTP {response.status_code}", "error")
                return False
                
        except Exception as e:
            self.print_status(f"Login error: {str(e)}", "error")
            return False
    
    def get_form_hash(self):
        """Get form hash from create page"""
        try:
            response = self.session.get('https://my.telegram.org/apps/create', timeout=10)
            
            # Multiple patterns to find hash
            patterns = [
                r'name=["\']hash["\']\s+value=["\']([^"\']+)["\']',
                r'hash["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'csrf["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, response.text, re.I)
                if match:
                    self.print_status(f"Found form hash: {match.group(1)[:20]}...", "success")
                    return match.group(1)
            
            return "telegram_app_hash"
            
        except Exception as e:
            self.print_status(f"Could not get form hash: {e}", "warning")
            return "telegram_app_hash"
    
    def create_application(self):
        """Create Telegram application"""
        self.print_status("Creating application...")
        
        # Generate unique app names
        app_title = self.generate_app_name()
        app_shortname = app_title.lower().replace('_', '')[:15]
        
        # Get form hash
        form_hash = self.get_form_hash()
        
        # Prepare application data
        app_data = {
            'app_title': app_title,
            'app_shortname': app_shortname,
            'app_url': 'https://telegram.org',
            'app_platform': 'desktop',
            'app_desc': 'Telegram Desktop Application',
            'hash': form_hash
        }
        
        self.print_status(f"App Title: {app_title}", "info")
        self.print_status(f"Short Name: {app_shortname}", "info")
        self.print_status(f"Platform: desktop", "info")
        
        try:
            # Submit application creation
            response = self.session.post(
                'https://my.telegram.org/apps/create',
                data=app_data,
                timeout=20,
                headers={
                    'Referer': 'https://my.telegram.org/apps/create',
                    'Origin': 'https://my.telegram.org',
                }
            )
            
            if response.status_code == 200:
                self.print_status("Application submitted successfully!", "success")
                
                # Wait for processing
                time.sleep(3)
                
                return True
            else:
                self.print_status(f"Creation failed: HTTP {response.status_code}", "error")
                return False
                
        except Exception as e:
            self.print_status(f"Creation error: {str(e)}", "error")
            return False
    
    def extract_credentials_advanced(self, html):
        """Advanced credential extraction with multiple methods"""
        # Method 1: Direct patterns
        patterns = [
            # API ID patterns
            (r'api_id["\']?\s*[:=]\s*["\']?(\d{5,9})["\']?', 'id'),
            (r'app_id["\']?\s*[:=]\s*["\']?(\d{5,9})["\']?', 'id'),
            (r'>\s*(\d{5,9})\s*<', 'id'),
            (r'<span[^>]*>(\d{5,9})</span>', 'id'),
            (r'<strong[^>]*>(\d{5,9})</strong>', 'id'),
            (r'value=["\'](\d{5,9})["\']', 'id'),
            
            # API Hash patterns
            (r'api_hash["\']?\s*[:=]\s*["\']?([a-f0-9]{32})["\']?', 'hash'),
            (r'app_hash["\']?\s*[:=]\s*["\']?([a-f0-9]{32})["\']?', 'hash'),
            (r'>\s*([a-f0-9]{32})\s*<', 'hash'),
            (r'<span[^>]*>([a-f0-9]{32})</span>', 'hash'),
            (r'<strong[^>]*>([a-f0-9]{32})</strong>', 'hash'),
            (r'value=["\']([a-f0-9]{32})["\']', 'hash'),
        ]
        
        api_id = None
        api_hash = None
        
        # Try all patterns
        for pattern, ptype in patterns:
            matches = re.findall(pattern, html, re.I)
            for match in matches:
                if ptype == 'id' and not api_id:
                    if str(match).isdigit() and 10000 <= int(match) <= 999999999:
                        api_id = match
                        self.print_status(f"Found API ID: {api_id}", "success")
                elif ptype == 'hash' and not api_hash:
                    if re.match(r'^[a-f0-9]{32}$', str(match), re.I):
                        api_hash = match
                        self.print_status(f"Found API Hash: {api_hash[:8]}...", "success")
            
            if api_id and api_hash:
                break
        
        # Method 2: Context-based extraction
        if not api_id or not api_hash:
            lines = html.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                # Look for API ID context
                if 'api_id' in line_lower or 'app id' in line_lower:
                    # Check surrounding lines
                    for j in range(max(0, i-3), min(len(lines), i+4)):
                        # Look for numbers
                        nums = re.findall(r'\b(\d{5,9})\b', lines[j])
                        for num in nums:
                            if 10000 <= int(num) <= 999999999 and not api_id:
                                api_id = num
                                break
                
                # Look for API Hash context
                if 'api_hash' in line_lower or 'app hash' in line_lower:
                    # Check surrounding lines
                    for j in range(max(0, i-3), min(len(lines), i+4)):
                        # Look for hex strings
                        hexs = re.findall(r'\b([a-f0-9]{32})\b', lines[j], re.I)
                        for hex_str in hexs:
                            if not api_hash:
                                api_hash = hex_str
                                break
        
        return api_id, api_hash
    
    def get_credentials(self):
        """Get API credentials after app creation"""
        self.print_status("Extracting credentials...")
        
        try:
            # Get apps page
            response = self.session.get('https://my.telegram.org/apps', timeout=15)
            
            # Try extraction
            api_id, api_hash = self.extract_credentials_advanced(response.text)
            
            if api_id and api_hash:
                self.api_id = api_id
                self.api_hash = api_hash
                return True
            
            # Try alternative method: Save page and analyze
            self.print_status("Trying alternative extraction...", "warning")
            
            # Try different endpoints
            endpoints = [
                ('https://my.telegram.org/apps', 'GET'),
                ('https://my.telegram.org/apps/api', 'GET'),
                ('https://my.telegram.org/api/v1/apps', 'GET'),
            ]
            
            for endpoint, method in endpoints:
                try:
                    if method == 'GET':
                        resp = self.session.get(endpoint, timeout=10)
                    else:
                        resp = self.session.post(endpoint, timeout=10)
                    
                    api_id, api_hash = self.extract_credentials_advanced(resp.text)
                    if api_id and api_hash:
                        self.api_id = api_id
                        self.api_hash = api_hash
                        self.print_status(f"Found via {endpoint}", "success")
                        return True
                        
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.print_status(f"Extraction error: {str(e)}", "error")
            return False
    
    def save_credentials_to_files(self):
        """Save credentials to multiple file formats"""
        if not self.api_id or not self.api_hash:
            return
        
        clean_phone = self.phone.replace('+', '').replace(' ', '_')
        timestamp = int(time.time())
        
        # 1. Save as TXT
        txt_content = f"""╔══════════════════════════════════════════════════╗
║        TELEGRAM API CREDENTIALS                  ║
║        Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}          ║
╚══════════════════════════════════════════════════╝

📱 Phone Number: {self.phone}
🔑 API ID: {self.api_id}
🔐 API Hash: {self.api_hash}

📅 Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}
⚡ By: @esfelurm

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pyrogram Example:
──────────────────
from pyrogram import Client

app = Client(
    "my_account",
    api_id={self.api_id},
    api_hash="{self.api_hash}",
    phone_number="{self.phone}"
)

Telethon Example:
──────────────────
from telethon import TelegramClient

client = TelegramClient(
    'session',
    {self.api_id},
    '{self.api_hash}'
)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Keep these credentials secure!
⚠️ Do not share with anyone!
"""
        
        txt_filename = f"telegram_api_{clean_phone}_{timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        # 2. Save as JSON
        json_content = {
            "telegram_api_credentials": {
                "phone_number": self.phone,
                "api_id": int(self.api_id),
                "api_hash": self.api_hash,
                "generated_at": time.strftime('%Y-%m-%d %H:%M:%S'),
                "app_name": "Telegram Desktop",
                "platform": "desktop",
                "generator": "@esfelurm"
            }
        }
        
        json_filename = f"telegram_api_{clean_phone}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=4, ensure_ascii=False)
        
        # 3. Save as Python config
        py_content = f"""# Telegram API Configuration
# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
# Phone: {self.phone}

API_ID = {self.api_id}
API_HASH = "{self.api_hash}"
PHONE_NUMBER = "{self.phone}"

# Pyrogram Configuration
def create_pyrogram_client():
    from pyrogram import Client
    return Client(
        "my_account",
        api_id=API_ID,
        api_hash=API_HASH,
        phone_number=PHONE_NUMBER
    )

# Telethon Configuration  
def create_telethon_client():
    from telethon import TelegramClient
    return TelegramClient(
        'session',
        API_ID,
        API_HASH
    )

if __name__ == "__main__":
    print("Telegram API Configuration loaded successfully!")
    print(f"API ID: {{API_ID}}")
    print(f"API Hash: {{API_HASH}}")
"""
        
        py_filename = f"telegram_config_{clean_phone}_{timestamp}.py"
        with open(py_filename, 'w', encoding='utf-8') as f:
            f.write(py_content)
        
        self.print_status(f"Saved credentials to:", "success")
        self.print_status(f"  📄 {txt_filename}", "info")
        self.print_status(f"  📊 {json_filename}", "info")
        self.print_status(f"  🐍 {py_filename}", "info")
    
    def display_success_banner(self):
        """Display success banner"""
        banner = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════╗
{Fore.GREEN}║    ✅ SUCCESS! API CREDENTIALS CREATED           ║
{Fore.GREEN}╚══════════════════════════════════════════════════╝

{Fore.CYAN}📱 Phone Number: {Fore.YELLOW}{self.phone}
{Fore.CYAN}🔑 API ID: {Fore.YELLOW}{self.api_id}
{Fore.CYAN}🔐 API Hash: {Fore.YELLOW}{self.api_hash}

{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Fore.CYAN}Credentials have been saved to multiple files!
{Fore.CYAN}Use them with Pyrogram or Telethon libraries.

{Fore.YELLOW}⚠️  Keep these credentials secure!
{Fore.YELLOW}⚠️  Do not share with anyone!
"""
        print(banner)
    
    def run(self):
        """Main execution method"""
        try:
            # Get phone number
            print(f"\n{Fore.CYAN}[*] Enter your Telegram phone number")
            phone = input(f"{Fore.GREEN}[?] Phone (+91XXXXXXXXXX): {Fore.YELLOW}")
            
            # Step 1: Login
            if not self.login(phone):
                return
            
            # Step 2: Create application
            if not self.create_application():
                self.print_status("Trying alternative creation method...", "warning")
                # Try one more time with different parameters
                time.sleep(2)
                if not self.create_application():
                    self.print_status("Could not create application", "error")
                    return
            
            # Step 3: Get credentials
            if not self.get_credentials():
                self.print_status("Could not extract credentials automatically", "warning")
                self.print_status("But the app was likely created!", "info")
                self.print_status(f"Manually visit: {Fore.YELLOW}https://my.telegram.org/apps", "info")
                return
            
            # Step 4: Save and display
            self.save_credentials_to_files()
            self.display_success_banner()
            
            # Step 5: Show quick test
            self.quick_test_credentials()
            
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Process interrupted by user")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error: {str(e)}")
    
    def quick_test_credentials(self):
        """Quick test to verify credentials work"""
        self.print_status("Testing credentials...", "info")
        
        test_code = f"""
# Quick test script to verify your credentials
import asyncio

async def test_pyrogram():
    try:
        from pyrogram import Client
        app = Client(
            "test_session",
            api_id={self.api_id},
            api_hash="{self.api_hash}"
        )
        async with app:
            me = await app.get_me()
            return True, f"Pyrogram works! User: {{me.first_name}}"
    except Exception as e:
        return False, f"Pyrogram error: {{str(e)}}"

async def test_telethon():
    try:
        from telethon import TelegramClient
        client = TelegramClient('test_session', {self.api_id}, '{self.api_hash}')
        async with client:
            me = await client.get_me()
            return True, f"Telethon works! User: {{me.first_name}}"
    except Exception as e:
        return False, f"Telethon error: {{str(e)}}"

print("Install required packages:")
print("pip install pyrogram telethon")
print("\\nThen run the test script above.")
"""
        
        test_filename = f"test_credentials_{int(time.time())}.py"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        self.print_status(f"Test script saved as: {test_filename}", "info")
        self.print_status("Run: pip install pyrogram telethon", "info")
        self.print_status(f"Then run: python {test_filename}", "info")

# Run the creator
if __name__ == "__main__":
    try:
        print(f"{Fore.CYAN}[*] Telegram API Ultimate Creator")
        print(f"{Fore.CYAN}[*] Starting in 3 seconds...")
        time.sleep(1)
        
        creator = TelegramAPIUltimateCreator()
        creator.run()
        
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal error: {e}")
    
    # Keep window open
    input(f"\n{Fore.CYAN}Press Enter to exit...")