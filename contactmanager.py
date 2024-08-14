import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt
import sqlite3 as sql


class ContactManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDatabase()

    def initUI(self):
        self.setWindowTitle('Contact Manager')
        self.setGeometry(100, 100, 500, 400)

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Form layout for adding and updating contacts
        self.form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.address_input = QLineEdit(self)

        self.form_layout.addRow('Name:', self.name_input)
        self.form_layout.addRow('Phone:', self.phone_input)
        self.form_layout.addRow('Email:', self.email_input)
        self.form_layout.addRow('Address:', self.address_input)

        self.layout.addLayout(self.form_layout)

        # Buttons for adding, updating, deleting, and searching contacts
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton('Add Contact', self)
        self.update_button = QPushButton('Update Contact', self)
        self.delete_button = QPushButton('Delete Contact', self)
        self.search_button = QPushButton('Search Contact', self)
        self.view_button = QPushButton('View Contacts', self)

        self.add_button.clicked.connect(self.add_contact)
        self.update_button.clicked.connect(self.update_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.search_button.clicked.connect(self.search_contact)
        self.view_button.clicked.connect(self.view_contacts)

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.update_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.search_button)
        self.button_layout.addWidget(self.view_button)

        self.layout.addLayout(self.button_layout)

        # List widget to display contacts
        self.contact_list = QListWidget(self)
        self.layout.addWidget(self.contact_list)

    def initDatabase(self):
        self.conn = sql.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                name TEXT PRIMARY KEY,
                phone TEXT,
                email TEXT,
                address TEXT
            )
        ''')
        self.conn.commit()

    def add_contact(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if name and phone:
            try:
                self.cursor.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)',
                                    (name, phone, email, address))
                self.conn.commit()
                QMessageBox.information(self, 'Contact Added', f'Contact {name} added successfully!')
            except sql.IntegrityError:
                QMessageBox.warning(self, 'Contact Exists', f'A contact with the name {name} already exists.')
            self.clear_inputs()
            self.view_contacts()  # Refresh the contact list
        else:
            QMessageBox.warning(self, 'Input Error', 'Name and Phone are required fields.')

    def update_contact(self):
        name = self.name_input.text().strip()
        if name:
            phone = self.phone_input.text().strip()
            email = self.email_input.text().strip()
            address = self.address_input.text().strip()
            
            self.cursor.execute('UPDATE contacts SET phone = ?, email = ?, address = ? WHERE name = ?',
                                (phone, email, address, name))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                QMessageBox.information(self, 'Contact Updated', f'Contact {name} updated successfully!')
            else:
                QMessageBox.warning(self, 'Contact Not Found', f'No contact found with name {name}.')
            self.clear_inputs()
            self.view_contacts()  # Refresh the contact list
        else:
            QMessageBox.warning(self, 'Input Error', 'Name is required to update.')

    def delete_contact(self):
        name = self.name_input.text().strip()
        if name:
            self.cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                QMessageBox.information(self, 'Contact Deleted', f'Contact {name} deleted successfully!')
            else:
                QMessageBox.warning(self, 'Contact Not Found', f'No contact found with name {name}.')
            self.clear_inputs()
            self.view_contacts()  # Refresh the contact list
        else:
            QMessageBox.warning(self, 'Input Error', 'Name is required to delete.')

    def search_contact(self):
        name = self.name_input.text().strip()
        if name:
            self.cursor.execute('SELECT phone, email, address FROM contacts WHERE name = ?', (name,))
            result = self.cursor.fetchone()
            if result:
                phone, email, address = result
                details = (f"Name: {name}\nPhone: {phone}\nEmail: {email}\nAddress: {address}")
                QMessageBox.information(self, 'Contact Found', details)
            else:
                QMessageBox.warning(self, 'Contact Not Found', f'No contact found with name {name}.')
        else:
            QMessageBox.warning(self, 'Input Error', 'Name is required to search.')

    def view_contacts(self):
        self.contact_list.clear()
        self.cursor.execute('SELECT name, phone FROM contacts')
        contacts = self.cursor.fetchall()
        for name, phone in contacts:
            self.contact_list.addItem(f"{name} - {phone}")

    def clear_inputs(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ContactManagerApp()
    ex.show()
    sys.exit(app.exec_())
