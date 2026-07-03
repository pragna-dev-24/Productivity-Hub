from collections import defaultdict
from modules import utils

FILENAME = "expenses.json"
CATEGORIES = ["food", "transport", "bills", "shopping", "entertainment", "health", "other"]


def load_expenses():
    return utils.load_json(FILENAME, [])


def save_expenses(expenses):
    utils.save_json(FILENAME, expenses)


def add_expense():
    utils.print_header("Add Expense")
    amount = utils.get_float("Amount: ")
    category = utils.get_choice(f"Category ({'/'.join(CATEGORIES)}): ", CATEGORIES)
    description = input("Description (optional): ").strip()
    date = utils.get_valid_date("Date (YYYY-MM-DD, blank = today): ", allow_blank=True) or utils.today_str()

    expenses = load_expenses()
    expense = {
        "id": utils.new_id(),
        "amount": amount,
        "category": category,
        "description": description,
        "date": date,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"\nExpense of {amount:.2f} logged under '{category}'.")


def list_expenses(silent=False):
    expenses = sorted(load_expenses(), key=lambda e: e["date"], reverse=True)
    if not silent:
        utils.print_header("All Expenses")
        if not expenses:
            print("No expenses recorded.")
        else:
            for e in expenses:
                desc = f" - {e['description']}" if e["description"] else ""
                print(f"{e['date']} | {e['category']:<13} | {e['amount']:>10.2f}{desc}  [id:{e['id']}]")
            print_divider_total(expenses)
    return expenses


def print_divider_total(expenses):
    utils.print_divider()
    total = sum(e["amount"] for e in expenses)
    print(f"Total: {total:.2f}")


def summary_by_category():
    expenses = load_expenses()
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]

    utils.print_header("Spending by Category")
    if not totals:
        print("No expenses recorded.")
    else:
        for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
            print(f"{cat:<15}: {amt:.2f}")
        print_divider_total(expenses)
    utils.pause()


def monthly_summary():
    month = input("Enter month (YYYY-MM, blank = current): ").strip()
    if not month:
        month = utils.today_str()[:7]
    expenses = [e for e in load_expenses() if e["date"].startswith(month)]

    utils.print_header(f"Summary for {month}")
    if not expenses:
        print("No expenses for this month.")
    else:
        totals = defaultdict(float)
        for e in expenses:
            totals[e["category"]] += e["amount"]
        for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
            print(f"{cat:<15}: {amt:.2f}")
        print_divider_total(expenses)
    utils.pause()


def delete_expense():
    list_expenses()
    exp_id = input("\nEnter expense ID to delete: ").strip()
    expenses = load_expenses()
    exp = next((e for e in expenses if e["id"] == exp_id), None)
    if not exp:
        print("Expense not found.")
    else:
        expenses = [e for e in expenses if e["id"] != exp_id]
        save_expenses(expenses)
        print("Expense deleted.")
    utils.pause()


def get_summary():
    expenses = load_expenses()
    month = utils.today_str()[:7]
    month_total = sum(e["amount"] for e in expenses if e["date"].startswith(month))
    total = sum(e["amount"] for e in expenses)
    return {"total": total, "month_total": month_total, "count": len(expenses)}


def menu():
    while True:
        utils.clear_screen()
        utils.print_header("EXPENSE TRACKER")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Summary by category")
        print("4. Monthly summary")
        print("5. Delete expense")
        print("0. Back to Dashboard")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_expense()
            utils.pause()
        elif choice == "2":
            list_expenses()
            utils.pause()
        elif choice == "3":
            summary_by_category()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            delete_expense()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            utils.pause()
