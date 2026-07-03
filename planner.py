from modules import utils

FILENAME = "planner.json"


def load_plans():
    return utils.load_json(FILENAME, {})


def save_plans(plans):
    utils.save_json(FILENAME, plans)


def _pick_date(prompt="Date (YYYY-MM-DD, blank = today): "):
    date = utils.get_valid_date(prompt, allow_blank=True)
    return date or utils.today_str()


def add_entry():
    utils.print_header("Add Planner Entry")
    date = _pick_date()
    time = input("Time (e.g. 09:00, or 'anytime'): ").strip() or "anytime"
    activity = utils.get_nonempty_input("Activity: ")

    plans = load_plans()
    plans.setdefault(date, [])
    plans[date].append({"time": time, "activity": activity, "done": False})
    plans[date].sort(key=lambda e: e["time"])
    save_plans(plans)
    print(f"\nAdded to your plan for {date}.")


def view_day(date=None, silent=False):
    if date is None:
        date = _pick_date("View which date? (YYYY-MM-DD, blank = today): ")
    plans = load_plans()
    entries = plans.get(date, [])

    if not silent:
        utils.print_header(f"Plan for {date}")
        if not entries:
            print("Nothing planned for this day.")
        else:
            for i, e in enumerate(entries, start=1):
                mark = "[x]" if e["done"] else "[ ]"
                print(f"{i}. {mark} {e['time']} - {e['activity']}")
    return date, entries


def mark_done():
    date, entries = view_day()
    if not entries:
        utils.pause()
        return
    idx = input("\nEntry number to mark done: ").strip()
    if idx.isdigit() and 1 <= int(idx) <= len(entries):
        plans = load_plans()
        plans[date][int(idx) - 1]["done"] = True
        save_plans(plans)
        print("Marked as done!")
    else:
        print("Invalid entry number.")
    utils.pause()


def delete_entry():
    date, entries = view_day()
    if not entries:
        utils.pause()
        return
    idx = input("\nEntry number to delete: ").strip()
    if idx.isdigit() and 1 <= int(idx) <= len(entries):
        plans = load_plans()
        removed = plans[date].pop(int(idx) - 1)
        save_plans(plans)
        print(f"Removed: {removed['activity']}")
    else:
        print("Invalid entry number.")
    utils.pause()


def get_today_summary():
    date = utils.today_str()
    plans = load_plans()
    entries = plans.get(date, [])
    done = sum(1 for e in entries if e["done"])
    return {"date": date, "total": len(entries), "done": done}


def menu():
    while True:
        utils.clear_screen()
        utils.print_header("DAILY PLANNER")
        print("1. Add entry to a day")
        print("2. View a day&apos;s plan")
        print("3. Mark entry as done")
        print("4. Delete entry")
        print("0. Back to Dashboard")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_entry()
            utils.pause()
        elif choice == "2":
            view_day()
            utils.pause()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_entry()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            utils.pause()
