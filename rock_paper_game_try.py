import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QFont

class RockPaperScissorsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.reset_scores()

    def initUI(self):
        self.setWindowTitle('Rock-Paper-Scissors Game')
        self.setGeometry(100, 100, 400, 400)  # Adjusted height to fit the layout

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Game buttons
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.rock_button = QPushButton('Rock', self)
        self.rock_button.clicked.connect(lambda: self.play('Rock'))
        self.button_layout.addWidget(self.rock_button)

        self.paper_button = QPushButton('Paper', self)
        self.paper_button.clicked.connect(lambda: self.play('Paper'))
        self.button_layout.addWidget(self.paper_button)

        self.scissors_button = QPushButton('Scissors', self)
        self.scissors_button.clicked.connect(lambda: self.play('Scissors'))
        self.button_layout.addWidget(self.scissors_button)

        # Result and score labels with larger font
        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont('Arial', 16))  # Larger font size for result
        self.layout.addWidget(self.result_label)

        self.score_label = QLabel('Wins: 0 | Losses: 0 | Attempts: 0', self)
        self.score_label.setFont(QFont('Arial', 14))  # Larger font size for score
        self.layout.addWidget(self.score_label)

    def reset_scores(self):
        self.wins = 0
        self.losses = 0
        self.attempts = 0
        self.update_score_label()

    def update_score_label(self):
        # Style the score label to make it more game-like
        self.score_label.setText(
            f'<b>Wins:</b> {self.wins}  |  <b>Losses:</b> {self.losses}  |  <b>Attempts:</b> {self.attempts}'
        )
        self.score_label.setFont(QFont('Arial', 14))  # Larger font size for score

    def play(self, user_choice):
        choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(choices)
        result = self.determine_winner(user_choice, computer_choice)
        self.attempts += 1
        self.update_score(result)
        self.result_label.setText(f'<b>You chose:</b> {user_choice}<br><b>Computer chose:</b> {computer_choice}<br><b>Result:</b> {result}')
        self.result_label.setFont(QFont('Arial', 16))  # Larger font size for result
        self.update_score_label()

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return 'It\'s a tie!'
        elif (user_choice == 'Rock' and computer_choice == 'Scissors') or \
             (user_choice == 'Scissors' and computer_choice == 'Paper') or \
             (user_choice == 'Paper' and computer_choice == 'Rock'):
            return 'You win!'
        else:
            return 'You lose!'

    def update_score(self, result):
        if result == 'You win!':
            self.wins += 1
        elif result == 'You lose!':
            self.losses += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RockPaperScissorsApp()
    ex.show()
    sys.exit(app.exec_())
