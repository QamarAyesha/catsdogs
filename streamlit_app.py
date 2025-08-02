import streamlit as st

st.set_page_config(page_title="📝 Simple Notes App", layout="centered")
st.title("🗒️ My Notes")
st.caption("Write and save your notes easily.")

# Initialize the notes list in session state
if "notes" not in st.session_state:
    st.session_state.notes = []

# Add new note
st.subheader("Add a New Note")
note = st.text_area("🖊️ Write your note here:", height=150)

if st.button("➕ Add Note"):
    if note.strip() != "":
        st.session_state.notes.append(note.strip())
        st.success("Note added!")
    else:
        st.warning("Note is empty.")

st.markdown("---")
st.subheader("📚 Saved Notes")

if st.session_state.notes:
    for i, saved_note in enumerate(st.session_state.notes):
        st.markdown(f"**Note {i+1}:** {saved_note}")
        if st.button(f"🗑️ Delete Note {i+1}", key=f"del_{i}"):
            st.session_state.notes.pop(i)
            st.experimental_rerun()
else:
    st.info("No notes yet. Add one above!")


