import requests
from urllib.parse import urljoin
import os


def load_usernames(path):
    try:
        with open(path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as error:
        print(f"[!] Failed to load wordlist: {error}")
        return []


def login(base_url, username, password):
    login_url = urljoin(base_url, '/login')
    data = {'username': username, 'password': password}

    session = requests.Session()
    try:
        response = session.post(login_url, data=data, timeout=5)
    except requests.RequestException as error:
        print(f"[!] Error during login: {error}")
        return None, None

    if response.status_code == 200 and "login" not in response.text.lower():
        print(f"[+] Logged in as '{username}'")
        return session, response.url
    else:
        print(f"[-] Login failed for '{username}'")
        return None, None


def test_profile_access(session, base_url, target_user):
    if not target_user:
        return

    profile_url = urljoin(base_url + '/', target_user)

    try:
        response = session.get(profile_url, timeout=5)
    except requests.RequestException as error:
        print(f"[!] Error accessing '{target_user}': {error}")
        return

    if response.status_code == 200:
        print(f"[!] POSSIBLE BAC: Access to '{target_user}' profile is allowed!")
    elif response.status_code == 403:
        print(f"[+] Access to '{target_user}' is correctly denied (403).")
    elif response.status_code == 404:
        print(f"[-] Profile '{target_user}' not found (404).")
    else:
        print(f"[?] Unexpected response for '{target_user}': {response.status_code}")


def check_bac(base_url, valid_user, valid_pass, target_users):
    session, redirected_url = login(base_url, valid_user, valid_pass)
    if not session:
        print("[x] Cannot continue without a valid session.")
        return

    test_base_url = redirected_url.rsplit('/', 1)[0]

    print("\n[~] Starting BAC test on user profiles...\n")
    for target_user in target_users:
        test_profile_access(session, test_base_url, target_user)


# === Example usage ===

# Set correct path to your usernames file
base_path = os.path.dirname(__file__)
wordlist_path = os.path.join(base_path, '../lists/Usernames.txt')

target_users = load_usernames(wordlist_path)

# Replace with your actual values
url = 'http://localhost:5000'
valid_username = 'user1'
valid_password = 'password1'

check_bac(url, valid_username, valid_password, target_users)
