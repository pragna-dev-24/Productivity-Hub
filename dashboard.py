from modules import utils, task_manager, notes, planner, expenses, vault


def show():
    utils.clear_screen()
    utils.print_header("PRODUCTIVITY HUB - DASHBOARD")

    t = task_manager.get_summary()
    print(f"\nTASKS")
    print(f"   Pending: {t['pending']}  |  Completed: {t['completed']}  |  Overdue: {t['overdue']}")

    n = notes.get_summary()
    print(f"\nNOTES")
    print(f"   Total notes saved: {n['total']}")

    p = planner.get_today_summary()
    print(f"\nTODAY'S PLAN ({p['date']})")
    print(f"   {p['done']}/{p['total']} activities done today")

    e = expenses.get_summary()
    print(f"\nEXPENSES")
    print(f"   This month: {e['month_total']:.2f}  |  All-time: {e['total']:.2f}  ({e['count']} entries)")

    v = vault.get_summary()
    print(f"\nPASSWORD VAULT")
    if v["exists"]:
        print("   Vault is set up. Open it to view/manage entries securely.")
    else:
        print("   No vault created yet. Open it to set a master password.")

    utils.print_divider()
