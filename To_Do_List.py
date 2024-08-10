import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime

class ToDoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('To-Do List Application')
        self.setGeometry(100, 100, 600, 400)
        
        # Layouts
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.input_layout = QHBoxLayout()
        self.layout.addLayout(self.input_layout)
        
        # Widgets
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Enter a new task')
        self.input_layout.addWidget(self.task_input)
        
        self.deadline_input = QDateTimeEdit(self)
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDateTime(QDateTime.currentDateTime())
        self.input_layout.addWidget(self.deadline_input)
        
        self.add_task_button = QPushButton('Add Task', self)
        self.add_task_button.clicked.connect(self.add_task)
        self.input_layout.addWidget(self.add_task_button)
        
        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(['Task', 'Deadline', 'Completed'])
        self.layout.addWidget(self.task_table)
        
        self.update_task_button = QPushButton('Update Task', self)
        self.update_task_button.clicked.connect(self.update_task)
        self.layout.addWidget(self.update_task_button)
        
        self.delete_task_button = QPushButton('Delete Task', self)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_task_button)

    def add_task(self):
        task_text = self.task_input.text()
        deadline = self.deadline_input.dateTime().toString('yyyy-MM-dd HH:mm')
        if task_text:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            
            task_item = QTableWidgetItem(task_text)
            task_item.setFlags(task_item.flags() | Qt.ItemIsUserCheckable)
            task_item.setCheckState(Qt.Unchecked)
            
            deadline_item = QTableWidgetItem(deadline)
            deadline_item.setFlags(deadline_item.flags() & ~Qt.ItemIsEditable)
            
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemIsUserCheckable)
            checkbox_item.setCheckState(Qt.Unchecked)
            
            self.task_table.setItem(row_position, 0, task_item)
            self.task_table.setItem(row_position, 1, deadline_item)
            self.task_table.setItem(row_position, 2, checkbox_item)
            
            self.task_input.clear()
        else:
            QMessageBox.warning(self, 'Error', 'Task cannot be empty')

    def update_task(self):
        selected_items = self.task_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Error', 'No task selected')
            return
        
        selected_row = selected_items[0].row()
        task_item = self.task_table.item(selected_row, 0)
        deadline_item = self.task_table.item(selected_row, 1)

        new_task_text, ok = QInputDialog.getText(self, 'Update Task', 'Enter new task:', QLineEdit.Normal, task_item.text())
        if ok and new_task_text:
            task_item.setText(new_task_text)
        
        new_deadline, ok = QInputDialog.getText(self, 'Update Deadline', 'Enter new deadline (yyyy-MM-dd HH:mm):', QLineEdit.Normal, deadline_item.text())
        if ok and new_deadline:
            deadline_item.setText(new_deadline)
    
    def delete_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Error', 'No task selected')
            return
        
        self.task_table.removeRow(selected_row)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToDoListApp()
    ex.show()
    sys.exit(app.exec_())
