
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


def make_button( text, callback):
    button = QPushButton(text)
    button.clicked.connect(callback)

    return button


def make_title_label():
    title_label = QLabel()
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold)) # 폰트 크기 및 굵기 설정

    return title_label