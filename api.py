__CHANNEL__ = 'Telegram : @esfelurm'

import requests
import json
import time
import random
import string
from colorama import Fore, init
import sys

init()

print(f"""{Fore.CYAN}
╔══════════════════════════════════════════════════╗
║    TELEGRAM API AUTO-CREATOR - POWER MODE        ║
║    100% PowerShell - No Browser                  ║
║    Telegram: @esfelurm                           ║
╚══════════════════════════════════════════════════╝\n
""")

class TelegramAPIForceCreator:
    def __init__(self):
        self.session = requests.Session()
        self.setup_realistic_headers()
        
    def setup_realistic_headers(self):
        """Setup headers to look like real Telegram app"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
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
        })
    
    def get_random_user_agent(self):
        """Get random realistic user agent"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        return random.choice(agents)
    
    def generate_random_string(self, length=8):
        """Generate random string for app names"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    def login(self, phone):
        """Login and return session"""
        print(f"{Fore.YELLOW}[1] Requesting login code...")
        
        try:
            # First, get the main page to set cookies
            self.session.get('https://my.telegram.org', timeout=10)
            
            # Send phone
            response = self.session.post(
                'https://my.telegram.org/auth/send_password',
                data={'phone': phone},
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"{Fore.RED}[!] Failed to send code: {response.status_code}")
                return False
            
            data = response.json()
            if 'random_hash' not in data:
                print(f"{Fore.RED}[!] No hash in response")
                return False
            
            random_hash = data['random_hash']
            print(f"{Fore.GREEN}[✓] Code sent to Telegram!")
            
            # Get code
            code = input(f"{Fore.CYAN}[?] Enter Telegram code: {Fore.YELLOW}")
            
            # Login with code
            print(f"{Fore.YELLOW}[2] Logging in...")
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
                print(f"{Fore.GREEN}[✓] Login successful!")
                return True
            else:
                print(f"{Fore.RED}[!] Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[!] Login error: {e}")
            return False
    
    def direct_api_create_app(self):
        """Direct API method to create app - Bypasses web interface"""
        print(f"{Fore.YELLOW}[3] Using direct API method...")
        
        # First, we need to get the user's config
        try:
            # Get user config (this often triggers app creation)
            config_url = "https://my.telegram.org/apps/api"
            response = self.session.get(config_url, timeout=15)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[✓] Got API endpoint")
                return self.parse_api_response(response.text)
            
            # If that doesn't work, try the web API
            return self.web_api_create_app()
            
        except Exception as e:
            print(f"{Fore.RED}[!] API method failed: {e}")
            return self.web_api_create_app()
    
    def web_api_create_app(self):
        """Web API method for app creation"""
        print(f"{Fore.YELLOW}[4] Using web API method...")
        
        # Generate random names
        random_suffix = self.generate_random_string(6)
        app_title = f"Telegram{random_suffix}"
        app_shortname = f"tg{random_suffix}"
        
        # Prepare app data
        app_data = {
            'app_title': app_title,
            'app_shortname': app_shortname,
            'app_url': '',
            'app_platform': 'desktop',
            'app_desc': f'Telegram Desktop Client {random_suffix}',
            'hash': self.get_form_hash()
        }
        
        print(f"{Fore.CYAN}[*] Creating app: {app_title} ({app_shortname})")
        
        try:
            # Submit creation
            response = self.session.post(
                'https://my.telegram.org/apps/create',
                data=app_data,
                timeout=20
            )
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[✓] App creation submitted via web!")
                time.sleep(2)
                
                # Now try to get the credentials
                return self.get_credentials_from_apps()
            else:
                print(f"{Fore.RED}[!] Web API failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[!] Web API error: {e}")
            return None
    
    def get_form_hash(self):
        """Get form hash from create page"""
        try:
            response = self.session.get('https://my.telegram.org/apps/create', timeout=10)
            
            # Look for hash in the page
            import re
            hash_match = re.search(r'name=["\']hash["\']\s+value=["\']([^"\']+)["\']', response.text)
            if hash_match:
                return hash_match.group(1)
            
            # Alternative pattern
            hash_match = re.search(r'hash["\']?\s*[:=]\s*["\']([^"\']+)["\']', response.text)
            if hash_match:
                return hash_match.group(1)
            
            return "dummy_hash"
            
        except:
            return "dummy_hash"
    
    def get_credentials_from_apps(self):
        """Get credentials from apps page"""
        print(f"{Fore.YELLOW}[5] Extracting credentials...")
        
        try:
            # Get apps page
            response = self.session.get('https://my.telegram.org/apps', timeout=15)
            page_content = response.text
            
            # Try multiple extraction methods
            credentials = self.brute_force_extract(page_content)
            
            if credentials:
                return credentials
            
            # If still not found, try the raw API endpoint
            return self.try_raw_api_endpoint()
            
        except Exception as e:
            print(f"{Fore.RED}[!] Extraction error: {e}")
            return None
    
    def brute_force_extract(self, html):
        """Brute force extract credentials from HTML"""
        import re
        
        # Try multiple patterns
        patterns = [
            # Pattern 1: JSON-like
            (r'"api_id"\s*:\s*"?(\d{5,9})"?', 'api_id'),
            (r'"api_hash"\s*:\s*"?([a-f0-9]{32})"?', 'api_hash'),
            
            # Pattern 2: HTML text
            (r'>\s*(\d{5,9})\s*<', 'api_id'),
            (r'>\s*([a-f0-9]{32})\s*<', 'api_hash'),
            
            # Pattern 3: In form values
            (r'value=["\'](\d{5,9})["\']', 'api_id'),
            (r'value=["\']([a-f0-9]{32})["\']', 'api_hash'),
            
            # Pattern 4: In script tags
            (r'api_id\s*=\s*["\']?(\d{5,9})["\']?', 'api_id'),
            (r'api_hash\s*=\s*["\']?([a-f0-9]{32})["\']?', 'api_hash'),
            
            # Pattern 5: Any numbers/hex in certain contexts
            (r'App api_id[^<]*<[^>]*>([^<]+)', 'api_id'),
            (r'App api_hash[^<]*<[^>]*>([^<]+)', 'api_hash'),
        ]
        
        api_id = None
        api_hash = None
        
        for pattern, field in patterns:
            matches = re.findall(pattern, html, re.I)
            for match in matches:
                if field == 'api_id' and not api_id:
                    if str(match).isdigit() and 10000 <= int(match) <= 999999999:
                        api_id = match
                elif field == 'api_hash' and not api_hash:
                    if re.match(r'^[a-f0-9]{32}$', str(match), re.I):
                        api_hash = match
            
            if api_id and api_hash:
                break
        
        if api_id and api_hash:
            return {'api_id': api_id, 'api_hash': api_hash}
        
        return None
    
    def try_raw_api_endpoint(self):
        """Try raw API endpoints that might exist"""
        print(f"{Fore.YELLOW}[6] Trying raw API endpoints...")
        
        endpoints = [
            'https://my.telegram.org/apps/api',
            'https://my.telegram.org/api/v1/apps',
            'https://my.telegram.org/api/apps',
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(endpoint, timeout=10)
                if response.status_code == 200:
                    # Try to parse as JSON
                    try:
                        data = response.json()
                        if 'api_id' in data and 'api_hash' in data:
                            print(f"{Fore.GREEN}[✓] Found in API endpoint!")
                            return data
                    except:
                        pass
            except:
                continue
        
        return None
    
    def create_app_telegram_api(self):
        """Alternative: Use Telegram's own API if web fails"""
        print(f"{Fore.YELLOW}[7] Using Telegram Core API...")
        
        # This is a more direct approach
        try:
            # Get the current user's app list
            apps_response = self.session.get('https://my.telegram.org/apps/list', timeout=15)
            
            if apps_response.status_code == 200:
                # Try to parse response
                import re
                
                # Look for create app endpoint
                create_pattern = r'/apps/create/[^"\']+'
                matches = re.findall(create_pattern, apps_response.text)
                
                if matches:
                    create_url = f"https://my.telegram.org{matches[0]}"
                    
                    # Try to create app via this URL
                    response = self.session.post(create_url, timeout=20)
                    
                    if response.status_code == 200:
                        print(f"{Fore.GREEN}[✓] App created via direct endpoint!")
                        return self.get_credentials_from_apps()
            
            return None
            
        except Exception as e:
            print(f"{Fore.RED}[!] Telegram API error: {e}")
            return None
    
    def run_full_creation(self, phone):
        """Run the full creation process"""
        print(f"{Fore.CYAN}[*] Starting FULL auto-creation process...")
        
        # Step 1: Login
        if not self.login(phone):
            return
        
        # Step 2: Try multiple creation methods
        methods = [
            self.direct_api_create_app,
            self.web_api_create_app,
            self.create_app_telegram_api,
        ]
        
        credentials = None
        
        for method in methods:
            if credentials:
                break
                
            print(f"{Fore.YELLOW}[*] Trying method: {method.__name__}...")
            credentials = method()
            
            if credentials and 'api_id' in credentials and 'api_hash' in credentials:
                if credentials['api_id'] and credentials['api_hash']:
                    break
        
        # Final check
        if credentials and credentials.get('api_id') and credentials.get('api_hash'):
            self.show_results(phone, credentials['api_id'], credentials['api_hash'])
        else:
            print(f"{Fore.RED}[!] ALL auto-methods failed!")
            print(f"{Fore.YELLOW}[*] But you're logged in! Trying ONE LAST METHOD...")
            self.last_resort_method(phone)
    
    def last_resort_method(self, phone):
        """Last resort: Create app using simulated browser"""
        print(f"{Fore.YELLOW}[*] Using simulated browser method...")
        
        try:
            # This simulates a full browser session
            import re
            
            # Get the create form with all details
            response = self.session.get('https://my.telegram.org/apps', timeout=15)
            
            # Check if we're on the right page
            if 'app_creation' in response.text or 'Create application' in response.text:
                # Extract all form fields
                form_fields = self.extract_all_form_fields(response.text)
                
                if form_fields:
                    print(f"{Fore.GREEN}[✓] Got form fields, submitting...")
                    
                    # Submit with all fields
                    submit_response = self.session.post(
                        'https://my.telegram.org/apps/create',
                        data=form_fields,
                        timeout=20
                    )
                    
                    if submit_response.status_code == 200:
                        print(f"{Fore.GREEN}[✓] Form submitted!")
                        
                        # Try to extract one more time
                        final_response = self.session.get('https://my.telegram.org/apps', timeout=15)
                        credentials = self.brute_force_extract(final_response.text)
                        
                        if credentials:
                            self.show_results(phone, credentials['api_id'], credentials['api_hash'])
                            return
            
            print(f"{Fore.RED}[!] Even last method failed.")
            print(f"{Fore.CYAN}[*] However, you ARE logged in to: https://my.telegram.org")
            print(f"{Fore.CYAN}[*] Session cookies are active.")
            print(f"{Fore.YELLOW}[*] To get API manually, run this PowerShell command:")
            print(f"{Fore.WHITE}" + "="*60)
            print(f"""
# Get your session cookies:
$cookies = @{{""")
            
            # Show cookies
            for cookie in self.session.cookies:
                print(f"    '{cookie.name}' = '{cookie.value}'")
            
            print(f"""}}

# Then visit https://my.telegram.org/apps in browser
# Or use: Invoke-WebRequest with these cookies""")
            print(f"{Fore.WHITE}" + "="*60)
            
        except Exception as e:
            print(f"{Fore.RED}[!] Last method error: {e}")
    
    def extract_all_form_fields(self, html):
        """Extract all form fields from HTML"""
        import re
        
        fields = {}
        
        # Extract all input fields
        input_pattern = r'<input[^>]+name=["\']([^"\']+)["\'][^>]+value=["\']([^"\']*)["\']'
        matches = re.findall(input_pattern, html, re.I)
        
        for name, value in matches:
            fields[name] = value
        
        # Add our app data
        random_suffix = self.generate_random_string(4)
        fields.update({
            'app_title': f'TelegramDesktop{random_suffix}',
            'app_shortname': f'tg{random_suffix}',
            'app_url': 'https://desktop.telegram.org',
            'app_platform': 'desktop',
            'app_desc': 'Official Telegram Desktop',
        })
        
        return fields
    
    def show_results(self, phone, api_id, api_hash):
        """Show successful results"""
        print(f"\n{Fore.GREEN}" + "="*60)
        print(f"{Fore.CYAN}    SUCCESS! API CREDENTIALS CREATED")
        print(f"{Fore.GREEN}" + "="*60)
        print(f"{Fore.YELLOW}Phone: {Fore.WHITE}{phone}")
        print(f"{Fore.YELLOW}API ID: {Fore.WHITE}{api_id}")
        print(f"{Fore.YELLOW}API Hash: {Fore.WHITE}{api_hash}")
        print(f"{Fore.GREEN}" + "="*60)
        
        # Save to multiple formats
        self.save_credentials(phone, api_id, api_hash)
        
        # Show usage examples
        self.show_usage_examples(api_id, api_hash, phone)
    
    def save_credentials(self, phone, api_id, api_hash):
        """Save credentials to files"""
        import os
        
        # Clean phone for filename
        clean_phone = phone.replace('+', '').replace(' ', '')
        
        # Save as text
        txt_content = f"""TELEGRAM API CREDENTIALS
=======================
Phone: {phone}
API ID: {api_id}
API Hash: {api_hash}
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
By: @esfelurm
"""
        
        with open(f"api_{clean_phone}.txt", "w") as f:
            f.write(txt_content)
        
        # Save as JSON
        json_content = {
            "phone": phone,
            "api_id": int(api_id),
            "api_hash": api_hash,
            "app_title": "Telegram Desktop",
            "app_platform": "desktop",
            "generated": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(f"api_{clean_phone}.json", "w") as f:
            json.dump(json_content, f, indent=2)
        
        # Save as Python config
        py_content = f"""# Telegram API Configuration
API_ID = {api_id}
API_HASH = "{api_hash}"
PHONE = "{phone}"

# Pyrogram
from pyrogram import Client
app = Client("my_account", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE)

# Telethon
from telethon import TelegramClient
client = TelegramClient('session', API_ID, API_HASH)
"""
        
        with open(f"api_{clean_phone}.py", "w") as f:
            f.write(py_content)
        
        print(f"{Fore.CYAN}[✓] Saved credentials to:")
        print(f"{Fore.YELLOW}    - api_{clean_phone}.txt")
        print(f"{Fore.YELLOW}    - api_{clean_phone}.json")
        print(f"{Fore.YELLOW}    - api_{clean_phone}.py")
    
    def show_usage_examples(self, api_id, api_hash, phone):
        """Show usage examples"""
        print(f"\n{Fore.CYAN}[*] Usage Examples:")
        print(f"{Fore.YELLOW}" + "-"*40)
        
        print(f"{Fore.GREEN}Pyrogram:")
        print(f"{Fore.WHITE}from pyrogram import Client")
        print(f"app = Client(")
        print(f"    'my_account',")
        print(f"    api_id={api_id},")
        print(f"    api_hash='{api_hash}',")
        print(f"    phone_number='{phone}'")
        print(f")")
        
        print(f"\n{Fore.GREEN}Telethon:")
        print(f"{Fore.WHITE}from telethon import TelegramClient")
        print(f"client = TelegramClient(")
        print(f"    'session',")
        print(f"    {api_id},")
        print(f"    '{api_hash}'")
        print(f")")

# Main execution
if __name__ == "__main__":
    try:
        creator = TelegramAPIForceCreator()
        
        print(f"{Fore.CYAN}[*] This script will:")
        print(f"{Fore.YELLOW}    1. Login to your Telegram account")
        print(f"{Fore.YELLOW}    2. Automatically create app")
        print(f"{Fore.YELLOW}    3. Extract API ID & Hash")
        print(f"{Fore.YELLOW}    4. Save to files")
        print()
        
        phone = input(f"{Fore.GREEN}[?] Enter phone (+91XXXXXXXXXX): {Fore.YELLOW}")
        
        creator.run_full_creation(phone)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupted by user")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {e}")
    
    input(f"\n{Fore.CYAN}Press Enter to exit...")