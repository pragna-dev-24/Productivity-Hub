import json
import os
import uuid
from datetime import datetime


# Base data directory (created next to main.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def ensure_data_dir():
    """Make sure the data folder exists before any read/write."""
    os.makedirs(DATA_DIR, exist_ok=True)

def data_path(filename):
    ensure_data_dir()
    return os.path.join(DATA_DIR, filename)


def load_json(filename, default):
    """Load a JSON file from the data folder, returning `default` if missing/corrupt."""
    path = data_path(filename)
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filename, data):
    """Save data as JSON into the data folder."""
    path = data_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def new_id():
    """Short unique id for records (tasks, notes, expenses, etc.)."""
    return uuid.uuid4().hex[:8]


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


# ---------- Terminal UI helpers ----------

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    width = 60
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_divider():
    print("-" * 60)


def get_nonempty_input(prompt):
    """Keep asking until the user provides a non-blank value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_valid_date(prompt, allow_blank=False):
    """Ask for a date in YYYY-MM-DD format, validating it."""
    while True:
        value = input(prompt).strip()
        if allow_blank and not value:
            return ""
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD (e.g. 2026-07-15).")


def get_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def get_choice(prompt, valid_choices):
    """Ask until the user enters one of the valid_choices (case-insensitive)."""
    valid_lower = [c.lower() for c in valid_choices]
    while True:
        value = input(prompt).strip()
        if value.lower() in valid_lower:
            return value.lower()
        print(f"Please choose one of: {', '.join(valid_choices)}")
