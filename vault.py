"""
vault.py - Encrypted password vault.

Security design:
- A master password unlocks the vault (never stored directly).
- A random salt + PBKDF2-HMAC-SHA256 derives an encryption key from the master password.
- All entries are encrypted with Fernet (AES-128-CBC + HMAC) before being written to disk.
- Only a salt and a verification hash are stored in plaintext in vault.json;
  the actual entries are stored encrypted.
"""

import base64
import os
import secrets
import string

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from modules import utils

FILENAME = "vault.json"
PBKDF2_ITERATIONS = 390_000


def _load_raw():
    return utils.load_json(FILENAME, None)


def _save_raw(data):
    utils.save_json(FILENAME, data)


def _derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    key = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def vault_exists():
    return _load_raw() is not None


def setup_vault():
    """First-time setup: create a master password and initialize the vault file."""
    utils.print_header("Set Up Password Vault")
    print("This is your first time opening the vault. Create a master password.")
    print("IMPORTANT: If you forget this password, your saved passwords cannot be recovered.\n")

    while True:
        pw1 = input("Create master password: ").strip()
        pw2 = input("Confirm master password: ").strip()
        if not pw1:
            print("Password cannot be empty.")
            continue
        if pw1 != pw2:
            print("Passwords don't match. Try again.")
            continue
        break

    salt = os.urandom(16)
    key = _derive_key(pw1, salt)
    fernet = Fernet(key)

    # Store a verification token we can decrypt later to confirm the password is correct
    verification = fernet.encrypt(b"vault-ok")
    empty_entries = fernet.encrypt(b"[]")

    data = {
        "salt": base64.urlsafe_b64encode(salt).decode("utf-8"),
        "verification": verification.decode("utf-8"),
        "entries": empty_entries.decode("utf-8"),
    }
    _save_raw(data)
    print("\nVault created successfully!")
    return key


def unlock_vault():
    """Prompt for master password and return the derived Fernet key, or None if wrong."""
    data = _load_raw()
    salt = base64.urlsafe_b64decode(data["salt"])
    pw = input("Enter master password: ").strip()
    key = _derive_key(pw, salt)
    fernet = Fernet(key)
    try:
        fernet.decrypt(data["verification"].encode("utf-8"))
        return key
    except InvalidToken:
        return None


def _get_entries(key):
    data = _load_raw()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data["entries"].encode("utf-8"))
    import json
    return json.loads(decrypted.decode("utf-8"))


def _save_entries(key, entries):
    import json
    data = _load_raw()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(entries).encode("utf-8"))
    data["entries"] = encrypted.decode("utf-8")
    _save_raw(data)


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def add_entry(key):
    utils.print_header("Add Password Entry")
    site = utils.get_nonempty_input("Site / App name: ")
    username = input("Username / Email: ").strip()

    use_gen = input("Generate a strong random password? (y/n): ").strip().lower()
    if use_gen == "y":
        password = generate_password()
        print(f"Generated password: {password}")
    else:
        password = utils.get_nonempty_input("Password: ")

    notes = input("Notes (optional): ").strip()

    entries = _get_entries(key)
    entries.append({
        "id": utils.new_id(),
        "site": site,
        "username": username,
        "password": password,
        "notes": notes,
        "created_at": utils.now_str(),
    })
    _save_entries(key, entries)
    print(f"\nEntry for '{site}' saved securely.")


def list_entries(key):
    entries = _get_entries(key)
    utils.print_header("Vault Entries")
    if not entries:
        print("No entries saved yet.")
    else:
        for e in entries:
            print(f"- {e['site']}  (user: {e['username'] or 'n/a'})  [id:{e['id']}]")
    return entries


def view_entry(key):
    entries = list_entries(key)
    if not entries:
        utils.pause()
        return
    entry_id = input("\nEnter entry ID to reveal password: ").strip()
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        print("Entry not found.")
    else:
        utils.print_header(entry["site"])
        print(f"Username: {entry['username']}")
        print(f"Password: {entry['password']}")
        if entry["notes"]:
            print(f"Notes: {entry['notes']}")
    utils.pause()


def delete_entry(key):
    entries = list_entries(key)
    if not entries:
        utils.pause()
        return
    entry_id = input("\nEnter entry ID to delete: ").strip()
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        print("Entry not found.")
    else:
        entries = [e for e in entries if e["id"] != entry_id]
        _save_entries(key, entries)
        print(f"Entry for '{entry['site']}' deleted.")
    utils.pause()


def get_summary():
    """Non-sensitive summary for the dashboard: doesn't require unlocking."""
    if not vault_exists():
        return {"exists": False, "count": None}
    return {"exists": True, "count": None}  # count hidden until unlocked, by design


def menu():
    utils.clear_screen()
    utils.print_header("PASSWORD VAULT")

    if not vault_exists():
        key = setup_vault()
        utils.pause()
    else:
        attempts = 0
        key = None
        while attempts < 3:
            key = unlock_vault()
            if key:
                print("\nVault unlocked!")
                break
            attempts += 1
            print(f"Incorrect password. {3 - attempts} attempt(s) left.")
        if not key:
            print("\nToo many failed attempts. Returning to dashboard.")
            utils.pause()
            return

    while True:
        utils.clear_screen()
        utils.print_header("PASSWORD VAULT (unlocked)")
        print("1. Add entry")
        print("2. View all entries")
        print("3. Reveal a password")
        print("4. Delete entry")
        print("0. Lock & return to Dashboard")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_entry(key)
            utils.pause()
        elif choice == "2":
            list_entries(key)
            utils.pause()
        elif choice == "3":
            view_entry(key)
        elif choice == "4":
            delete_entry(key)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            utils.pause()