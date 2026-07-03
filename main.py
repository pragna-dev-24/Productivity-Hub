
"""
Productivity Hub
=================
A terminal-based productivity suite with:
  1. Task Manager
  2. Notes
  3. Daily Planner
  4. Expense Tracker
  5. Password Vault (encrypted)
  6. Dashboard
"""

from modules import task_manager, notes, planner, expenses, vault, dashboard
import modules.utils as utils

print(utils)
print(utils.__file__)
print(dir(utils))

def main_menu():
    while True:
        dashboard.show()
        print("\nMAIN MENU")
        print("1. Task Manager")
        print("2. Notes")
        print("3. Daily Planner")
        print("4. Expense Tracker")
        print("5. Password Vault")
        print("6. Refresh Dashboard")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            task_manager.menu()
        elif choice == "2":
            notes.menu()
        elif choice == "3":
            planner.menu()
        elif choice == "4":
            expenses.menu()
        elif choice == "5":
            vault.menu()
        elif choice == "6":
            continue
        elif choice == "0":
            print("\nGoodbye! Stay productive.")
            break
        else:
            print("Invalid choice.")
            utils.pause()


if __name__ == "__main__":
    utils.ensure_data_dir()
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExited. See you next time!")