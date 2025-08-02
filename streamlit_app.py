import streamlit as st
import json
import os
from datetime import datetime
from io import StringIO

NOTES_FILE = "notes.json"

# Load notes from file
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

# Save notes to file
def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

# Initialize session state
if "notes" not in st.session_state:
    st.session_state.notes = load_notes()

# --- UI Layout ---
st.title("📝 Smart Note-Taking App")

st.markdown("Enter your note below, tag it, and click 'Add Note'.")

with st.form("note_form", clear_on_submit=True):
    note_text = st.text_area("Your Note", height=150)
    category = st.selectbox("Category", ["General", "Work", "Personal", "Ideas", "To-Do"])
    submitted = st.form_submit_button("Add Note")
    if submitted and note_text.strip():
        new_note = {
            "text": note_text,
            "category": category,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.notes.append(new_note)
        save_notes(st.session_state.notes)
        st.success("Note added successfully!")

# --- Category Filter ---
st.markdown("### 📂 Filter Notes by Category")
selected_category = st.selectbox("View category", ["All"] + sorted(set(note["category"] for note in st.session_state.notes)))

# --- Display Notes ---
st.markdown("### 🗂️ Your Notes")

filtered_notes = st.session_state.notes if selected_category == "All" else [
    note for note in st.session_state.notes if note["category"] == selected_category
]

if not filtered_notes:
    st.info("No notes to display.")
else:
    for idx, note in enumerate(filtered_notes):
        with st.expander(f"🗒️ {note['category']} — {note['timestamp']}"):
            st.markdown(note["text"], unsafe_allow_html=True)
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("🗑️ Delete", key=f"delete_{idx}"):
                    # Remove from both session and file
                    original_index = st.session_state.notes.index(note)
                    st.session_state.notes.pop(original_index)
                    save_notes(st.session_state.notes)
                    st.experimental_rerun()

# --- Download Button ---
st.markdown("### 📥 Download Notes")
if st.session_state.notes:
    all_notes_text = ""
    for note in st.session_state.notes:
        all_notes_text += f"[{note['timestamp']}] ({note['category']})\n{note['text']}\n\n"

    st.download_button("Download All Notes as .txt", data=all_notes_text, file_name="my_notes.txt", mime="text/plain")
else:
    st.warning("No notes available for download.")



