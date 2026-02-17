import os

NOTES_FILE = "notes.txt"

def add_note(text):
    try:
        with open(NOTES_FILE, "a") as f:
            f.write(f"- {text}\n")
        return "Note saved."
    except Exception as e:
        return f"Could not save note: {e}"

def read_notes(last_n=5):
    if not os.path.exists(NOTES_FILE):
        return "You have no notes."
    
    try:
        with open(NOTES_FILE, "r") as f:
            lines = f.readlines()
            if not lines:
                return "Your notes are empty."
            
            recent = lines[-last_n:]
            content = "".join(recent)
            return f"Here are your entries:\n{content}"
    except Exception as e:
        return f"Could not read notes: {e}"
