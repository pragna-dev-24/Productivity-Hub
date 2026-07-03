from modules import utils, task_manager, notes, planner, expenses, vault

FILENAME = "tasks.json"
PRIORITIES = ["low", "medium", "high"]


def load_tasks():
    return utils.load_json(FILENAME, [])


def save_tasks(tasks):
    utils.save_json(FILENAME, tasks)


def add_task():
    utils.print_header("Add New Task")
    title = utils.get_nonempty_input("Task title: ")
    description = input("Description (optional): ").strip()
    priority = utils.get_choice(
        f"Priority ({'/'.join(PRIORITIES)}): ", PRIORITIES
    )
    due_date = utils.get_valid_date(
        "Due date (YYYY-MM-DD, blank for none): ", allow_blank=True
    )

    tasks = load_tasks()
    task = {
        "id": utils.new_id(),
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "status": "pending",
        "created_at": utils.now_str(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"\nTask added successfully! (ID: {task['id']})")


def _sort_key(task):
    priority_rank = {"high": 0, "medium": 1, "low": 2}
    return (
        task["status"] != "pending",
        priority_rank.get(task["priority"], 3),
        task["due_date"] or "9999-99-99",
    )


def list_tasks(filter_status=None, silent=False):
    tasks = load_tasks()
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    tasks = sorted(tasks, key=_sort_key)

    if not silent:
        utils.print_header("Your Tasks")
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                status_icon = "[x]" if t["status"] == "completed" else "[ ]"
                due = f" | due {t['due_date']}" if t["due_date"] else ""
                print(f"{status_icon} {t['title']}  ({t['priority']}){due}  [id:{t['id']}]")
                if t["description"]:
                    print(f"      {t['description']}")
    return tasks


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def complete_task():
    tasks = list_tasks(filter_status="pending")
    if not tasks:
        utils.pause()
        return
    task_id = input("\nEnter task ID to mark complete: ").strip()
    task = find_task(load_tasks(), task_id)
    if not task:
        print("Task not found.")
    else:
        all_tasks = load_tasks()
        for t in all_tasks:
            if t["id"] == task_id:
                t["status"] = "completed"
        save_tasks(all_tasks)
        print(f"Task '{task['title']}' marked as completed!")
    utils.pause()


def edit_task():
    tasks = list_tasks()
    if not tasks:
        utils.pause()
        return
    task_id = input("\nEnter task ID to edit: ").strip()
    all_tasks = load_tasks()
    task = find_task(all_tasks, task_id)
    if not task:
        print("Task not found.")
        utils.pause()
        return

    print("Leave a field blank to keep it unchanged.")
    new_title = input(f"New title [{task['title']}]: ").strip()
    new_desc = input(f"New description [{task['description']}]: ").strip()
    new_priority = input(f"New priority [{task['priority']}]: ").strip().lower()
    new_due = input(f"New due date [{task['due_date']}]: ").strip()

    if new_title:
        task["title"] = new_title
    if new_desc:
        task["description"] = new_desc
    if new_priority in PRIORITIES:
        task["priority"] = new_priority
    if new_due:
        task["due_date"] = new_due

    save_tasks(all_tasks)
    print("Task updated.")
    utils.pause()


def delete_task():
    tasks = list_tasks()
    if not tasks:
        utils.pause()
        return
    task_id = input("\nEnter task ID to delete: ").strip()
    all_tasks = load_tasks()
    task = find_task(all_tasks, task_id)
    if not task:
        print("Task not found.")
    else:
        all_tasks = [t for t in all_tasks if t["id"] != task_id]
        save_tasks(all_tasks)
        print(f"Task '{task['title']}' deleted.")
    utils.pause()


def get_summary():
    tasks = load_tasks()
    pending = [t for t in tasks if t["status"] == "pending"]
    completed = [t for t in tasks if t["status"] == "completed"]
    overdue = [
        t for t in pending
        if t["due_date"] and t["due_date"] < utils.today_str()
    ]
    return {
        "total": len(tasks),
        "pending": len(pending),
        "completed": len(completed),
        "overdue": len(overdue),
    }


def menu():
    while True:
        utils.clear_screen()
        utils.print_header("TASK MANAGER")
        print("1. Add task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. Mark task as complete")
        print("5. Edit task")
        print("6. Delete task")
        print("0. Back to Dashboard")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_task()
            utils.pause()
        elif choice == "2":
            list_tasks()
            utils.pause()
        elif choice == "3":
            list_tasks(filter_status="pending")
            utils.pause()
        elif choice == "4":
            complete_task()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            delete_task()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            utils.pause()
