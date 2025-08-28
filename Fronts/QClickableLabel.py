
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtSignal

class QClickableLabel(QLabel):
    # 클릭 시그널 정의
    clicked = pyqtSignal()
    
    def __init__(self, parent=None, movie_idx=-1):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.idx = movie_idx

    def mousePressEvent(self, event):
        self.clicked.emit()