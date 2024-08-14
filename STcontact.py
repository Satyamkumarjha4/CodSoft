import streamlit as st
import sqlite3 as sql
import time

# Initialize SQLite database
def init_db():
    try:
        with sql.connect('Manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    name TEXT PRIMARY KEY,
                    phone TEXT,
                    email TEXT,
                    address TEXT
                )
            ''')
            conn.commit()
        st.write("Database initialized successfully.")
    except Exception as e:
        st.error(f"Error initializing database: {e}")

# Function to add a contact
def add_contact(name, phone, email, address):
    try:
        with sql.connect('Manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)',
                           (name, phone, email, address))
            conn.commit()
        return "Contact added successfully!"
    except sql.IntegrityError:
        return "A contact with this name already exists."
    except Exception as e:
        return f"Error adding contact: {e}"

# Function to update a contact
def update_contact(name, phone, email, address):
    try:
        with sql.connect('Manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE contacts SET phone = ?, email = ?, address = ? WHERE name = ?',
                           (phone, email, address, name))
            if cursor.rowcount > 0:
                conn.commit()
                return "Contact updated successfully!"
            else:
                return "No contact found with this name."
    except Exception as e:
        return f"Error updating contact: {e}"

# Function to delete a contact
def delete_contact(name):
    try:
        with sql.connect('Manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
            if cursor.rowcount > 0:
                conn.commit()
                return "Contact deleted successfully!"
            else:
                return "No contact found with this name."
    except Exception as e:
        return f"Error deleting contact: {e}"

# Function to search for a contact
def search_contact(name):
    try:
        with sql.connect('Manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT phone, email, address FROM contacts WHERE name = ?', (name,))
            result = cursor.fetchone()
            if result:
                phone, email, address = result
                return f"Name: {name}\nPhone: {phone}\nEmail: {email}\nAddress: {address}"
            else:
                return "No contact found with this name."
    except Exception as e:
        return f"Error searching contact: {e}"

# Function to view all contacts
def view_contacts():
    try:
        with sql.connect('Manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contacts')
            contacts = cursor.fetchall()
            return contacts
    except Exception as e:
        st.error(f"Error retrieving contacts: {e}")
        return []

# Main function to render the Streamlit app
def main():
    st.title('Contact Manager')
    init_db()

    st.sidebar.title("Contact Manager")
    action = st.sidebar.radio("Select action", ["Add Contact", "Update Contact", "Delete Contact", "Search Contact", "View Contacts"])

    if action == "Add Contact":
        st.subheader("Add a new contact")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_input("Address")

        if st.button("Add Contact"):
            message = add_contact(name, phone, email, address)
            st.success(message)

    elif action == "Update Contact":
        st.subheader("Update an existing contact")
        name = st.text_input("Name")
        phone = st.text_input("New Phone")
        email = st.text_input("New Email")
        address = st.text_input("New Address")

        if st.button("Update Contact"):
            message = update_contact(name, phone, email, address)
            st.success(message)

    elif action == "Delete Contact":
        st.subheader("Delete a contact")
        name = st.text_input("Name")

        if st.button("Delete Contact"):
            message = delete_contact(name)
            st.success(message)

    elif action == "Search Contact":
        st.subheader("Search for a contact")
        name = st.text_input("Name")

        if st.button("Search Contact"):
            message = search_contact(name)
            st.text(message)

    elif action == "View Contacts":
        st.subheader("All Contacts")
        contacts = view_contacts()
        if contacts:
            for contact in contacts:
                st.write(f"{contact[0]} - {contact[1]}- {contact[2]} - {contact[3]}")
        else:
            st.write("No contacts available.")

if __name__ == "__main__":
    main()
