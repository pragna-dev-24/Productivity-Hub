from modules import utils

FILENAME = "notes.json"


def load_notes():
    return utils.load_json(FILENAME, [])


def save_notes(notes):
    utils.save_json(FILENAME, notes)


def add_note():
    utils.print_header("Add New Note")
    title = utils.get_nonempty_input("Note title: ")
    print("Enter note content (press Enter twice to finish):")
    lines = []
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 1 and lines:
                break
            if empty_count >= 2:
                break
        else:
            empty_count = 0
            lines.append(line)
    content = "\n".join(lines)
    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]

    notes = load_notes()
    note = {
        "id": utils.new_id(),
        "title": title,
        "content": content,
        "tags": tags,
        "created_at": utils.now_str(),
    }
    notes.append(note)
    save_notes(notes)
    print(f"\nNote saved! (ID: {note['id']})")


def list_notes(notes=None, silent=False):
    if notes is None:
        notes = load_notes()
    if not silent:
        utils.print_header("Your Notes")
        if not notes:
            print("No notes found.")
        else:
            for n in notes:
                tags = f" [{', '.join(n['tags'])}]" if n["tags"] else ""
                preview = (n["content"][:40] + "...") if len(n["content"]) > 40 else n["content"]
                print(f"- {n['title']}{tags}  [id:{n['id']}]")
                print(f"    {preview}")
    return notes


def view_note():
    list_notes()
    note_id = input("\nEnter note ID to view in full: ").strip()
    notes = load_notes()
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        print("Note not found.")
    else:
        utils.print_header(note["title"])
        print(note["content"])
        if note["tags"]:
            print(f"\nTags: {', '.join(note['tags'])}")
        print(f"Created: {note['created_at']}")
    utils.pause()


def search_notes():
    query = input("Search notes (title/content/tag): ").strip().lower()
    notes = load_notes()
    results = [
        n for n in notes
        if query in n["title"].lower()
        or query in n["content"].lower()
        or any(query in tag.lower() for tag in n["tags"])
    ]
    utils.print_header(f"Search Results for '{query}'")
    if not results:
        print("No matching notes.")
    else:
        list_notes(notes=results)
    utils.pause()


def delete_note():
    list_notes()
    note_id = input("\nEnter note ID to delete: ").strip()
    notes = load_notes()
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        print("Note not found.")
    else:
        notes = [n for n in notes if n["id"] != note_id]
        save_notes(notes)
        print(f"Note '{note['title']}' deleted.")
    utils.pause()


def get_summary():
    notes = load_notes()
    return {"total": len(notes)}


def menu():
    while True:
        utils.clear_screen()
        utils.print_header("NOTES")
        print("1. Add note")
        print("2. View all notes")
        print("3. View a note in full")
        print("4. Search notes")
        print("5. Delete note")
        print("0. Back to Dashboard")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_note()
            utils.pause()
        elif choice == "2":
            list_notes()
            utils.pause()
        elif choice == "3":
            view_note()
        elif choice == "4":
            search_notes()
        elif choice == "5":
            delete_note()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            utils.pause()
