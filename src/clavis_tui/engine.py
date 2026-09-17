import base64
import configparser
import json
import os
import sys
from datetime import datetime
from difflib import SequenceMatcher

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_FILE = os.path.join(SCRIPT_DIR, sys.argv[1] if len(sys.argv) > 1 else "vault.json")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "clavis.conf")
ph = PasswordHasher()

def save_theme(theme: str) -> None:
    config = configparser.ConfigParser()
    config["settings"] = {"theme": theme}
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

def load_theme() -> str:
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config["settings"].get("theme", "tokyo-night")
    return "tokyo-night"


#vault creation
def vault_exists():
    return os.path.exists(VAULT_FILE)
    

def create_vault(password):
    password_hash = ph.hash(password)
    salt = os.urandom(16)

    vault_data = {
        "password_hash": password_hash,
        "salt": base64.b64encode(salt).decode(),
        "entries": []
    }

    with open(VAULT_FILE, "w") as f:
        json.dump(vault_data, f)


#password hashing
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


#authentication process
def unlock_vault(password):
    with open(VAULT_FILE, "r") as f:
        vault_data = json.load(f)

    ph.verify(vault_data["password_hash"], password)

    salt = base64.b64decode(vault_data["salt"])
    key = derive_key(password, salt)
    return key, vault_data


#vault saving variable
def save_vault(vault_data):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault_data, f)


#creating/adding entry
def add_entry(fernet, vault_data, entry_type, title, topic, content):
    entry_date = datetime.now().astimezone().date().isoformat()

    encrypted_title = fernet.encrypt(title.encode())
    encrypted_topic = fernet.encrypt(topic.encode())
    encrypted_date = fernet.encrypt(entry_date.encode())
    encrypted_content = fernet.encrypt(content.encode())

    entry = {
        "type": entry_type,
        "title": encrypted_title.decode(),
        "date": encrypted_date.decode(),
        "topic": encrypted_topic.decode(),
        "content": encrypted_content.decode()
    }

    vault_data["entries"].append(entry)
    save_vault(vault_data)


#Search Helper Function
MATCH_CUTOFF = 0.6

def fuzzy_score(term, text):
    term = term.lower()
    text = text.lower()

    if term in text:
        return 1.0

    best = 0
    for word in text.split():
        ratio = SequenceMatcher(None, term, word).ratio()
        if ratio > best:
            best = max(best, ratio)
    return best


#Search Entry Feature
def search_entries(fernet, vault_data, keyword=None, title=None, date=None, topic=None):
    matches = []
    for entry in vault_data["entries"]:
        decrypted_title = fernet.decrypt(entry["title"].encode()).decode()
        decrypted_date = fernet.decrypt(entry["date"].encode()).decode()
        decrypted_topic = fernet.decrypt(entry["topic"].encode()).decode()
        decrypted_content = fernet.decrypt(entry["content"].encode()).decode()

        score = 0

        if keyword:
            keyword_score = max(
                fuzzy_score(keyword, decrypted_content),
                fuzzy_score(keyword, decrypted_title)
            )
            if keyword_score >= MATCH_CUTOFF:
                score += keyword_score

        if title:
            title_score = fuzzy_score(title, decrypted_title)
            if title_score >= MATCH_CUTOFF:
                score += title_score

        if date and date in decrypted_date:
            score += 1

        if topic:
            topic_score = fuzzy_score(topic, decrypted_topic)
            if topic_score >= MATCH_CUTOFF:
                score += topic_score

        if score > 0:
            matches.append((score, {
                "type": entry["type"],
                "title": decrypted_title,
                "date": decrypted_date,
                "topic": decrypted_topic,
                "content": decrypted_content
            }))

    matches.sort(key=lambda pair: pair[0], reverse=True)
    return [entry for score, entry in matches]

    